import {createContext, useEffect, useState} from "react";
import {useNavigate} from 'react-router-dom'
import jwt_decode from 'jwt-decode';
import useAxios from "../utils/useAxios";
import {Tokens, User, LoginUserType, LogoutUserType, RegisterUserType, AuthContextType} from "../@types/authorization"


const AuthContext = createContext<AuthContextType | {}>({})
export default AuthContext

export const AuthProvider = ({children}) => {

    let localTokens = localStorage.getItem('authTokens')

    let [authTokens, setAuthTokens] = useState<Tokens | null>(() => localTokens ? JSON.parse(localTokens) : null)
    let [user, setUser] = useState<User | null>(() => localTokens ? jwt_decode(localTokens) : null)
    let [loading, setLoading] = useState<boolean>(true)

    const navigate = useNavigate()
    let api = useAxios()

    let loginUser:LoginUserType = async (e) => {
        e.preventDefault()
        await api.axiosInstance // todo: unite multiple services in one instance!
            .post('/token/', {
                'email':e.target.email.value,
                'password':e.target.password.value
            })
            .then( (response) => {
                if (response.status === 200) {
                    const data = response.data
                    setAuthTokens(data)
                    setUser(jwt_decode(data.access))
                    localStorage.setItem('authTokens', JSON.stringify(data))
                    navigate(-2) // redirects to element from PrivateRoute
                } else {
                    alert('Something went wrong.')
                }
            })
            .catch(error => console.log(error))
    }

    let registerUser:RegisterUserType = async event => {
        event.preventDefault()
        await api.axiosInstance
            .post('/member/register/', {
                first_name: event.target.first_name.value,
                last_name: event.target.last_name.value,
                email: event.target.email.value,
                password:event.target.password.value,
                working_group: event.target.working_group.value
            })
            .then( (response) => {
                if (response.status === 200) {
                    loginUser(event)
                    // todo: notification / redirection to user page (prompt user for additional info: phone etc.)
                } else {
                    alert('Something went wrong!')
                }
            })
            .catch( (error) => console.log(error))
    }

    let logoutUser:LogoutUserType = () => {
        setUser(null)
        setAuthTokens(null)
        localStorage.removeItem('authTokens')
        navigate('/')
    }


    useEffect(() => {
        if (authTokens){
            setUser(jwt_decode(authTokens.access))
        }
        setLoading(false)
    }, [authTokens, loading])

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