import { formatDistanceToNow } from 'date-fns'
import { ptBR } from 'date-fns/locale'
import { ArrowRight, Search, X } from 'lucide-react'

import { TaskStatus } from '@/components/task-status'
import { Button } from '@/components/ui/button'
import { Dialog, DialogTrigger } from '@/components/ui/dialog'
import { TableCell, TableRow } from '@/components/ui/table'

import { TaskDetails } from './task-details'


interface Task {
    task: {
        id: number;
        title: string;
        description: string;
        created_at: string;
        updated_at: string;
        due_date: string | null;
        status: string;
        owner: number;
        category: number | null;
        shared_with: {
            id: number;
            username: string;
        }[];
    }
}


export function TaskTableRow({task}: Task) {
  console.log("objetos: ", task)
  return (
    <TableRow>
      <TableCell>
        <Dialog>
          <DialogTrigger asChild>
            <Button variant="outline" size="xs">
              <Search className="h-3 w-3" />
              <span className="sr-only">Detalhes da tarefa</span>
            </Button>
          </DialogTrigger>

          <TaskDetails />
        </Dialog>
      </TableCell>
      <TableCell className="font-mono text-xs font-medium">
        {task.id}
      </TableCell>
      <TableCell className="text-muted-foreground">
        {formatDistanceToNow(task.created_at, {
          locale: ptBR,
          addSuffix: true,
        })}
      </TableCell>
      <TableCell>
        {task.status === 'PENDING' ? (
          <TaskStatus status="pending" />
        ) : (
          <TaskStatus status="completed" />)}
      </TableCell>
      <TableCell className="font-medium ">{task.title}</TableCell>
      <TableCell className='text-xs'>
       {task.shared_with.map((shared) => shared.username).join(', ')}
      </TableCell>
    </TableRow>
  )
}