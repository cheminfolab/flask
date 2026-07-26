// import { Dispatch, SetStateAction } from "react"

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

export type RegisterUserType = (event: SubmitEvent<HTMLFormElement>) => void
export type LogoutUserType = () => void

export interface AuthContextType {
    user: User
    setUser: Dispatch<SetStateAction<User>>
    authTokens: Tokens
    setAuthTokens: Dispatch<SetStateAction<Tokens>>
    loginUser: LoginUserType
    logoutUser: LogoutUserType
    registerUser: RegisterUserType
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

type FormValidator = () => Errors
