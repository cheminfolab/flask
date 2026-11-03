import type { Dispatch, FormEventHandler, SetStateAction } from "react"
import type { Location } from "react-router"

export interface Tokens {
    access: string
    refresh: string
}

/** Claims of the access token (not part of the OpenAPI schema). */
export interface User {
    token_type: string
    exp: number
    iat: number
    jti: string
    user_id: number
    email: string
}

export type { RegistrationPayload } from "./api"
import type { RegistrationPayload } from "./api"

// resolves when the (inactive) account was created; rejects with the axios error
export type RegisterUserType = (form: RegistrationPayload) => Promise<void>
export type LogoutUserType = () => void
export type LoginUserType = FormEventHandler<HTMLFormElement>

export interface LoginEventTarget extends EventTarget {
    email: {value: string}
    password: {value: string}
}

export interface AuthContextType {
    user: User | null          // null when logged out
    authTokens: Tokens | null
    loginUser: LoginUserType
    loginError: string | null  // message from the last failed login
    logoutUser: LogoutUserType
    registerUser: RegisterUserType
    redirect: Location | null
    setRedirect: Dispatch<SetStateAction<Location | null>>
}

export interface RegistrationForm {
    first_name: undefined | string
    last_name: undefined | string
    status: undefined | number
    email: undefined | string
    password: undefined | string
    password_confirm: undefined | string
}

export interface Errors {
    first_name?: string
    last_name?: string
    status?: string
    email?: string
    password?: string
    password_confirm?: string
}

export type FormValidator = () => Errors
