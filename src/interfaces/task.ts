export interface Task {
  readonly id: number
  name: string
  description?: string
  date: Date
  status: string
}