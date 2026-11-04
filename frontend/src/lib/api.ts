/**
 * Shared API client.
 *
 * One axios instance for the whole app. The request interceptor attaches the
 * access token and, when it is about to expire, waits for a refresh before
 * sending. Concurrent requests share a single in-flight refresh, which matters
 * because the backend rotates and blacklists refresh tokens: a second refresh
 * with the old token would fail. A 401 response triggers one refresh + retry.
 */
import axios, { AxiosError } from "axios"
import { jwtDecode } from "jwt-decode"
import type { Tokens, User } from "@/types/authorization"

declare module "axios" {
    interface AxiosRequestConfig {
        /** send without Authorization header and without refresh handling (login, register, refresh) */
        skipAuth?: boolean
        /** internal: request was already retried after a 401 */
        retried?: boolean
    }
}

const STORAGE_KEY = "authTokens"
const EXPIRY_MARGIN_SECONDS = 30

export const baseURL: string = import.meta.env.VITE_API_BASE_URL || "/api"

export const api = axios.create({
    baseURL,
    timeout: 15000, // ms
    headers: { "Content-Type": "application/json", accept: "application/json" },
})

// ---------------------------------------------------------------- tokens

type AuthListener = (tokens: Tokens | null) => void
const listeners = new Set<AuthListener>()

/** Subscribe to token changes (refresh, logout). Returns an unsubscribe function. */
export const onAuthChange = (listener: AuthListener) => {
    listeners.add(listener)
    return () => { listeners.delete(listener) }
}

const secondsLeft = (token: string): number => {
    try {
        const { exp } = jwtDecode<{ exp: number }>(token)
        return exp - Date.now() / 1000
    } catch {
        return -Infinity // malformed token counts as expired
    }
}

export const decodeUser = (tokens: Tokens | null): User | null => {
    if (!tokens) return null
    try {
        return jwtDecode<User>(tokens.access)
    } catch {
        return null
    }
}

/** Stored tokens, or null if missing, malformed, or the refresh token has expired. */
export const loadTokens = (): Tokens | null => {
    try {
        const raw = localStorage.getItem(STORAGE_KEY)
        if (!raw) return null
        const tokens = JSON.parse(raw) as Tokens
        if (!tokens?.access || !tokens?.refresh || secondsLeft(tokens.refresh) <= 0) return null
        return tokens
    } catch {
        return null
    }
}

let currentTokens: Tokens | null = loadTokens()

export const setTokens = (tokens: Tokens | null) => {
    currentTokens = tokens
    try {
        if (tokens) localStorage.setItem(STORAGE_KEY, JSON.stringify(tokens))
        else localStorage.removeItem(STORAGE_KEY)
    } catch {
        // storage unavailable (private mode): keep the session in memory only
    }
    listeners.forEach(listener => listener(tokens))
}

export const getTokens = () => currentTokens

// ---------------------------------------------------------------- refresh

let refreshInFlight: Promise<Tokens | null> | null = null

/** Refresh the access token once, shared by all concurrent callers. Resolves to null on failure (logged out). */
export const refreshTokens = (): Promise<Tokens | null> => {
    if (refreshInFlight) return refreshInFlight
    const refresh = currentTokens?.refresh
    if (!refresh) return Promise.resolve(null)

    refreshInFlight = api
        .post<{ access: string, refresh?: string }>("/token/refresh/", { refresh }, { skipAuth: true })
        .then(response => {
            // with ROTATE_REFRESH_TOKENS the response carries a new refresh token; keep the old one otherwise
            const tokens: Tokens = { access: response.data.access, refresh: response.data.refresh ?? refresh }
            setTokens(tokens)
            return tokens
        })
        .catch(() => {
            setTokens(null)
            return null
        })
        .finally(() => { refreshInFlight = null })
    return refreshInFlight
}

api.interceptors.request.use(async config => {
    if (config.skipAuth) return config
    let tokens = currentTokens
    if (tokens && secondsLeft(tokens.access) < EXPIRY_MARGIN_SECONDS) {
        tokens = await refreshTokens()
    }
    if (tokens) config.headers.Authorization = `Bearer ${tokens.access}`
    return config
})

api.interceptors.response.use(undefined, async (error: AxiosError) => {
    const config = error.config
    if (error.response?.status === 401 && config && !config.skipAuth && !config.retried && currentTokens) {
        config.retried = true
        const tokens = await refreshTokens()
        if (tokens) return api(config)
    }
    return Promise.reject(error)
})

// ---------------------------------------------------------------- helpers

/** `/resource/` or `/resource/<id>/`, tolerant of leading/trailing slashes in `resource`. */
export const resourceUrl = (resource: string, id?: string | number) => {
    const path = resource.replace(/^\/+|\/+$/g, "")
    return id === undefined ? `/${path}/` : `/${path}/${encodeURIComponent(String(id))}/`
}

/** Human-readable message for any request failure, including network errors and timeouts. */
export const errorMessage = (error: unknown): string => {
    if (axios.isAxiosError(error)) {
        if (!error.response) return "The server could not be reached. Please check your connection."
        const data = error.response.data as { detail?: unknown } | undefined
        if (data && typeof data.detail === "string") return data.detail
        return `Request failed (${error.response.status}).`
    }
    return "An unexpected error occurred."
}

/** One page of a list endpoint (every list endpoint is paginated). */
export interface Page<T> {
    count: number
    next: string | null
    previous: string | null
    results: T[]
}

export type ListParams = Record<string, string | number | boolean | undefined> & {
    page?: number
    page_size?: number
}

/** Largest page the backend accepts (DefaultPagination.max_page_size). */
const MAX_PAGE_SIZE = 500
/** getAll() is for small reference lists; refuse to pull more than this many rows. */
const GET_ALL_LIMIT = 10_000

const list = <T>(resource: string, params: ListParams = {}) =>
    api.get<Page<T>>(resourceUrl(resource), { params }).then(r => r.data)

/** Every row of a small list (working groups, storages, ...), fetched page by page. */
const getAll = async <T>(resource: string, params: ListParams = {}): Promise<T[]> => {
    const rows: T[] = []
    for (let page = 1; ; page += 1) {
        const data = await list<T>(resource, { ...params, page, page_size: MAX_PAGE_SIZE })
        rows.push(...data.results)
        if (!data.next) return rows
        if (rows.length >= GET_ALL_LIMIT) {
            throw new Error(`${resource}: more than ${GET_ALL_LIMIT} rows; use list() with paging instead`)
        }
    }
}

/** Thin CRUD wrapper returning response bodies. */
export const apiClient = {
    list,
    getAll,
    get: <T = unknown>(resource: string, id: string | number) => api.get<T>(resourceUrl(resource, id)).then(r => r.data),
    create: <T = unknown>(resource: string, body: object) => api.post<T>(resourceUrl(resource), body).then(r => r.data),
    update: <T = unknown>(resource: string, id: string | number, body: object) =>
        api.put<T>(resourceUrl(resource, id), body).then(r => r.data),
    patch: <T = unknown>(resource: string, id: string | number, body: object) =>
        api.patch<T>(resourceUrl(resource, id), body).then(r => r.data),
    remove: (resource: string, id: string | number) => api.delete(resourceUrl(resource, id)).then(() => undefined),
}

export type ApiClient = typeof apiClient

/**
 * Log out: forget the tokens locally right away and ask the backend to blacklist
 * the refresh token, so a copied token cannot be used to stay logged in.
 */
export const endSession = (): Promise<void> => {
    const refresh = currentTokens?.refresh
    setTokens(null)
    if (!refresh) return Promise.resolve()
    return api
        .post("/token/blacklist/", { refresh }, { skipAuth: true })
        .then(() => undefined)
        .catch(() => undefined)  // already expired or blacklisted: nothing left to revoke
}
