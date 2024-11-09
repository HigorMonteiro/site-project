import { Helmet } from 'react-helmet-async';

import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'

export function SignIn() {
    return (
      <>
        <Helmet title="Login" />
        <div className="p-8 flex justify-center items-center min-h-screen">
          <div className="flex w-full max-w-md flex-col justify-center gap-6">
            <div className="flex flex-col gap-2 text-center">
              <h1 className="text-2xl font-semibold tracking-tight">
                Organize sua Vida com Facilidade
              </h1>
              <p className="text-sm text-muted-foreground">
                Gerencie suas tarefas diárias com eficiência!
              </p>
            </div>
            <form className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="email">Seu e-mail</Label>
                <Input id="email" type="email" />
                <Label htmlFor="password">Sua senha</Label>
                <Input id="password" type="password" />
              </div>
              <Button className="w-full" type="submit">
                Acessar Lista
              </Button>
            </form>
          </div>
        </div>
      </>
    )
}