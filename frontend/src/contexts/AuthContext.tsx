import { 
    createContext, 
    useEffect, 
    useState, 
    type FormEventHandler, 
    type ReactNode 
} from "react"
import type { 
    AuthContextType, 
    LogoutUserType, 
    RegisterUserType, 
    Tokens, 
    User 
} from "@/types/authorization"
import { useNavigate } from "react-router"
import { jwtDecode } from "jwt-decode"
import useAxios from "@/hooks/useAxios"

const AuthContext = createContext<AuthContextType | {}>({})
export default AuthContext

export const Authprovider = ({children}: {children: ReactNode}) => {
    
    const localTokens = localStorage.getItem("authTokens")
    const [authTokens, setAuthTokens] = useState<Tokens|null>(null)
    const [user, setUser] = useState<User|null>(null)
    const [loading, setLoading] = useState<boolean>(true)

    const api = useAxios()
    const navigate = useNavigate()

    useEffect(() => {
        if (localTokens) {
            setAuthTokens(JSON.parse(localTokens))
            setUser(jwtDecode(localTokens))
        }
    },[])

    useEffect(() => {
        if (authTokens) setUser(jwtDecode(authTokens.access))
        setLoading(false)
    }, [authTokens, loading])

    interface LoginEventTarget extends EventTarget {
        email: {value: string},
        password: {value: string}
    }

    const loginUser:FormEventHandler<HTMLFormElement> = (event) => {
        event.preventDefault()
        const target = event.target as LoginEventTarget
        api
            .create("/token/", {
                "email": target.email.value,
                "password": target.password.value
            })
            .then(data =>{
                setAuthTokens(data)
                setUser(jwtDecode(data.access))
                localStorage.setItem('authTokens', JSON.stringify(data))
                navigate(-2) // redirects to element from PrivateRoute
            })
    }

    const registerUser:RegisterUserType = event => {
        event.preventDefault()
        api
            .create("/member/register/", {
                first_name: event.target.first_name.value,
                last_name: event.target.last_name.value,
                email: event.target.email.value,
                password: event.target.password.value,
                working_group: event.target.working_group.value
            })
            .then(() => loginUser(event)) // TODO: landing page for inactive users, captcha?
    }

    const logoutUser:LogoutUserType = () => {
        setUser(null)
        setAuthTokens(null)
        localStorage.removeItem('authTokens')
        navigate("/")
    }
    
    let contextData = {
        user,
        setUser,
        authTokens,
        setAuthTokens,
        loginUser,
        logoutUser,
        registerUser
    }

    return(
        <AuthContext.Provider value={contextData}>
            {loading ? null : children}
        </AuthContext.Provider>
    )
}