<template>
  <form
    v-if="isLogin"
    class="auth-form login"
  >
    <h2>Вход</h2>
    <input
      class="auth-form__input"
      v-model="username"
      type="text"
      placeholder="Логин"
    />
    <input
      class="auth-form__input"
      v-model="password"
      type="password"
      placeholder="Пароль"
    />
    <button
      class="auth-form__submit-btn"
      type="submit"
    >Войти</button>
  </form>
  <form
    v-else
    class="auth-form registration"
  >
    <h2>Регистрация</h2>
    <input
      class="auth-form__input"
      v-model="firstname"
      type="text"
      placeholder="Ваше имя"
    />
    <input
      class="auth-form__input"
      v-model="username"
      type="text"
      placeholder="Логин"
    />
    <input
      class="auth-form__input"
      v-model="password"
      type="password"
      placeholder="Пароль"
    />
    <input
      class="auth-form__input"
      v-model="passwordConfirm"
      type="password"
      placeholder="Подтверждение пароля"
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
    {{ isLogin ? 'Перейти к регистрации' : 'Перейти к входу' }}
  </button>
</template>

<script lang="ts">
import { ref, defineComponent } from 'vue'

export default defineComponent({
  name: 'AuthForm',
  setup() {
    const isLogin = ref<boolean>(true)
    const username = ref<string>('')
    const firstname = ref<string>('')
    const password = ref<string>('')
    const passwordConfirm = ref<string>('')

    const toggleForm = () => {
      isLogin.value = !isLogin.value
    }

    return {
      isLogin,
      username,
      firstname,
      password,
      passwordConfirm,
      toggleForm
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
  max-width: 400px;
  margin: 0 auto;

  &__input {
    margin: 8px auto;
    width: 15rem;
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
    margin-top: 12px;
    width: 15rem;
    padding: 12px;

    border-radius: 24px;
    border: none !important;
    background: linear-gradient(135deg, rgba(5, 31, 32, 1) 0%, rgba(11, 73, 63, 1) 100%);
    color: #f0f0f0;
  }

  &__toggle-form {
    margin-top: 12px;
  }
}
</style>