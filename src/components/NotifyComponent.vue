<template>
  <transition name="fade">
    <div
      v-if="visible"
      :class="['notification', statusClass]"
      @click="close"
    >
      <p>{{ message }}</p>
    </div>
  </transition>
</template>

<script lang="ts">
import { defineComponent, ref, computed } from 'vue'

export default defineComponent({
  name: 'NotifyComponent',
  props: {
    message: {
      type: String,
      required: true,
    },
    status: {
      type: String,
      required: true,
      validator: (value: string) => {
        return ['success', 'negative'].includes(value)
      },
    },
  },
  setup(props) {
    const visible = ref(true)

    setTimeout(() => {
      visible.value = false
    }, 5000)

    const statusClass = computed(() => {
      return props.status === 'success' ? 'notification-success' : 'notification-negative'
    })

    const close = () => {
      visible.value = false
    }

    return {
      visible,
      statusClass,
      close,
    }
  },
})
</script>

<style scoped>
.notification {
  position: fixed;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  padding: 15px 20px;
  border-radius: 5px;
  color: white;
  z-index: 1000;
  cursor: pointer;
  transition: opacity 0.5s ease;
}

.notification-success {
  background-color: #4caf50;
}

.notification-negative {
  background-color: #f44336;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}

.fade-enter,
.fade-leave-to {
  opacity: 0;
}
</style>