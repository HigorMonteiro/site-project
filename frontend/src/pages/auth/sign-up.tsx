import { Helmet } from 'react-helmet-async'
import { useForm } from 'react-hook-form'
import { Link, useNavigate } from 'react-router-dom'
import { Eye, EyeOff } from 'lucide-react'
import { toast } from 'sonner'
import { z } from 'zod'
import zxcvbn from 'zxcvbn'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { useState } from 'react'

const signUpForm = z
  .object({
    username: z.string(),
    email: z.string().email(),
  password1: z.string().min(6, 'A senha deve ter pelo menos 6 caracteres'),
  password2: z.string().min(6, 'A senha deve ter pelo menos 6 caracteres'),
  })
  .refine((data) => data.password1 === data.password2, {
    message: "As senhas não são iguais",
    path: ["password2"],
  })

type SignUpForm = z.infer<typeof signUpForm>


export function SignUp() {
  const navigate = useNavigate()
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
    watch
  } = useForm<SignUpForm>({
    resolver: async (data) => {
      try {
        signUpForm.parse(data)
        return { values: data, errors: {} }
      } catch (error) {
        return { values: {}, errors: (error as z.ZodError).formErrors.fieldErrors }
      }
    },
  })
  
  const [passwordStrength, setPasswordStrength] = useState(0)
  const [showPassword1, setShowPassword1] = useState(false)
  const [showPassword2, setShowPassword2] = useState(false)
  const password1 = watch('password1')
  const password2 = watch('password2')

  function PasswordStrengthMeter({ score }: { score: number }) {
  const strength = ['', '😟', '😐', '😊', '😃']
  const color = ['red', 'orange', 'yellow', 'green', 'green']
  const width = ['20%', '40%', '60%', '80%', '100%']
  
  return (
    <div className="flex items-center gap-1">
      <div className="w-full h-2 bg-gray-200 rounded-full">
        <div
          className={`h-2 bg-${color[score]}-500 rounded-full`}
          style={{ width: width[score] }}
        ></div>
      </div>
      <span className="flex ml-2 text-sm">{strength[score]}</span>
    </div>
  )
}
  function handlePasswordChange(password: string) {
    const result = zxcvbn(password)
    setPasswordStrength(result.score)
  }
  
  async function handleSignUp(data: SignUpForm) {
    if (data.password1 !== data.password2) {
      alert('As senhas não são iguais')
      return
    }
    try {
      console.log(data)
      await new Promise((resolve) => setTimeout(resolve, 2000))
      toast.success('Conta criada com sucesso! 🎉',
        {
          richColors: true,
          duration: 3000,
        action: {
          label: 'Login',
          onClick: () => navigate('/sign-in'),
        },
      })
    } catch (error) {
      toast.error('Algo deu errado. Tente novamente.')
    }
  }

  return (
    <>
      <Helmet title="Cadastro" />
      <div className="p-8 flex justify-center items-center min-h-screen">
        <Button variant="ghost" asChild className="absolute right-8 top-8">
          <Link to="/sign-in">Fazer login</Link>
        </Button>
        <div className="flex w-[350px] flex-col justify-center gap-6">
          <div className="flex flex-col gap-2 text-center">
            <h1 className="text-2xl font-semibold tracking-tight">
              Criar conta grátis
            </h1>
            <p className="text-sm text-muted-foreground">
              Organize suas tarefas e conquiste seus objetivos!
            </p>
          </div>
          <form className="space-y-4" onSubmit={handleSubmit(handleSignUp)}>
            <div className="space-y-2">
              <Label htmlFor="username">Seu nome</Label>
              <Input id="username" type="text" {...register('username')} />
              {errors.username && <p>{errors.username.message}</p>}
            </div>
            <div className="space-y-2">
              <Label htmlFor="email">Seu e-mail</Label>
              <Input id="email" type="email" {...register('email')} />
              {errors.email && <p>{errors.email.message}</p>}
            </div>
      <div className="space-y-2">
        <Label htmlFor="password1">Digite sua senha</Label>
        <div className="relative">
          <Input
            id="password1"
            type={showPassword1 ? 'text' : 'password'}
            {...register('password1')}
            onChange={(e) => handlePasswordChange(e.target.value)}
          />
          <button
            type="button"
            className="absolute inset-y-0 right-0 flex items-center px-2"
            onClick={() => setShowPassword1(!showPassword1)}
          >
            {showPassword1 ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
          </button>
        </div>
        {errors.password1 && <p>{errors.password1.message}</p>}
        <PasswordStrengthMeter score={passwordStrength} />
      </div>
      <div className="space-y-2">
        <Label htmlFor="password2">Digite novamente</Label>
        <div className="relative">
          <Input
            id="password2"
            type={showPassword2 ? 'text' : 'password'}
            {...register('password2')}
          />
          <button
            type="button"
            className="absolute inset-y-0 right-0 flex items-center px-2"
            onClick={() => setShowPassword2(!showPassword2)}
          >
            {showPassword2 ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
          </button>
        </div>
        {errors.password2 && <p>{errors.password2.message}</p>}
        {password1 && password2 && password1 !== password2 && (
          <p>As senhas não são iguais</p>
        )}
      </div>
            <Button disabled={isSubmitting} className="w-full" type="submit">
              Finalizar cadastro
            </Button>
            <p className="px-6 text-center text-sm leading-relaxed text-muted-foreground">
              Ao continuar, você concorda com nossos{' '}
              <a href="" className="underline underline-offset-4">
                termos de serviço
              </a>{' '}
              e{' '}
              <a href="" className="underline underline-offset-4">
                políticas de privacidade
              </a>
            </p>
          </form>
        </div>
      </div>
    </>
  )
}

