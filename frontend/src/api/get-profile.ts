import { api } from '@/lib/axios'
interface GetProfileResponse {
  id: string
  username: string
  email: string
}
export async function getProfile() {
  const response = await api.get<GetProfileResponse>('/auth/user/')
  return response.data
}