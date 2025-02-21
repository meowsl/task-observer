<template>
  <form @submit.prevent="handleSubmit">
    <div class="form-group">
      <label for="name">Название задачи:</label>
      <input
        id="name"
        type="text"
        v-model="newTask.name"
        required
        placeholder="Введите название задачи"
      />
    </div>

    <div class="form-group">
      <label for="description">Описание:</label>
      <textarea
        id="description"
        v-model="newTask.description"
        placeholder="Введите описание задачи"
      ></textarea>
    </div>

    <div class="form-actions">
      <button
        type="submit"
        class="submit-button"
      >Создать задачу</button>
      <button
        type="button"
        @click="cancel"
        class="cancel-button"
      >Отмена</button>
    </div>
  </form>
</template>

<script lang="ts">
import { defineComponent, reactive } from 'vue';
import { Task } from '@/interfaces/task';

export default defineComponent({
  name: 'TaskCreateForm',
  emits: ['task-created', 'cancel'],
  setup(_, { emit }) {
    const newTask = reactive<Omit<Task, 'id' | 'date'>>({
      name: '',
      description: '',
      status: ''
    });

    const handleSubmit = () => {
      if (newTask.name.trim()) {
        emit('task-created', { ...newTask });
        resetForm();
      } else {
        alert('Пожалуйста, введите название задачи.');
      }
    };

    const cancel = () => {
      emit('cancel');
      resetForm();
    };

    const resetForm = () => {
      newTask.name = '';
      newTask.description = '';
    };

    return {
      newTask,
      handleSubmit,
      cancel
    };
  }
});
</script>

<style scoped lang="scss">
.form-group {
  margin-bottom: 16px;
  padding: 12px;

  label {
    display: block;
    margin-bottom: 8px;
    font-weight: bold;
  }

  input,
  textarea {
    width: 100%;
    padding: 8px;
    border: 1px solid #ccc;
    border-radius: 4px;
    font-size: 1rem;

    &:focus {
      outline: none;
      border-color: #007bff;
    }
  }

  textarea {
    resize: vertical;
    min-height: 80px;
  }
}

.form-actions {
  display: flex;
  justify-content: space-between;

  .submit-button,
  .cancel-button {
    padding: 10px 20px;
    font-size: 1rem;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }

  .submit-button {
    background-color: #28a745;
    color: white;

    &:hover {
      background-color: #1e7e34;
    }
  }

  .cancel-button {
    background-color: #6c757d;
    color: white;

    &:hover {
      background-color: #5a6268;
    }
  }
}
</style>