import { ListCheck  } from 'lucide-react'
import { Outlet } from 'react-router-dom'

export function AuthLayout() {
    return (
      <div className="lg:min-h-screen grid grid-cols-1 lg:grid-cols-2 antialiased">
      <div className="flex h-full flex-col justify-between border-r border-foreground/5 bg-muted p-10 text-muted-foreground">
        <div className="flex items-center gap-3 text-lg text-foreground">
          <ListCheck className="h-5 w-5" />
          <span className="font-semibold">ToDo-List</span>
        </div>

        <footer className="text-sm hidden lg:block">
          Sua lista &copy; ToDo-List - {new Date().getFullYear()}
        </footer>
      </div>

      <div className="flex flex-col items-center justify-center">
        <Outlet />
      </div>
    </div>
  )
}