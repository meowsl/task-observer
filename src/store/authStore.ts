import { createStore } from 'vuex'
import { api } from '@/boot/axios'
import { TokenPair, User, AuthState, UserRegistration } from '@/interfaces/user'

export const useAuthStore = createStore<AuthState>({
  state: {
    user: null,
    accessToken: localStorage.getItem('token') || null,
  },
  getters: {
    getUser(state) {
      return state.user
    },
    isAuthenticated(state) {
      return !!state.accessToken
    }
  },
  mutations: {
    setUser(state, user: User) {
      state.user = user
    },
    setAccessToken(state, token: string) {
      state.accessToken = token
      localStorage.setItem('token', token)
    },
    clearUser(state) {
      state.user = null
      state.accessToken = null
      localStorage.removeItem('token')
    }
  },
  actions: {
    async login({ commit }, { username, password }) {
      try {
        const response = await api.post('/user/login', { username, password }, {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          }
        })
        const tokenPair: TokenPair = response.data
        commit('setAccessToken', tokenPair.access_token)
      } catch (error: any) {
        console.error(error)
        throw error
      }
    },
    async register({ commit }, newUser: UserRegistration) {
      try {
        const response = await api.post('/user/register', newUser)
        const tokenPair: TokenPair = response.data
        commit('setAccessToken', tokenPair.access_token)
      } catch (error) {
        console.error(error)
        throw error
      }
    },
    logout({ commit }) {
      commit('clearUser')
    }
  }
})
