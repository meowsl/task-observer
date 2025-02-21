import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { useAuthStore } from './store'

createApp(App).use(useAuthStore).use(router).mount('#app')
