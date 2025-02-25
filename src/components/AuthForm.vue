<template>
  <NotifyComponent
    v-if="showNotification"
    :message="notificationMessage"
    :status="notificationStatus"
  />
  <form
    v-if="isLogin"
    class="auth-form login"
    @submit.prevent="handleLogin"
  >
    <h2 class="auto-form__title">Вход</h2>
    <input
      class="auth-form__input"
      v-model="username"
      type="text"
      placeholder="Логин"
      required
    />
    <input
      class="auth-form__input"
      v-model="password"
      type="password"
      placeholder="Пароль"
      required
    />
    <button
      class="auth-form__submit-btn"
      type="submit"
    >
      Войти
    </button>
  </form>
  <form
    v-else
    class="auth-form registration"
    @submit.prevent="handleRegistration"
  >
    <h2 class="auto-form__title">Регистрация</h2>
    <input
      class="auth-form__input"
      v-model="firstname"
      type="text"
      placeholder="Ваше имя"
      required
    />
    <input
      class="auth-form__input"
      v-model="username"
      type="text"
      placeholder="Логин"
      required
    />
    <input
      class="auth-form__input"
      v-model="password"
      type="password"
      placeholder="Пароль"
      required
    />
    <input
      class="auth-form__input"
      v-model="passwordConfirm"
      type="password"
      placeholder="Подтверждение пароля"
      required
    />
    <button
      class="auth-form__submit-btn"
      type="submit"
    >Зарегистрироваться</button>
  </form>
  <button
    class="auth-form__toggle-form"
    @click="toggleForm"
  >
    {{ isLogin ? 'Регистрация' : 'Уже зарегистрированы?' }}
  </button>
</template>

<script lang="ts">
import { UserRegistration } from '@/interfaces/user'
import { ref, defineComponent } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import NotifyComponent from '@/components/NotifyComponent.vue'

export default defineComponent({
  name: 'AuthForm',
  components: {
    NotifyComponent
  },
  setup() {
    const store = useStore()
    const router = useRouter()
    const isLogin = ref<boolean>(true)
    const username = ref<string>('')
    const firstname = ref<string>('')
    const password = ref<string>('')
    const passwordConfirm = ref<string>('')

    const notificationMessage = ref<string>('')
    const notificationStatus = ref<string>('success')
    const showNotification = ref<boolean>(false)

    const toggleForm = () => {
      isLogin.value = !isLogin.value
    }

    const handleLogin = async () => {
      try {
        await store.dispatch('login', { username: username.value, password: password.value })
        router.push('/')
      } catch (error: any) {
        console.error('Ошибка входа:', error.detail)
        notificationMessage.value = 'Ошибка входа: ' + error.detail
        notificationStatus.value = 'negative'
        showNotification.value = true
      }
    }

    const handleRegistration = async () => {
      try {
        const userData: UserRegistration = {
          username: username.value,
          firstname: firstname.value,
          password: password.value,
          password_confirm: passwordConfirm.value
        }
        await store.dispatch('register', userData)
        router.push('/')
      } catch (error: any) {
        console.error('Ошибка регистрации:', error.detail)
        notificationMessage.value = 'Ошибка регистрации: ' + error.detail
        notificationStatus.value = 'negative'
        showNotification.value = true
      }
    }

    return {
      isLogin,
      username,
      firstname,
      password,
      passwordConfirm,
      toggleForm,
      handleLogin,
      handleRegistration,
      notificationMessage,
      notificationStatus,
      showNotification
    }
  }
})
</script>


<style scoped lang="scss">
.auth-form {
  display: flex;
  flex-direction: column;
  align-items: center;
  color: black;
  // max-width: 400px;
  margin: 0 auto;
  padding: 32px;
  padding-top: 0px;
  background-color: #f8f8f8;
  border-radius: 24px;
  box-shadow: 0px 0px 10px -4px rgba(129, 129, 129, 0.2);

  &__input {
    margin: 12px auto;
    width: 20rem;
    height: 2rem;
    border-radius: 60px;
    border: 2px solid transparent;
    background-color: #DAF1DE;
    padding: 6px 12px;
    transition: border-color 0.5s ease;

    &:focus {
      outline: none;
      border-color: #8EB69B;
    }

    &::placeholder {
      color: #0b2b26;
      opacity: 0.5;
      font-weight: 600;
    }
  }

  &__submit-btn {
    cursor: pointer;
    margin-top: 12px;
    width: 10rem;
    padding: 12px;

    border-radius: 24px;
    border: none !important;
    background: linear-gradient(135deg, rgba(5, 31, 32, 1) 0%, rgba(11, 73, 63, 1) 100%);
    color: #f0f0f0;
  }

  &__toggle-form {
    cursor: pointer;
    margin-top: 12px;
    background-color: transparent;
    border: none;
    color: #375534;
    font-weight: 600;
  }
}
</style>