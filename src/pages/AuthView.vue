<template>
  <div class="home">
    <AuthForm />
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import AuthForm from '@/components/AuthForm.vue';

export default defineComponent({
  name: 'AuthView',
  components: {
    AuthForm
  },
});
</script>

<style scoped lang="scss">
.home {
  height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
}
</style>