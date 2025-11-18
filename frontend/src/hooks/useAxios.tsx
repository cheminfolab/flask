import { useContext } from "react"
import type { AuthContextType, User } from "@/types/authorization"
import axios from "axios"
import { jwtDecode } from "jwt-decode"
import dayjs from "dayjs"
import AuthContext from "@/contexts/AuthContext"

const useAxios = (authentication=false) => {
    
    const baseURL = import.meta.env.VITE_API_BASE_URL || "/api"
    
    const {
        authTokens,
        setAuthTokens,
        setUser,
        logoutUser
    } = useContext(AuthContext) as AuthContextType

    const axiosInstance = axios.create({
        baseURL: baseURL,
        timeout: 5000, // ms
        headers: {
            'Content-Type': 'application/json',
            accept: 'application/json'
        }
    })

    if (authentication) {
        axiosInstance.defaults.headers['Authorization'] = `Bearer ${authTokens?.access}`
        axiosInstance.interceptors.request.use(request => {
            // check if token is expired
            const user: User = jwtDecode(authTokens.access)
            const isExpired = dayjs.unix(user.exp).diff(dayjs(), 'second') < 30;
            if (!isExpired) return request

            // if token is expired, request new token
            axios
                .post(`${baseURL}/token/refresh/`, {refresh: authTokens.refresh})
                .then(response => {
                    const tokens = response.data
                    setAuthTokens(tokens)
                    setUser(jwtDecode(tokens.access))
                    localStorage.setItem('authTokens', JSON.stringify(tokens))
                    request.headers.Authorization = `Bearer ${tokens.access}`
                })
                .catch(error => console.log("error during token refreshment:", error.response.statusText))
            return request
        })
    }

    const getAll = (url: string) => axiosInstance
        .get(url)
        .then(response => response.data)
        .catch(error => {
            console.error("Error for GET request:", error)
            if (error.response.status === 401) logoutUser()
            return Promise.reject(error)
        })

    const get = (url: string, id: string | number) => axiosInstance
        .get(`${url}/${id}`)
        .then(response => response.data)
        .catch(error => {
            console.error("Error for GET request:", error)
            if (error.response.status === 401) logoutUser()
            return Promise.reject(error)
        })

    const create = (url: string, newObject: {}) => axiosInstance
        .post(url, newObject)
        .then(response => response.data)
        .catch(error => {
            console.error("Error for POST request:", error)
            if (error.response.status === 401) logoutUser()
            return Promise.reject(error)
        })

    const update = (url: string, id: string | number, newObject: {}) => axiosInstance
        .put(`${url}/${id}`, newObject)
        .then(response => response.data)
        .catch(error => {
            console.error("Error for PUT request:", error)
            if (error.response.status === 401) logoutUser()
            return Promise.reject(error)
        })

    const remove = (url: string, id: string | number) => axiosInstance
        .delete(`${url}/${id}`)
        .then(response => console.log('delete response', response))
        .catch(error => {
            console.error("Error for DELETE request:", error)
            if (error.response.status === 401) logoutUser()
            return Promise.reject(error)
        })

    return {axiosInstance, getAll, get, create, update, remove}
}

export default useAxios