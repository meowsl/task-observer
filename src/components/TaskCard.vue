<template>
  <div
    class="task-card"
    v-if="task"
  >
    <div class="task-card__header">
      <select
        v-model="editedTask.status"
        @change="updateTaskStatus"
        class="task-card__status-select"
      >
        <option
          v-for="status in taskStatuses"
          :key="status"
          :value="status"
        >
          {{ status }}
        </option>
      </select>
    </div>
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

    const taskStatuses = [
      'Запланирована',
      'В процессе',
      'Завершена'
    ];

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

    const updateTaskStatus = async () => {
      try {
        const updatedTask = { ...editedTask, status: editedTask.status };
        await updateTask(props.task.id, updatedTask);
        emit('task-status-updated', { id: props.task.id, status: editedTask.status });
      } catch (error) {
        console.error('Failed to update task status:', error);
      }
    };

    return {
      formattedDate,
      handleDeleteTask,
      isEditing,
      editedTask,
      toggleEdit,
      saveEditedTask,
      taskStatuses,
      updateTaskStatus
    };
  }
});
</script>

<style scoped lang="scss">
.task-card {
  position: relative;
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 16px;
  background-color: #f9f9f9;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 350px;
  box-sizing: border-box;

  &>h3 {
    margin-top: 0;
    font-size: 1.25rem;
  }

  &>p {
    margin: 8px 0;
    font-size: 0.9rem;
  }

  &__header {
    position: absolute;
    top: 0;
    left: 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
  }

  &__status-select {
    padding: 8px;
    padding-right: 0;
    border: 1px solid #ccc;
    border-radius: 4px;
    font-size: 0.9rem;
    box-sizing: border-box;
  }

  &__edit-input {
    width: 100%;
    padding: 8px;
    margin-bottom: 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
    font-size: 1rem;
    box-sizing: border-box;
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
    background-color: #dc3545;
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
    background-color: #28a745;
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
    background-color: #007bff;
    border: none;
    border-radius: 4px;
    cursor: pointer;

    &:hover {
      background-color: #0056b3;
    }
  }
}
</style>