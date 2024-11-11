type TaskStatus =
  | 'pending'
  | 'completed'

interface TaskStatusProps {
  status: TaskStatus
}

const taskStatusMap: Record<TaskStatus, string> = {
  pending: 'PENDENTE',
  completed: 'COMPLETED',
}

export function TaskStatus({ status }: TaskStatusProps) {
  return (
    <div className="flex items-center gap-2">
      {status === 'pending' && (
        <span className="h-2 w-2 rounded-full bg-slate-400" />
      )}

      {['completed', 'completed'].includes(status) && (
        <span className="h-2 w-2 rounded-full bg-amber-500" />
      )}

      <span className="font-medium text-muted-foreground">
        {taskStatusMap[status]}
      </span>
    </div>
  )
}