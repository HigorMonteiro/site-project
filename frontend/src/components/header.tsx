import { useQuery } from '@tanstack/react-query'
import { getProfile } from '@/api/get-profile'

import { ListCheck, Home, Share2, User } from 'lucide-react'
import { NavLink } from './nav-link'
import { Separator } from './ui/separator'

export function Header() {
  const { data: profile } = useQuery({
    queryKey: ['profile'],
    queryFn: getProfile,
  })
  return (
    <div className="border-b">
        <div className="flex h-16 items-center justify-center gap-6 px-6">
          <Home className="h-6 w-6" />
          <Separator orientation="vertical" className="h-6" />
          <nav className="flex items-center space-x-4 lg:space-x-6">
              <NavLink to="/">
                  <ListCheck className="h-4 w-4" />
                  Início
              </NavLink>
              <NavLink to="/">
                  <Share2 className="h-4 w-4" />
                  Tarefas
            </NavLink>
          <NavLink to="/">
              <User className="h-4 w-4" />
              {profile?.username}
            </NavLink>
                </nav>
            </div>
        </div>
    )
}