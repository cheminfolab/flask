import axios from "axios";

let authTokens = localStorage.getItem('authTokens') ? JSON.parse(localStorage.getItem('authTokens')) : null

const baseURL = 'http://127.0.0.1:8000'

const axiosInstance = axios.create({
    baseURL,
    headers:{
        'Authorization': `Bearer ${authTokens?.access}`
    },
})

export default axiosInstance