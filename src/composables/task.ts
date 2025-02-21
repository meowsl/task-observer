import { api } from "@/boot/axios"
import { getAuthToken  } from "."
import { Task } from "@/interfaces/task"

export function useTask() {

  const getTaskList = async () => {
    const response = await api.get('task/list', {
      headers: {
        'Authorization': getAuthToken()
      }
    })
    return response.data
  }

  const createTask = async(newTask: Omit<Task, "id" | "date">) => {
    const response = await api.post('task/create', newTask, {
      headers: {
        'Authorization': getAuthToken()
      }
    })

    return response.data
  }

  const deleteTask = async (taskId: number) => {
    await api.delete(`task/${taskId}`, {
      headers: {
        'Authorization': getAuthToken()
      }
    })
  }

  const updateTask = async (taskId: number, newTask: Omit<Task, "id" | "date">) => {
    const response = await api.patch(`task/${taskId}`, newTask, {
      headers: {
        'Authorization': getAuthToken()
      }
    })
    return response.data
  }

  return {
    getTaskList,
    createTask,
    deleteTask,
    updateTask
  }
}