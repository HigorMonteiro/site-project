import { api } from '@/lib/axios'

export interface SignUpBody {
	email: string,
	first_name: string,
	password1: string,
	password2: string,
    
}

export async function signUp({ email, first_name, password1, password2 }: SignUpBody) {
	const response = await api.post('/auth/registration/', { email, first_name, password1, password2 });
	const token = response.status;
	return token;
}
