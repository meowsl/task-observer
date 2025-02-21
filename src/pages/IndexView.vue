<template>
  <div class="task-list">
    <h1>Мои задачи</h1>
    <button
      @click="showModal = true"
      class="task-list__add-task-button"
    >
      Добавить задачу
    </button>
    <div class="task-list__content">
      <TaskCard
        v-for="task in localTaskList"
        :key="task.id"
        :task="task"
        @task-deleted="handleTaskDeleted"
        @task-updated="handleTaskUpdated"
      />
    </div>
    <teleport to="body">
      <div
        v-if="showModal"
        class="modal-overlay"
        @click="closeModal"
      >
        <div
          class="modal"
          @click.stop
        >
          <h2>Создание задачи</h2>
          <TaskCreateForm
            @task-created="handleTaskCreated"
            @cancel="closeModal"
          />
        </div>
      </div>
    </teleport>
  </div>
</template>

<script lang="ts">
import { ref, defineComponent, onMounted, nextTick } from 'vue';
import { Task } from '@/interfaces/task';
import { useTask } from '@/composables';
import TaskCard from '@/components/TaskCard.vue';
import TaskCreateForm from '@/components/TaskCreateForm.vue';

export default defineComponent({
  name: 'IndexView',
  components: {
    TaskCard,
    TaskCreateForm
  },
  setup() {
    const { getTaskList, createTask, deleteTask } = useTask();
    const localTaskList = ref<Task[]>([]);
    const showModal = ref(false);

    onMounted(async () => {
      try {
        const tasks = await getTaskList();
        localTaskList.value = tasks;
      } catch (error) {
        console.error('Failed to fetch task list:', error);
      }
    });

    const handleTaskCreated = async (newTask: Omit<Task, 'id' | 'date'>) => {
      try {
        const createdTask = await createTask(newTask);
        localTaskList.value.push(createdTask);
        closeModal();
      } catch (error) {
        console.error('Failed to create task:', error);
      }
    };

    const handleTaskDeleted = async (taskId: number) => {
      try {
        await deleteTask(taskId);
        localTaskList.value = localTaskList.value.filter(task => task.id !== taskId);

        await nextTick();
      } catch (error) {
        console.error('Failed to delete task:', error);
      }
    };

    const handleTaskUpdated = (updatedTask: Task) => {
      const index = localTaskList.value.findIndex(task => task.id === updatedTask.id);
      if (index !== -1) {
        localTaskList.value.splice(index, 1, updatedTask);
      }
    };

    const closeModal = () => {
      showModal.value = false;
    };

    return {
      localTaskList,
      showModal,
      handleTaskCreated,
      handleTaskDeleted,
      closeModal,
      handleTaskUpdated
    };
  }
});
</script>

<style scoped lang="scss">
.task-list {
  height: 100vh;
  padding: 0 5rem;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  box-sizing: border-box;

  &__content {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 1.5rem;
    margin-top: 16px;

    @media (min-width: 768px) {
      grid-template-columns: repeat(4, 1fr);
    }
  }

  &__add-task-button {
    margin-bottom: 16px;
    padding: 10px 20px;
    font-size: 1rem;
    width: 14rem;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;

    &:hover {
      background-color: #0056b3;
    }
  }
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal {
  background: white;
  padding: 20px;
  border-radius: 8px;
  width: 300px;
  max-width: 90%;
}
</style>