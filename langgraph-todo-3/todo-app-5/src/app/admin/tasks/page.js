"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useMemo } from "react";

import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from "@/components/ui/dialog";
import {
  Form,
  FormField,
  FormItem,
  FormLabel,
  FormControl,
  FormMessage,
} from "@/components/ui/form";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  createTask,
  getTasks,
  updateTask,
  deleteTask,
  fetchCurrentUser,
  fetchTasksFromAPI,
  getUsers,
} from "@/lib/actions";
import {
  DeleteConfirmation,
  TaskStatusBadge,
} from "@/components/ui-components";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { useCopilotAction, useCopilotReadable } from "@copilotkit/react-core";

const taskSchema = z.object({
  title: z.string().min(2, "Title is too short"),
  description: z.string().optional(),
  status: z.enum(["TODO", "IN_PROGRESS", "COMPLETED"]),
  assigneeId: z.string().min(1, "Please assign a user"),
});

const updateTaskSchema = taskSchema.extend({
  id: z.string(),
});

export default function TasksPage() {
  const router = useRouter();
  const [tasks, setTasks] = useState([]);
  const [users, setUsers] = useState([]);
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);
  const [currentTask, setCurrentTask] = useState(null);
  const [isDeleting, setIsDeleting] = useState(false);

  const createForm = useForm({
    resolver: zodResolver(taskSchema),
    defaultValues: {
      title: "",
      description: "",
      status: "TODO",
      assigneeId: "",
    },
  });

  const editForm = useForm({
    resolver: zodResolver(updateTaskSchema),
    defaultValues: {
      id: "",
      title: "",
      description: "",
      status: "TODO",
      assigneeId: "",
    },
  });

  useEffect(() => {
    async function fetchData() {
      try {
        const userData = await fetchCurrentUser();
        if (!userData) {
          router.push("/login");
          return;
        }
        setUser(userData);
        if (userData.role !== "ADMIN") {
          router.push("/dashboard");
          return;
        }

        // const tasksRes = await getTasks();
        const tasksRes = await fetchTasksFromAPI();

        if (tasksRes.error) throw new Error(tasksRes.error);
        setTasks(tasksRes.tasks);

        const usersRes = await getUsers();
        if (usersRes.error) throw new Error(usersRes.error);
        setUsers(usersRes.users.filter((u) => u.role === "USER"));
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }

    fetchData();
  }, [router]);

  const taskSnapshot = useMemo(() => JSON.stringify(tasks), [tasks]);

  useCopilotReadable({
    name: "taskList",
    description: "List of tasks with title, status, description, and assignee",
    value: taskSnapshot,
  });

  useCopilotAction({
    name: "createTask",
    description:
      "Create a new task with title, description, status, and assigneeId",
    parameters: [
      { name: "title", type: "string", required: true },
      { name: "description", type: "string" },
      {
        name: "status",
        type: "string",
        enum: ["TODO", "IN_PROGRESS", "COMPLETED"],
      },
      { name: "assigneeId", type: "string", required: true },
    ],
    handler: async ({ title, description, status, assigneeId }) => {
      await handleCreateTask({ title, description, status, assigneeId });
      return `Task "${title}" created successfully.`;
    },
  });

  useCopilotAction({
    name: "updateTask",
    description:
      "Update a task by ID with new title, description, status, and assigneeId",
    parameters: [
      { name: "id", type: "string", required: true },
      { name: "title", type: "string" },
      { name: "description", type: "string" },
      {
        name: "status",
        type: "string",
        enum: ["TODO", "IN_PROGRESS", "COMPLETED"],
      },
      { name: "assigneeId", type: "string" },
    ],
    handler: async ({ id, title, description, status, assigneeId }) => {
      await handleUpdateTask({ id, title, description, status, assigneeId });
      return `Task with ID ${id} updated successfully.`;
    },
  });

  useCopilotAction({
    name: "deleteTask",
    description: "Delete a task by ID",
    parameters: [{ name: "id", type: "string", required: true }],
    handler: async ({ id }) => {
      await handleDeleteTask(id);
      return `Task with ID ${id} deleted.`;
    },
  });

  const handleCreateTask = async (data) => {
    try {
      const result = await createTask(data);
      if (result.error) {
        createForm.setError("root", { message: result.error });
        return;
      }
      // const updated = await getTasks();
      const updated = await fetchTasksFromAPI();
      setTasks(updated.tasks);
      createForm.reset();
      setIsCreateModalOpen(false);
    } catch (err) {
      createForm.setError("root", { message: err.message });
    }
  };

  const handleUpdateTask = async (data) => {
    try {
      const result = await updateTask(data);
      if (result.error) {
        editForm.setError("root", { message: result.error });
        return;
      }
      // const updated = await getTasks();
      const updated = await fetchTasksFromAPI();

      setTasks(updated.tasks);
      editForm.reset();
      setIsEditModalOpen(false);
    } catch (err) {
      editForm.setError("root", { message: err.message });
    }
  };

  const handleDeleteTask = async (taskId) => {
    setIsDeleting(true);
    try {
      const result = await deleteTask(taskId);
      if (result.error) {
        setError(result.error);
        return;
      }
      setTasks((prev) => prev.filter((t) => t.id !== taskId));
      setIsDeleteModalOpen(false);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsDeleting(false);
    }
  };

  const openEditModal = (task) => {
    editForm.reset({ ...task });
    setCurrentTask(task);
    setIsEditModalOpen(true);
  };

  return (
    <div>
      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <div className="flex justify-between items-center">
            <h1 className="text-2xl font-semibold text-gray-900">
              Manage Tasks
            </h1>
            <Button
              className="cursor-pointer"
              onClick={() => setIsCreateModalOpen(true)}
            >
              Add Task
            </Button>
          </div>
          {error && <p className="text-red-500 mt-2">{error}</p>}
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
                    Description
                  </th>
                  <th
                    scope="col"
                    className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                  >
                    Status
                  </th>
                  <th
                    scope="col"
                    className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                  >
                    Assigned To
                  </th>
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
                    <td className="px-6 py-4">{task.title}</td>
                    <td className="px-6 py-4">
                      {task.description || "No description"}
                    </td>
                    <td className="px-6 py-4">
                      <TaskStatusBadge status={task.status} />
                    </td>
                    <td className="px-6 py-4">
                      {task.assignee?.name || "Unassigned"}
                    </td>
                    <td className="px-6 py-4 flex gap-2">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => openEditModal(task)}
                        className="cursor-pointer"
                      >
                        Edit
                      </Button>
                      <Button
                        variant="destructive"
                        className="cursor-pointer"
                        size="sm"
                        onClick={() => {
                          setCurrentTask(task);
                          setIsDeleteModalOpen(true);
                        }}
                      >
                        Delete
                      </Button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </main>

      {/* Create Task Modal */}
      <Dialog open={isCreateModalOpen} onOpenChange={setIsCreateModalOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Create Task</DialogTitle>
          </DialogHeader>
          <Form {...createForm}>
            <form
              onSubmit={createForm.handleSubmit(handleCreateTask)}
              className="space-y-4"
            >
              {/* Title */}
              <FormField
                control={createForm.control}
                name="title"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Title</FormLabel>
                    <FormControl>
                      <Input {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              {/* Description */}
              <FormField
                control={createForm.control}
                name="description"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Description</FormLabel>
                    <FormControl>
                      <Input {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              {/* Status */}
              <FormField
                control={createForm.control}
                name="status"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Status</FormLabel>
                    <Select value={field.value} onValueChange={field.onChange}>
                      <FormControl>
                        <SelectTrigger>
                          <SelectValue placeholder="Select status" />
                        </SelectTrigger>
                      </FormControl>
                      <SelectContent>
                        <SelectItem value="TODO">Todo</SelectItem>
                        <SelectItem value="IN_PROGRESS">In Progress</SelectItem>
                        <SelectItem value="COMPLETED">Completed</SelectItem>
                      </SelectContent>
                    </Select>
                    <FormMessage />
                  </FormItem>
                )}
              />
              {/* Assignee */}
              <FormField
                control={createForm.control}
                name="assigneeId"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Assign To</FormLabel>
                    <Select value={field.value} onValueChange={field.onChange}>
                      <FormControl>
                        <SelectTrigger>
                          <SelectValue placeholder="Select user" />
                        </SelectTrigger>
                      </FormControl>
                      <SelectContent>
                        {users.map((u) => (
                          <SelectItem key={u.id} value={u.id}>
                            {u.name}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <DialogFooter>
                <Button type="submit" className="cursor-pointer">
                  Create Task
                </Button>
              </DialogFooter>
            </form>
          </Form>
        </DialogContent>
      </Dialog>

      {/* Edit Task Modal */}
      <Dialog open={isEditModalOpen} onOpenChange={setIsEditModalOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Edit Task</DialogTitle>
          </DialogHeader>
          <Form {...editForm}>
            <form
              onSubmit={editForm.handleSubmit(handleUpdateTask)}
              className="space-y-4"
            >
              {/* Same fields as Create */}
              <FormField
                control={editForm.control}
                name="title"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Title</FormLabel>
                    <FormControl>
                      <Input {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={editForm.control}
                name="description"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Description</FormLabel>
                    <FormControl>
                      <Input {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={editForm.control}
                name="status"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Status</FormLabel>
                    <Select value={field.value} onValueChange={field.onChange}>
                      <FormControl>
                        <SelectTrigger>
                          <SelectValue placeholder="Select status" />
                        </SelectTrigger>
                      </FormControl>
                      <SelectContent>
                        <SelectItem value="TODO">Todo</SelectItem>
                        <SelectItem value="IN_PROGRESS">In Progress</SelectItem>
                        <SelectItem value="COMPLETED">Completed</SelectItem>
                      </SelectContent>
                    </Select>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={editForm.control}
                name="assigneeId"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Assign To</FormLabel>
                    <Select value={field.value} onValueChange={field.onChange}>
                      <FormControl>
                        <SelectTrigger>
                          <SelectValue placeholder="Select user" />
                        </SelectTrigger>
                      </FormControl>
                      <SelectContent>
                        {users.map((u) => (
                          <SelectItem key={u.id} value={u.id}>
                            {u.name}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <DialogFooter>
                <Button type="submit" className="cursor-pointer">
                  Update Task
                </Button>
              </DialogFooter>
            </form>
          </Form>
        </DialogContent>
      </Dialog>

      {/* Delete Confirmation Modal */}
      <Dialog open={isDeleteModalOpen} onOpenChange={setIsDeleteModalOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Delete Task</DialogTitle>
          </DialogHeader>
          {currentTask && (
            <DeleteConfirmation
              onConfirm={() => handleDeleteTask(currentTask.id)}
              onCancel={() => setIsDeleteModalOpen(false)}
              isDeleting={isDeleting}
            />
          )}
        </DialogContent>
      </Dialog>
    </div>
  );
}

// "use client";

// import { useEffect, useState } from "react";
// import { useRouter } from "next/navigation";
// import Navbar from "@/components/navbar";
// import { Button } from "@/components/ui/button";
// import { Progress } from "@/components/ui/progress";
// // import { getSession } from "./auth";
// import {
//   Dialog,
//   DialogContent,
//   DialogHeader,
//   DialogTitle,
//   DialogFooter,
// } from "@/components/ui/dialog";

// import {
//   createTask,
//   getTasks,
//   updateTask,
//   updateTaskStatus,
//   deleteTask,
//   fetchCurrentUser,
//   getUsers,
// } from "@/lib/actions";

// import {
//   Modal,
//   TaskForm,
//   DeleteConfirmation,
//   TaskStatusBadge,
// } from "@/components/ui-components";

// export default function TasksPage() {
//   const router = useRouter();
//   const [tasks, setTasks] = useState([]);
//   const [users, setUsers] = useState([]);
//   const [user, setUser] = useState(null);
//   const [loading, setLoading] = useState(true);
//   const [error, setError] = useState(null);
//   const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
//   const [isEditModalOpen, setIsEditModalOpen] = useState(false);
//   const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);
//   const [currentTask, setCurrentTask] = useState(null);
//   const [formState, setFormState] = useState(null);
//   const [isDeleting, setIsDeleting] = useState(false);

//   useEffect(() => {
//     async function fetchData() {
//       try {
//         const userData = await fetchCurrentUser();
//         if (!userData) {
//           router.push("/login");
//           return;
//         }

//         setUser(userData);

//         if (userData.role !== "ADMIN") {
//           router.push("/dashboard");
//           return;
//         }

//         const tasksRes = await getTasks();
//         if (tasksRes.error) throw new Error(tasksRes.error);
//         setTasks(tasksRes.tasks);

//         const usersRes = await getUsers();
//         if (usersRes.error) throw new Error(usersRes.error);
//         const onlyUsers = usersRes.users.filter((u) => u.role === "USER");
//         setUsers(onlyUsers);
//       } catch (err) {
//         setError(err.message);
//       } finally {
//         setLoading(false);
//       }
//     }

//     fetchData();
//   }, [router]);

//   // useEffect(() => {
//   //   async function fetchData() {
//   //     try {
//   //       // Fetch current user
//   //       const userRes = await fetch("/api/auth/me");
//   //       if (!userRes.ok) {
//   //         if (userRes.status === 401) {
//   //           router.push("/login");
//   //           return;
//   //         }
//   //         throw new Error("Failed to fetch user");
//   //       }
//   //       const userData = await userRes.json();
//   //       setUser(userData);

//   //       // Check if user is admin
//   //       if (userData.role !== "ADMIN") {
//   //         router.push("/dashboard");
//   //         return;
//   //       }

//   //       // Fetch tasks
//   //       const tasksRes = await fetch("/api/tasks");
//   //       if (!tasksRes.ok) throw new Error("Failed to fetch tasks");
//   //       const tasksData = await tasksRes.json();
//   //       setTasks(tasksData);

//   //       // Fetch users (for assignment)
//   //       const usersRes = await fetch("/api/users");
//   //       if (!usersRes.ok) throw new Error("Failed to fetch users");
//   //       const usersData = await usersRes.json();
//   //       setUsers(usersData.filter((user) => user.role === "USER"));
//   //     } catch (err) {
//   //       setError(err.message);
//   //     } finally {
//   //       setLoading(false);
//   //     }
//   //   }

//   //   fetchData();
//   // }, [router]);

//   const handleCreateTask = async (formData) => {
//     try {
//       setFormState({ pending: true });

//       // Call server action directly
//       const result = await createTask(formData);

//       if (result.error) {
//         setFormState({ error: result.error });
//         return;
//       }

//       setFormState({ success: result.success });

//       // Refresh tasks list (you can re-fetch or update UI manually)
//       const updated = await getTasks(); // If you have a server action for fetching
//       setTasks(updated.tasks); // Or update via props/state if passed in

//       // Close modal after a delay
//       setTimeout(() => {
//         setIsCreateModalOpen(false);
//         setFormState(null);
//       }, 1500);
//     } catch (err) {
//       setFormState({ error: err.message || "An error occurred" });
//     }
//   };

//   const handleUpdateTask = async (formData) => {
//     try {
//       setFormState({ pending: true });

//       const result = await updateTask(formData);

//       if (result.error) {
//         setFormState({ error: result.error });
//         return;
//       }

//       setFormState({ success: result.success });

//       // Refresh tasks list
//       const updated = await getTasks(); // Also from server actions
//       if (updated.error) {
//         setFormState({ error: updated.error });
//         return;
//       }

//       setTasks(updated.tasks);

//       // Close modal after a delay
//       setTimeout(() => {
//         setIsEditModalOpen(false);
//         setFormState(null);
//       }, 1500);
//     } catch (err) {
//       setFormState({ error: err.message || "An error occurred" });
//     }
//   };

//   // const handleUpdateTask = async (formData) => {
//   //   try {
//   //     setFormState({ pending: true });

//   //     const res = await fetch(`/api/tasks/${formData.id}`, {
//   //       method: "PUT",
//   //       headers: {
//   //         "Content-Type": "application/json",
//   //       },
//   //       body: JSON.stringify(formData),
//   //     });

//   //     const data = await res.json();

//   //     if (!res.ok) {
//   //       setFormState({ error: data.error || "Failed to update task" });
//   //       return;
//   //     }

//   //     setFormState({ success: "Task updated successfully" });

//   //     // Refresh tasks list
//   //     const tasksRes = await fetch("/api/tasks");
//   //     const tasksData = await tasksRes.json();
//   //     setTasks(tasksData);

//   //     // Close modal after a delay
//   //     setTimeout(() => {
//   //       setIsEditModalOpen(false);
//   //       setFormState(null);
//   //     }, 1500);
//   //   } catch (err) {
//   //     setFormState({ error: err.message || "An error occurred" });
//   //   }
//   // };

//   // ✅ In your client component

//   async function handleDeleteTask(taskId) {
//     setIsDeleting(true);
//     setError(null);

//     try {
//       const result = await deleteTask(taskId); // server action

//       if (result.error) {
//         setError(result.error);
//         return;
//       }

//       setTasks((prevTasks) => prevTasks.filter((task) => task.id !== taskId));
//       setIsDeleteModalOpen(false);
//     } catch (err) {
//       setError(err.message || "An unexpected error occurred");
//     } finally {
//       setIsDeleting(false);
//     }
//   }

//   // const handleDeleteTask = async () => {
//   //   try {
//   //     setIsDeleting(true);

//   //     const res = await fetch(`/api/tasks/${currentTask.id}`, {
//   //       method: "DELETE",
//   //     });

//   //     if (!res.ok) {
//   //       const data = await res.json();
//   //       throw new Error(data.error || "Failed to delete task");
//   //     }

//   //     // Refresh tasks list
//   //     const tasksRes = await fetch("/api/tasks");
//   //     const tasksData = await tasksRes.json();
//   //     setTasks(tasksData);

//   //     setIsDeleteModalOpen(false);
//   //   } catch (err) {
//   //     setError(err.message);
//   //   } finally {
//   //     setIsDeleting(false);
//   //   }
//   // };

//   // const handleStatusChange = async (id, newStatus) => {
//   //   try {
//   //     setFormState({ pending: true });

//   //     const result = await updateTaskStatus({ id, status: newStatus });

//   //     if (result.error) {
//   //       setFormState({ error: result.error });
//   //       return;
//   //     }

//   //     setFormState({ success: result.success });

//   //     // Optional: Refresh tasks list if needed
//   //     const updated = await getTasks();
//   //     if (!updated.error) {
//   //       setTasks(updated.tasks);
//   //     }

//   //     setTimeout(() => setFormState(null), 1500);
//   //   } catch (err) {
//   //     setFormState({ error: err.message || "An error occurred" });
//   //   }
//   // };

//   // if (loading) {
//   //   return (
//   //     <div className="flex justify-center items-center h-screen">
//   //       Loading...
//   //     </div>
//   //   );
//   // }

//   if (error) {
//     return (
//       <div className="flex justify-center items-center h-screen text-red-600">
//         {error}
//       </div>
//     );
//   }

//   return (
//     <div>
//       <Navbar user={user} />

//       <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
//         <div className="px-4 py-6 sm:px-0">
//           <div className="flex justify-between items-center">
//             <h1 className="text-2xl font-semibold text-gray-900">
//               Manage Tasks
//             </h1>
//             <Button
//               className="hover:text-blue-700 hover:border-gray-300 cursor-pointer"
//               onClick={() => setIsCreateModalOpen(true)}
//             >
//               {" "}
//               Add Task{" "}
//             </Button>
//           </div>

//           <div className="mt-4 bg-white shadow overflow-hidden sm:rounded-lg">
//             <table className="min-w-full divide-y divide-gray-200">
//               <thead className="bg-gray-50">
//                 <tr>
//                   <th
//                     scope="col"
//                     className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
//                   >
//                     Title
//                   </th>
//                   <th
//                     scope="col"
//                     className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
//                   >
//                     Status
//                   </th>
//                   <th
//                     scope="col"
//                     className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
//                   >
//                     Assigned To
//                   </th>
//                   <th
//                     scope="col"
//                     className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
//                   >
//                     Actions
//                   </th>
//                 </tr>
//               </thead>
//               <tbody className="bg-white divide-y divide-gray-200">
//                 {tasks.map((task) => (
//                   <tr key={task.id}>
//                     <td className="px-6 py-4">
//                       <div className="text-sm font-medium text-gray-900">
//                         {task.title}
//                       </div>
//                       {task.description && (
//                         <div className="text-sm text-gray-500">
//                           {task.description}
//                         </div>
//                       )}
//                     </td>
//                     <td className="px-6 py-4 whitespace-nowrap">
//                       <TaskStatusBadge status={task.status} />
//                     </td>
//                     <td className="px-6 py-4 whitespace-nowrap">
//                       {task.assignee ? (
//                         <div>
//                           <div className="text-sm font-medium text-gray-900">
//                             {task.assignee.name}
//                           </div>
//                           <div className="text-sm text-gray-500">
//                             {task.assignee.email}
//                           </div>
//                         </div>
//                       ) : (
//                         <span className="text-sm text-gray-500">
//                           Unassigned
//                         </span>
//                       )}
//                     </td>
//                     <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
//                       <Button
//                         variant="outline"
//                         size="sm"
//                         onClick={() => {
//                           setCurrentTask(task);
//                           setIsEditModalOpen(true);
//                         }}
//                         className="mr-2 text-blue-600 hover:text-blue-700 hover:border-gray-300 cursor-pointer"
//                       >
//                         Edit
//                       </Button>

//                       <Button
//                         className="hover:border-gray-300 cursor-pointer"
//                         variant="destructive"
//                         size="sm"
//                         onClick={() => {
//                           setCurrentTask(task); // ✅ FIXED
//                           setIsDeleteModalOpen(true);
//                         }}
//                       >
//                         Delete
//                       </Button>
//                     </td>
//                   </tr>
//                 ))}
//               </tbody>
//             </table>
//           </div>
//         </div>
//       </main>

//       <Dialog
//         open={isCreateModalOpen}
//         onOpenChange={(open) => {
//           setIsCreateModalOpen(open);
//           if (!open) setFormState(null);
//         }}
//       >
//         <DialogContent>
//           <DialogHeader>
//             <DialogTitle>Create Task</DialogTitle>
//           </DialogHeader>
//           <TaskForm
//             users={users}
//             onSubmit={handleCreateTask}
//             formState={formState}
//           />
//         </DialogContent>
//       </Dialog>
//       <Dialog
//         open={isEditModalOpen}
//         onOpenChange={(open) => {
//           setIsEditModalOpen(open);
//           if (!open) setFormState(null);
//         }}
//       >
//         <DialogContent>
//           <DialogHeader>
//             <DialogTitle>Edit Task</DialogTitle>
//           </DialogHeader>
//           {currentTask && (
//             <TaskForm
//               task={currentTask}
//               users={users}
//               onSubmit={handleUpdateTask}
//               formState={formState}
//             />
//           )}
//         </DialogContent>
//       </Dialog>
//       <Dialog open={isDeleteModalOpen} onOpenChange={setIsDeleteModalOpen}>
//         <DialogContent>
//           <DialogHeader>
//             <DialogTitle>Delete Task</DialogTitle>
//           </DialogHeader>
//           {currentTask && (
//             <DeleteConfirmation
//               onConfirm={() => handleDeleteTask(currentTask.id)}
//               onCancel={() => setIsDeleteModalOpen(false)}
//               isDeleting={isDeleting}
//             />
//           )}
//         </DialogContent>
//       </Dialog>
//     </div>
//   );
// }

// // {/* Create Task Modal */}
// // <Modal
// //   isOpen={isCreateModalOpen}
// //   onClose={() => {
// //     setIsCreateModalOpen(false);
// //     setFormState(null);
// //   }}
// //   title="Create Task"
// // >
// //   <TaskForm
// //     users={users}
// //     onSubmit={handleCreateTask}
// //     formState={formState}
// //   />
// // </Modal>

// // {/* Edit Task Modal */}
// // <Modal
// //   isOpen={isEditModalOpen}
// //   onClose={() => {
// //     setIsEditModalOpen(false);
// //     setFormState(null);
// //   }}
// //   title="Edit Task"
// // >
// //   {currentTask && (
// //     <TaskForm
// //       task={currentTask}
// //       users={users}
// //       onSubmit={handleUpdateTask}
// //       formState={formState}
// //     />
// //   )}
// // </Modal>

// // {/* Delete Task Modal */}
// // <Modal
// //   isOpen={isDeleteModalOpen}
// //   onClose={() => setIsDeleteModalOpen(false)}
// //   title="Delete Task"
// // >
// //   {currentTask && (
// //     <DeleteConfirmation
// //       onConfirm={() => handleDeleteTask(currentTask.id)}
// //       onCancel={() => setIsDeleteModalOpen(false)}
// //       isDeleting={isDeleting}
// //     />
// //   )}
// // </Modal>
