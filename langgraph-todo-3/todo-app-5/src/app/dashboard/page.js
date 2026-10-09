import { requireAuth } from "@/lib/auth";
import prisma from "@/lib/prisma";
// import Navbar from "@/components/navbar";
import { TaskStatusBadge } from "@/components/ui-components";
import { updateTaskStatus } from "@/lib/actions";
import { Button } from "@/components/ui/button";
import {
  Select,
  SelectTrigger,
  SelectValue,
  SelectContent,
  SelectItem,
} from "@/components/ui/select";

export default async function DashboardPage() {
  const user = await requireAuth();

  // Fetch tasks based on user role
  const tasks = await prisma.task.findMany({
    where: user.role === "ADMIN" ? {} : { assigneeId: user.id },
    include: {
      assignee: {
        select: {
          name: true,
          email: true,
        },
      },
    },
    orderBy: {
      updatedAt: "desc",
    },
  });

  return (
    <div>
      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <h1 className="text-2xl font-semibold text-gray-900">
            {user.role === "ADMIN" ? "All Tasks" : "My Tasks"}
          </h1>

          {tasks.length === 0 ? (
            <div className="mt-4 bg-white shadow overflow-hidden sm:rounded-lg p-6">
              <p className="text-gray-500">No tasks found.</p>
            </div>
          ) : (
            <div className="mt-4 bg-white shadow overflow-hidden sm:rounded-lg">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th
                      scope="col"
                      className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                    >
                      Title
                    </th>
                    <th
                      scope="col"
                      className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                    >
                      Status
                    </th>
                    {user.role === "ADMIN" && (
                      <th
                        scope="col"
                        className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                      >
                        Assigned To
                      </th>
                    )}
                    <th
                      scope="col"
                      className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                    >
                      Actions
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {tasks.map((task) => (
                    <tr key={task.id}>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm font-medium text-gray-900">
                          {task.title}
                        </div>
                        {task.description && (
                          <div className="text-sm text-gray-500">
                            {task.description}
                          </div>
                        )}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <TaskStatusBadge status={task.status} />
                      </td>
                      {user.role === "ADMIN" && (
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="text-sm text-gray-900">
                            {task.assignee ? task.assignee.name : "Unassigned"}
                          </div>
                          {task.assignee && (
                            <div className="text-sm text-gray-500">
                              {task.assignee.email}
                            </div>
                          )}
                        </td>
                      )}
                      <td className="px-6 py-4 whitespace-nowrap text-sm">
                        <form
                          action={updateTaskStatus}
                          className="flex items-center space-x-2"
                        >
                          <input type="hidden" name="id" value={task.id} />
                          <Select name="status" defaultValue={task.status}>
                            <SelectTrigger className="w-36">
                              <SelectValue placeholder="Select status" />
                            </SelectTrigger>
                            <SelectContent>
                              <SelectItem value="TODO">To Do</SelectItem>
                              <SelectItem value="IN_PROGRESS">
                                In Progress
                              </SelectItem>
                              <SelectItem value="COMPLETED">
                                Completed
                              </SelectItem>
                            </SelectContent>
                          </Select>
                          <Button
                            type="submit"
                            size="sm"
                            variant="default"
                            className="hover:text-cyan-500 hover:border-gray-300 cursor-pointer"
                          >
                            Update
                          </Button>
                        </form>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

// <td className="px-6 py-4 whitespace-nowrap text-sm">
//   <form action={updateTaskStatus}>
//     <input type="hidden" name="id" value={task.id} />
//     <select
//       name="status"
//       defaultValue={task.status}
//       className="mr-2 px-2 py-1 border rounded text-sm"
//     >
//       <option value="TODO">To Do</option>
//       <option value="IN_PROGRESS">In Progress</option>
//       <option value="COMPLETED">Completed</option>
//     </select>
//     <button
//       type="submit"
//       className="px-3 py-1 bg-blue-600 text-white rounded hover:bg-blue-700 text-sm"
//     >
//       Update
//     </button>
//   </form>
// </td>
