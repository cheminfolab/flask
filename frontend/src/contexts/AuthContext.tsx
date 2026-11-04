import {
    createContext,
    useEffect,
    useState,
    type FormEventHandler,
    type ReactNode
} from "react"
import type {
    AuthContextType,
    LoginEventTarget,
    LogoutUserType,
    RegisterUserType,
    Tokens,
} from "@/types/authorization"
import { useNavigate, type Location } from "react-router"
import axios from "axios"
import { api, decodeUser, errorMessage, getTokens, onAuthChange, setTokens } from "@/lib/api"

const AuthContext = createContext<AuthContextType | null>(null)
export default AuthContext

export const Authprovider = ({children}: {children: ReactNode}) => {
    // restored synchronously from storage (expired or malformed sessions are dropped)
    const [authTokens, setAuthTokens] = useState<Tokens | null>(getTokens)
    const [loginError, setLoginError] = useState<string | null>(null)
    const [redirect, setRedirect] = useState<Location | null>(null)
    const navigate = useNavigate()

    // follow token changes made by the API client (refresh, failed refresh = logout)
    useEffect(() => onAuthChange(setAuthTokens), [])

    const loginUser: FormEventHandler<HTMLFormElement> = event => {
        event.preventDefault()
        const target = event.target as LoginEventTarget
        setLoginError(null)
        api
            .post<Tokens>("/token/", {
                email: target.email.value,
                password: target.password.value,
            }, { skipAuth: true })
            .then(response => {
                setTokens(response.data)
                navigate(redirect ?? "/")
            })
            .catch(error => {
                // the backend answers 401 both for wrong credentials and for not-yet-approved accounts
                if (axios.isAxiosError(error) && error.response?.status === 401) {
                    setLoginError("Invalid email or password, or your account has not been approved yet.")
                } else {
                    setLoginError(errorMessage(error))
                }
            })
    }

    // New accounts are inactive until an admin approves them, so registration
    // does not log the user in. Errors propagate to the caller (the signup form).
    const registerUser: RegisterUserType = form => api
        .post("/members/register/", form, { skipAuth: true })
        .then(() => undefined)

    const logoutUser: LogoutUserType = () => {
        setTokens(null)
        navigate("/login")
    }

    const contextData: AuthContextType = {
        user: decodeUser(authTokens),
        authTokens,
        loginUser,
        loginError,
        logoutUser,
        registerUser,
        redirect,
        setRedirect,
    }

    return(
        <AuthContext.Provider value={contextData}>
            {children}
        </AuthContext.Provider>
    )
}
