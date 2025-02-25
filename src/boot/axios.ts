import axios, { AxiosInstance, AxiosError, AxiosRequestConfig } from 'axios'
import router from '@/router'

const api = axios.create({
  baseURL: process.env.VUE_APP_DEV ? 'http://185.211.170.161:8000/api/v1/' : '/api/v1',
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json'
  }
})

export { api }

api.interceptors.response.use(
  (response) => {
    return response
  },
  (error: AxiosError) => {
    if (error.response) {
      const status = error.response.status;
      if (status === 401) {
        localStorage.removeItem('token');
        router.push('/auth');
      }
      return Promise.reject(error.response.data);
    }
  }
)