import { api } from '@/lib/axios'

export interface SignInBody {
	email: string
	password: string
    
}

export async function signIn({ email, password }: SignInBody) {
	const response = await api.post('/auth/login/', { email, password });
	const token = response.data.token;
	return token;
}
