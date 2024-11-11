
import { api } from '@/lib/axios'

interface Task {
  task: {
    id: number;
    title: string;
    description: string;
    created_at: string;
    updated_at: string;
    due_date: string | null;
    status: 'PENDING' | 'COMPLETED';
    owner: number;
    category: number | null;
    shared_with: {
      id: number;
      username: string;
    }[];
  }
}

interface TaskResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: Task[];
}

export async function getTasks() {
  const response = await api.get<TaskResponse>('/tasks/', {
    params: {
      page: 1,
    },
  })
  return response.data
}