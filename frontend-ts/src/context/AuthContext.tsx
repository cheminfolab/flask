import {createContext, useEffect, useState} from "react";
import {useNavigate} from 'react-router-dom'
import jwt_decode from 'jwt-decode';
import useAxios from "../utils/useAxios";


const AuthContext = createContext({})
export default AuthContext


export const AuthProvider = ({children}) => {

    // todo: rewrite !
    let [authTokens, setAuthTokens] = useState(() => (
        localStorage.getItem('authTokens') ? JSON.parse(localStorage.getItem('authTokens')) : null
    ))
    let [user, setUser] = useState(() => (
        localStorage.getItem('authTokens') ? jwt_decode(localStorage.getItem('authTokens')) : null
    ))
    let [loading, setLoading] = useState(true)

    const navigate = useNavigate()
    let api = useAxios()

    let loginUser = async (e) => {
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
            .catch( (error) => console.log(error))
    }

    let registerUser = async (event) => {
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

    let logoutUser = () => {
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