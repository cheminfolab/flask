import { AxiosError, AxiosHeaders, type InternalAxiosRequestConfig } from "axios"
import { beforeEach, describe, expect, it, vi } from "vitest"

type ApiModule = typeof import("./api")

const base64url = (value: object) =>
    btoa(JSON.stringify(value)).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "")

/** Unsigned JWT expiring `seconds` from now (the client only decodes, never verifies). */
const jwt = (seconds: number, extra: object = {}) =>
    `${base64url({ alg: "HS256" })}.${base64url({ exp: Math.floor(Date.now() / 1000) + seconds, ...extra })}.sig`

const memoryStorage = () => {
    const data = new Map<string, string>()
    return {
        getItem: (key: string) => data.get(key) ?? null,
        setItem: (key: string, value: string) => { data.set(key, value) },
        removeItem: (key: string) => { data.delete(key) },
        clear: () => data.clear(),
    }
}

type Handler = (config: InternalAxiosRequestConfig) => { status: number, data?: unknown }

/** Load a fresh copy of the module with the given stored tokens and a fake HTTP adapter. */
const loadApi = async (stored: object | string | null, handler: Handler): Promise<ApiModule> => {
    vi.resetModules()
    const storage = memoryStorage()
    if (stored !== null) storage.setItem("authTokens", typeof stored === "string" ? stored : JSON.stringify(stored))
    vi.stubGlobal("localStorage", storage)
    const module = await import("./api")
    module.api.defaults.adapter = async config => {
        const { status, data } = handler(config)
        const response = { status, statusText: String(status), data, headers: {}, config }
        if (status >= 400) throw new AxiosError(`status ${status}`, "ERR_BAD_RESPONSE", config, null, response)
        return response
    }
    return module
}

const authHeader = (config: InternalAxiosRequestConfig) =>
    AxiosHeaders.from(config.headers).get("Authorization")

describe("resourceUrl", () => {
    it("normalizes slashes and appends a trailing slash", async () => {
        const { resourceUrl } = await loadApi(null, () => ({ status: 200 }))
        expect(resourceUrl("members")).toBe("/members/")
        expect(resourceUrl("/members/")).toBe("/members/")
        expect(resourceUrl("/members/", 5)).toBe("/members/5/")   // regression: was /members//5
        expect(resourceUrl("members/me")).toBe("/members/me/")
    })
})

describe("session restore", () => {
    it("drops sessions whose refresh token has expired", async () => {
        const { getTokens } = await loadApi({ access: jwt(-600), refresh: jwt(-60) }, () => ({ status: 200 }))
        expect(getTokens()).toBeNull()
    })

    it("drops malformed stored data instead of crashing", async () => {
        const { getTokens, decodeUser } = await loadApi("not json", () => ({ status: 200 }))
        expect(getTokens()).toBeNull()
        expect(decodeUser({ access: "garbage", refresh: "garbage" })).toBeNull()
    })

    it("decodes the user from the access token", async () => {
        const tokens = { access: jwt(300, { user_id: 7, email: "a@b.org" }), refresh: jwt(86400) }
        const { getTokens, decodeUser } = await loadApi(tokens, () => ({ status: 200 }))
        expect(decodeUser(getTokens())).toMatchObject({ user_id: 7, email: "a@b.org" })
    })
})

describe("token refresh", () => {
    it("waits for one shared refresh before sending concurrent requests", async () => {
        const fresh = jwt(300)
        let refreshCalls = 0
        const sentWith: (string | undefined)[] = []
        const { apiClient, getTokens } = await loadApi(
            { access: jwt(5), refresh: jwt(86400) },  // access token about to expire
            config => {
                if (config.url === "/token/refresh/") {
                    refreshCalls += 1
                    return { status: 200, data: { access: fresh, refresh: "rotated" } }
                }
                sentWith.push(String(authHeader(config)))
                return { status: 200, data: { count: 0, next: null, previous: null, results: [] } }
            },
        )

        await Promise.all([apiClient.getAll("substances"), apiClient.getAll("units"), apiClient.getAll("containers")])

        expect(refreshCalls).toBe(1)  // regression: each request started its own refresh
        expect(sentWith).toEqual([`Bearer ${fresh}`, `Bearer ${fresh}`, `Bearer ${fresh}`])
        expect(getTokens()).toEqual({ access: fresh, refresh: "rotated" })
    })

    it("retries once after a 401 with a refreshed token", async () => {
        const fresh = jwt(300)
        const stale = jwt(300)
        const { apiClient } = await loadApi({ access: stale, refresh: jwt(86400) }, config => {
            if (config.url === "/token/refresh/") return { status: 200, data: { access: fresh } }
            return authHeader(config) === `Bearer ${fresh}`
                ? { status: 200, data: { count: 1, next: null, previous: null, results: ["ok"] } }
                : { status: 401 }
        })

        await expect(apiClient.getAll("substances")).resolves.toEqual(["ok"])
    })

    it("logs out when the refresh fails", async () => {
        const { apiClient, getTokens, onAuthChange } = await loadApi({ access: jwt(5), refresh: jwt(86400) }, config =>
            config.url === "/token/refresh/" ? { status: 401 } : { status: 401 },
        )
        const changes: unknown[] = []
        onAuthChange(tokens => changes.push(tokens))

        await expect(apiClient.getAll("substances")).rejects.toBeInstanceOf(AxiosError)

        expect(getTokens()).toBeNull()
        expect(changes).toEqual([null])
    })

    it("sends login without an Authorization header", async () => {
        let header: unknown = "unset"
        const { api } = await loadApi({ access: jwt(300), refresh: jwt(86400) }, config => {
            header = authHeader(config)
            return { status: 200, data: {} }
        })

        await api.post("/token/", {}, { skipAuth: true })

        expect(header).toBeUndefined()
    })
})

describe("errorMessage", () => {
    beforeEach(() => vi.resetModules())

    it("handles network errors without a response", async () => {
        // regression: error.response.status threw a TypeError on timeouts and connection loss
        const { errorMessage } = await loadApi(null, () => ({ status: 200 }))
        expect(errorMessage(new AxiosError("Network Error", "ERR_NETWORK"))).toMatch(/could not be reached/)
    })

    it("prefers the server's detail message", async () => {
        const { apiClient, errorMessage } = await loadApi(null, () => ({ status: 403, data: { detail: "Not allowed." } }))
        const error = await apiClient.getAll("units").catch(e => e)
        expect(errorMessage(error)).toBe("Not allowed.")
    })
})

describe("pagination", () => {
    const page = (results: number[], next: boolean) => ({ count: 1200, next: next ? "more" : null, previous: null, results })

    it("list() passes paging parameters and returns one page", async () => {
        let params: unknown
        const { apiClient } = await loadApi(null, config => {
            params = config.params
            return { status: 200, data: page([1, 2], true) }
        })

        const data = await apiClient.list<number>("substances", { page: 3, page_size: 2 })

        expect(params).toEqual({ page: 3, page_size: 2 })
        expect(data.results).toEqual([1, 2])
    })

    it("getAll() collects every page with the largest page size", async () => {
        const requested: unknown[] = []
        const { apiClient } = await loadApi(null, config => {
            requested.push(config.params)
            const current = (config.params as { page: number }).page
            return { status: 200, data: page([current], current < 3) }
        })

        await expect(apiClient.getAll<number>("groups")).resolves.toEqual([1, 2, 3])
        expect(requested).toEqual([1, 2, 3].map(p => ({ page: p, page_size: 500 })))
    })

    it("getAll() refuses unbounded lists", async () => {
        const { apiClient } = await loadApi(null, () => ({
            status: 200, data: page(Array.from({ length: 500 }, (_, i) => i), true),
        }))

        await expect(apiClient.getAll("substances")).rejects.toThrow(/use list\(\) with paging/)
    })
})

describe("endSession", () => {
    it("clears the session immediately and blacklists the refresh token", async () => {
        const refresh = jwt(86400)
        let posted: { url?: string, body?: unknown, auth?: unknown } = {}
        const { endSession, getTokens } = await loadApi({ access: jwt(300), refresh }, config => {
            posted = { url: config.url, body: JSON.parse(String(config.data)), auth: authHeader(config) }
            return { status: 200, data: {} }
        })

        const pending = endSession()
        expect(getTokens()).toBeNull()  // logged out before the request completes
        await pending

        expect(posted).toEqual({ url: "/token/blacklist/", body: { refresh }, auth: undefined })
    })

    it("still logs out when the server is unreachable", async () => {
        const { endSession, getTokens } = await loadApi({ access: jwt(300), refresh: jwt(86400) }, () => {
            throw new AxiosError("Network Error", "ERR_NETWORK")
        })

        await expect(endSession()).resolves.toBeUndefined()
        expect(getTokens()).toBeNull()
    })
})
