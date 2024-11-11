import { useQuery } from '@tanstack/react-query'
import { Helmet } from 'react-helmet-async'

import { Pagination } from '@/components/pagination'
import {
  Table,
  TableBody,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'

import { OrderTableFilters } from './task-table-filters'
import { TaskTableRow } from './task-table-row'
import { getTasks } from '@/api/get-tasks'

export function Tasks() {

  const { data: tasks } = useQuery({
    queryKey: ['tasks'],
    queryFn: getTasks,
    staleTime: Infinity,
  })
    const url = tasks?.next;
    const urlParams = url ? new URLSearchParams(url.split('?')[1]) : null;
    const page = urlParams ? urlParams.get('page') : null;
  console.log("Table task:", tasks)
  return (
      <>
          
      <Helmet title="Tarefas" />
      <div className="flex flex-col gap-4">
        <h1 className="text-3xl font-bold tracking-tight">Tarefas</h1>
        <div className="space-y-2.5">
          <OrderTableFilters />

          <div className="rounded-md border">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead className="w-[64px]"></TableHead>
                  <TableHead className="w-[140px]">Identificador</TableHead>
                  <TableHead className="w-[180px]">Criada há</TableHead>
                  <TableHead className="w-[140px]">Status</TableHead>
                  <TableHead>Titulo</TableHead>
                  <TableHead className="w-[190px]">Total do tarefa</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {tasks &&
                  tasks?.results.map((task) => {
                    return <TaskTableRow key={task?.id} task={task} />
                  })}
              </TableBody>
            </Table>
          </div>
            
          <Pagination pageIndex={0} totalCount={tasks?.count || 0} perPage={10} />
        </div>
      </div>
    </>
  )
}