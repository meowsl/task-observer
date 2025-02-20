import axios from 'axios'

const api = axios.create({
  baseURL: process.env.DEV ? 'http://localhost:8000/api/v1/' : '/api/v1',
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json'
  }
})

export { api }