<template>
  <div class="home">
    <AuthForm />
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import AuthForm from '@/components/AuthForm.vue';

export default defineComponent({
  name: 'HomeView',
  components: {
    AuthForm
  },
});
</script>
