export interface Tokens {
    access: string
    refresh: string
}

export interface User {
  token_type: string
  exp: number
  iat: number
  jti: string
  user_id: number
  email: string
}

export type LoginUserType = (event:any) => Promise<void>
export type LogoutUserType = () => void
export type RegisterUserType = (event:any) => Promise<void>

export type AuthContextType = {
    "user": User
    "setUser": (User) => void
    "authTokens": Tokens
    "setAuthTokens": (Tokens) => void
    "loginUser": LoginUserType
    "logoutUser": LogoutUserType
    "registerUser": RegisterUserType
}

export type AuthModeType = "login" | "register"

export interface RegistrationForm {
    first_name: null | string
    last_name: null | string
    working_group: null | number
    status: null | number
    email: null | string
    password: null | string
    password2: null | string
}

export interface Errors {
    first_name?: string
    last_name?: string
    working_group?: string
    status?: string
    email?: string
    password?: string
    password2?: string
}