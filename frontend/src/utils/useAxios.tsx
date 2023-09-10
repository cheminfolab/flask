import {useContext} from "react";
import axios from "axios";
import jwt_decode from "jwt-decode";
import * as dayjs from "dayjs";
import AuthContext from "../context/AuthContext";
import {AuthContextType, User} from "../@types/authorization";

const apiPath = `${process.env.REACT_APP_API_BASE_URL}/api`

const useAxios = (authentication=false) => {
    const { authTokens, setAuthTokens, setUser, logoutUser } = useContext(AuthContext) as AuthContextType
    const axiosInstance = axios
        .create({
            baseURL: apiPath,
            timeout: 5000, // ms
            headers:{
                'Content-Type': 'application/json',
                accept: 'application/json'
            }
        })
    if (authentication){
        axiosInstance.defaults.headers['Authorization'] = `Bearer ${authTokens?.access}`
        axiosInstance.interceptors.request.use(
            async req => {

                // check if token is expired
                const user:User = jwt_decode(authTokens.access)
                const isExpired = dayjs.unix(user.exp).diff(dayjs(), 'second') < 30;
                if (!isExpired) return req

                // if token is expired, request new token
                const response = await axios.post(`${apiPath}/token/refresh/`, {
                    refresh:authTokens.refresh
                })

                localStorage.setItem('authTokens', JSON.stringify(response.data)) // redundant?

                setAuthTokens(response.data)
                setUser(jwt_decode(response.data.access))

                req.headers.Authorization = `Bearer ${response.data.access}`
                return req
            }
        )
    }
    const getAll = url => axiosInstance
        .get(url)
        .then(response => {
            if (response.statusText === 'Unauthorized') logoutUser()
            return response.data
        })

    const get = (url, id) => axiosInstance
        .get(`${url}/${id}`)
        .then(response => {
            if (response.statusText === 'Unauthorized') logoutUser()
            return response.data
        })

    const create = (url, newObject) => axiosInstance
        .post(url, newObject)
        .then(response => {
            if (response.statusText === 'Unauthorized') logoutUser()
            return response.data
        })

    const update = (url, id, newObject) => axiosInstance
        .put(`${url}/${id}`, newObject)
        .then(response => {
            if (response.statusText === 'Unauthorized') logoutUser()
            return response.data
        })

    const remove = (url, id) => axiosInstance
        .delete(`${url}/${id}`)
        .then(response => {
            if (response.statusText === 'Unauthorized') logoutUser()
            console.log('delete response', response)
        })


    return {axiosInstance, getAll, get, create, update, remove}
}

export default useAxios