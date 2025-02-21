<template>
  <div
    class="task-card"
    v-if="task"
  >
    <h3 v-if="!isEditing">{{ task.name }}</h3>
    <input
      v-else
      type="text"
      v-model="editedTask.name"
      class="task-card__edit-input"
      placeholder="Название задачи"
    />

    <p v-if="!isEditing"><strong>Описание:</strong> {{ task.description }}</p>
    <div
      v-else
      class="task-card__edit-description"
    >
      <strong>Описание:</strong>
      <textarea
        v-model="editedTask.description"
        class="task-card__edit-textarea"
        placeholder="Описание задачи"
      ></textarea>
    </div>

    <p><strong>Дата:</strong> {{ formattedDate }}</p>

    <div class="task-card__buttons">
      <button
        @click="handleDeleteTask"
        class="task-card__delete-button"
      >Удалить</button>
      <button
        @click="toggleEdit"
        class="task-card__edit-button"
      >{{ isEditing ? 'Отмена' : 'Редактировать' }}</button>
      <button
        v-if="isEditing"
        @click="saveEditedTask"
        class="task-card__save-button"
      >Сохранить</button>
    </div>
  </div>
</template>
<script lang="ts">
import { defineComponent, ref, computed, reactive } from 'vue';
import { Task } from '@/interfaces/task';
import { useTask } from '@/composables';

export default defineComponent({
  name: 'TaskCard',
  props: {
    task: {
      type: Object as () => Task,
      required: true,
      validator: (value: any): boolean => {
        return value && typeof value === 'object' && 'name' in value && 'status' in value;
      }
    }
  },
  setup(props, { emit }) {
    const { deleteTask, updateTask } = useTask();
    const isEditing = ref(false);
    const editedTask = reactive({ ...props.task });

    const formattedDate = computed(() => {
      if (!props.task.date) return '';
      const date = new Date(props.task.date);
      const day = String(date.getDate()).padStart(2, '0');
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const year = date.getFullYear();
      const hours = String(date.getHours()).padStart(2, '0');
      const minutes = String(date.getMinutes()).padStart(2, '0');
      return `${day}.${month}.${year} ${hours}:${minutes}`;
    });

    const handleDeleteTask = async () => {
      try {
        await deleteTask(props.task.id);
        emit('task-deleted', props.task.id);
      } catch (error) {
        console.error('Failed to delete task:', error);
      }
    };

    const toggleEdit = () => {
      if (isEditing.value) {
        // Отмена редактирования
        editedTask.name = props.task.name;
        editedTask.description = props.task.description;
      }
      isEditing.value = !isEditing.value;
    };

    const saveEditedTask = async () => {
      try {
        await updateTask(props.task.id, editedTask);
        emit('task-updated', { ...editedTask });
        isEditing.value = false;
      } catch (error) {
        console.error('Failed to update task:', error);
      }
    };

    return {
      formattedDate,
      handleDeleteTask,
      isEditing,
      editedTask,
      toggleEdit,
      saveEditedTask
    };
  }
});
</script>

<style scoped lang="scss">
.task-card {
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 16px;
  background-color: #f9f9f9;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 350px;
  box-sizing: border-box;
  /* Ensure padding and border are included in the element's total width and height */

  &>h3 {
    margin-top: 0;
    font-size: 1.25rem;
  }

  &>p {
    margin: 8px 0;
    font-size: 0.9rem;
  }

  &__edit-input {
    width: 100%;
    padding: 8px;
    margin-bottom: 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
    font-size: 1rem;
    box-sizing: border-box;
    /* Ensure padding and border are included in the element's total width and height */
  }

  &__edit-description {
    margin: 8px 0;

    & strong {
      display: block;
      margin-bottom: 5px;
      font-size: 0.9rem;
    }

    & textarea {
      width: 100%;
      padding: 8px;
      margin-bottom: 10px;
      border: 1px solid #ccc;
      border-radius: 4px;
      font-size: 0.9rem;
      resize: vertical;
      min-height: 60px;
      box-sizing: border-box;
      /* Ensure padding and border are included in the element's total width and height */
    }
  }

  &__buttons {
    display: flex;
    justify-content: space-between;
  }

  &__delete-button {
    margin-top: 16px;
    padding: 8px 16px;
    font-size: 0.9rem;
    color: white;
    background-color: #dc3545; // Красный цвет для кнопки удаления
    border: none;
    border-radius: 4px;
    cursor: pointer;

    &:hover {
      background-color: #a71d2a;
    }
  }

  &__edit-button {
    margin-top: 16px;
    padding: 8px 16px;
    font-size: 0.9rem;
    color: white;
    background-color: #28a745; // Зеленый цвет для кнопки редактирования
    border: none;
    border-radius: 4px;
    cursor: pointer;

    &:hover {
      background-color: #218838;
    }
  }

  &__save-button {
    margin-top: 16px;
    padding: 8px 16px;
    font-size: 0.9rem;
    color: white;
    background-color: #007bff; // Синий цвет для кнопки сохранения
    border: none;
    border-radius: 4px;
    cursor: pointer;

    &:hover {
      background-color: #0056b3;
    }
  }
}
</style>
