"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogTrigger,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from "@/components/ui/dialog";
import { useMemo } from "react";

import { useCopilotReadable } from "@copilotkit/react-core";

import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import React from "react";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { useCopilotAction } from "@copilotkit/react-core";

import {
  Modal,
  UserForm,
  DeleteConfirmation,
} from "@/components/ui-components";
import {
  createUser,
  updateUser,
  deleteUser,
  getCurrentUserAndAllUsers,
  getAllUsers,
} from "@/lib/actions";

// Zod schema for user validation
const userSchema = z.object({
  name: z.string().min(2, "Name must be at least 2 characters"),
  email: z.string().email("Invalid email address"),
  password: z
    .string()
    .min(5, "Password must be at least 5 characters")
    .optional(),
  role: z.enum(["USER", "ADMIN"], {
    required_error: "Please select a role",
  }),
});

// Schema for creating user (password required)
const createUserSchema = userSchema.extend({
  password: z.string().min(5, "Password must be at least 5 characters"),
});

// Schema for updating user (password optional)
const updateUserSchema = userSchema.extend({
  id: z.string(),
  password: z
    .string()
    .min(5, "Password must be at least 6 characters")
    .optional()
    .or(z.literal("")),
});

export default function UsersPage() {
  const router = useRouter();
  const [users, setUsers] = useState([]);
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);
  const [currentUser, setCurrentUser] = useState(null);
  const [isDeleting, setIsDeleting] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Create user form
  const createForm = useForm({
    resolver: zodResolver(createUserSchema),
    defaultValues: {
      name: "",
      email: "",
      password: "",
      role: "USER",
    },
  });

  const usersSnapshot = useMemo(() => JSON.stringify(users), [users]);

  useCopilotReadable({
    description: "All users in the system",
    value: usersSnapshot,
  });

  useCopilotAction({
    name: "createUser",
    description: "Create a new user with provided details",
    parameters: [
      {
        name: "name",
        type: "string",
        description: "User's name",
        required: true,
      },
      {
        name: "email",
        type: "string",
        description: "User's email",
        required: true,
      },
      {
        name: "password",
        type: "string",
        description: "New password (optional)",
        required: true,
      },
      {
        name: "role",
        type: "string",
        description: "User's role",
        required: true,
      },
    ],
    handler: async ({ name, email, role, password }) => {
      if (!name || !email || !role || !password) {
        throw new Error("All fields are required");
      }
      await handleCreateUser({ name, email, role, password });
      return `User "${name}" created successfully.`;
    },
  });

  useCopilotAction({
    name: "editUser",
    description: "Edit an existing user's details using their ID",
    parameters: [
      { name: "id", type: "string", description: "User ID" },
      {
        name: "name",
        type: "string",
        description: "Updated name",
        optional: true,
      },
      {
        name: "email",
        type: "string",
        description: "Updated email",
        optional: true,
      },
      {
        name: "password",
        type: "string",
        description: "New password (optional)",
        optional: true,
      },
      {
        name: "role",
        type: "string",
        description: "Updated role (USER or ADMIN)",
        optional: true,
      },
    ],
    handler: async ({ id, name, email, password, role }) => {
      const updatedFields = { id };

      if (name) updatedFields.name = name;
      if (email) updatedFields.email = email;
      if (password) updatedFields.password = password;
      if (role) updatedFields.role = role;

      const result = await updateUser(updatedFields);

      if (result.error) {
        throw new Error(result.error);
      }

      // const usersResult = await getAllUsers();
      // setUsers(usersResult.users);
    },
  });

  useCopilotAction({
    name: "deleteUser",
    description: "Delete a user by their ID",
    parameters: [
      { name: "id", type: "string", description: "User ID to delete" },
    ],
    handler: async ({ id }) => {
      const result = await deleteUser({ id });

      if (result.error) {
        throw new Error(result.error);
      }

      const usersResult = await getAllUsers();
      setUsers(usersResult.users);
    },
  });

  // Edit user form
  const editForm = useForm({
    resolver: zodResolver(updateUserSchema),
    defaultValues: {
      id: "",
      name: "",
      email: "",
      password: "",
      role: "USER",
    },
  });

  useEffect(() => {
    async function fetchData() {
      try {
        const result = await getCurrentUserAndAllUsers();

        if (result.redirectTo) {
          router.push(result.redirectTo);
          return;
        }

        if (result.error) {
          setError(result.error);
          return;
        }

        setUser(result.user);
        setUsers(result.users);
      } catch (err) {
        setError(err.message || "An error occurred");
      } finally {
        setLoading(false);
      }
    }

    fetchData();
  }, []);

  const handleCreateUser = async (data) => {
    try {
      setIsSubmitting(true);

      const result = await createUser(data);

      if (result.error) {
        // Set form error if creation fails
        createForm.setError("root", { message: result.error });
        return;
      }

      // Refresh users list
      const usersResult = await getAllUsers();
      if (usersResult.error) {
        setError(usersResult.error);
        return;
      }

      setUsers(usersResult.users);

      // Reset form and close modal
      createForm.reset();
      setIsCreateModalOpen(false);

      // You could add a toast notification here
      console.log("User created successfully");
    } catch (err) {
      createForm.setError("root", {
        message: err.message || "An error occurred",
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleUpdateUser = async (data) => {
    try {
      setIsSubmitting(true);

      // const data = {
      //   password: "",
      // };

      // Remove password if it's empty
      const updateData = { ...data };
      if (!updateData.password) {
        delete updateData.password;
      }

      const result = await updateUser(updateData);

      if (result.error) {
        editForm.setError("root", { message: result.error });
        return;
      }

      // Refresh users list
      const usersResult = await getAllUsers();
      if (usersResult.error) {
        setError(usersResult.error);
        return;
      }

      setUsers(usersResult.users);

      // Reset form and close modal
      editForm.reset();
      setIsEditModalOpen(false);
      setCurrentUser(null);

      console.log("User updated successfully");
    } catch (err) {
      editForm.setError("root", {
        message: err.message || "An error occurred",
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleDeleteUser = async () => {
    try {
      setIsDeleting(true);

      const result = await deleteUser({ id: currentUser.id });

      if (result.error) {
        throw new Error(result.error);
      }

      // Refresh users list
      const usersResult = await getAllUsers();
      if (usersResult.error) {
        throw new Error(usersResult.error);
      }

      setUsers(usersResult.users);
      setIsDeleteModalOpen(false);
      setCurrentUser(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsDeleting(false);
    }
  };

  const openEditModal = (userToEdit) => {
    setCurrentUser(userToEdit);
    editForm.reset({
      id: userToEdit.id,
      name: userToEdit.name,
      email: userToEdit.email,
      password: "",
      role: userToEdit.role,
    });
    setIsEditModalOpen(true);
  };

  const closeCreateModal = () => {
    createForm.reset();
    createForm.clearErrors();
    setIsCreateModalOpen(false);
  };

  const closeEditModal = () => {
    editForm.reset();
    editForm.clearErrors();
    setIsEditModalOpen(false);
    setCurrentUser(null);
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-screen">
        Loading...
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex justify-center items-center h-screen text-red-600">
        {error}
      </div>
    );
  }

  return (
    <div>
      {/* <Navbar user={user} /> */}

      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <div className="flex justify-between items-center">
            <h1 className="text-2xl font-semibold text-gray-900">
              Manage Users
            </h1>
            <Button
              className="hover:text-blue-700 hover:border-gray-300 cursor-pointer"
              onClick={() => setIsCreateModalOpen(true)}
            >
              Add User
            </Button>
          </div>
          <div className="mt-4 bg-white shadow overflow-hidden sm:rounded-lg">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th
                    scope="col"
                    className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                  >
                    Name
                  </th>
                  <th
                    scope="col"
                    className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                  >
                    Email
                  </th>
                  <th
                    scope="col"
                    className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                  >
                    Role
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
                {users.map((userItem) => (
                  <tr key={userItem.id}>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm font-medium text-gray-900">
                        {userItem.name}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-500">
                        {userItem.email}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span
                        className={`px-2 py-1 text-xs font-medium rounded-full ${
                          userItem.role === "ADMIN"
                            ? "bg-purple-100 text-purple-800"
                            : "bg-green-100 text-green-800"
                        }`}
                      >
                        {userItem.role}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => openEditModal(userItem)}
                        className="mr-2 text-blue-600 hover:text-blue-700 hover:border-gray-300 cursor-pointer"
                      >
                        Edit
                      </Button>

                      <Button
                        className="hover:border-gray-300 cursor-pointer"
                        variant="destructive"
                        size="sm"
                        onClick={() => {
                          setCurrentUser(userItem);
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

      {/* Create User Modal */}
      <Dialog open={isCreateModalOpen} onOpenChange={closeCreateModal}>
        <DialogContent className="sm:max-w-[425px]">
          <DialogHeader>
            <DialogTitle>Create User</DialogTitle>
          </DialogHeader>
          <Form {...createForm}>
            <form
              onSubmit={createForm.handleSubmit(handleCreateUser)}
              className="space-y-4"
            >
              <FormField
                control={createForm.control}
                name="name"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Name</FormLabel>
                    <FormControl>
                      <Input placeholder="Enter user name" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={createForm.control}
                name="email"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Email</FormLabel>
                    <FormControl>
                      <Input
                        placeholder="Enter email address"
                        type="email"
                        {...field}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={createForm.control}
                name="password"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Password</FormLabel>
                    <FormControl>
                      <Input
                        placeholder="Enter password"
                        type="password"
                        {...field}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={createForm.control}
                name="role"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Role</FormLabel>
                    <Select
                      onValueChange={field.onChange}
                      defaultValue={field.value}
                    >
                      <FormControl>
                        <SelectTrigger>
                          <SelectValue placeholder="Select a role" />
                        </SelectTrigger>
                      </FormControl>
                      <SelectContent>
                        <SelectItem value="USER">User</SelectItem>
                        <SelectItem value="ADMIN">Admin</SelectItem>
                      </SelectContent>
                    </Select>
                    <FormMessage />
                  </FormItem>
                )}
              />

              {createForm.formState.errors.root && (
                <div className="text-red-600 text-sm">
                  {createForm.formState.errors.root.message}
                </div>
              )}

              <DialogFooter>
                <Button
                  type="button"
                  variant="outline"
                  onClick={closeCreateModal}
                  disabled={isSubmitting}
                >
                  Cancel
                </Button>
                <Button type="submit" disabled={isSubmitting}>
                  {isSubmitting ? "Creating..." : "Create User"}
                </Button>
              </DialogFooter>
            </form>
          </Form>
        </DialogContent>
      </Dialog>

      {/* Edit User Modal */}
      <Dialog open={isEditModalOpen} onOpenChange={closeEditModal}>
        <DialogContent className="sm:max-w-[425px]">
          <DialogHeader>
            <DialogTitle>Edit User</DialogTitle>
          </DialogHeader>
          <Form {...editForm}>
            <form
              onSubmit={editForm.handleSubmit(handleUpdateUser)}
              className="space-y-4"
            >
              <FormField
                control={editForm.control}
                name="name"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Name</FormLabel>
                    <FormControl>
                      <Input placeholder="Enter user name" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={editForm.control}
                name="email"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Email</FormLabel>
                    <FormControl>
                      <Input
                        placeholder="Enter email address"
                        type="email"
                        {...field}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={editForm.control}
                name="password"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Password</FormLabel>
                    <FormControl>
                      <Input
                        placeholder="Leave empty to keep current password"
                        type="password"
                        {...field}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={editForm.control}
                name="role"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Role</FormLabel>
                    <Select onValueChange={field.onChange} value={field.value}>
                      <FormControl>
                        <SelectTrigger>
                          <SelectValue placeholder="Select a role" />
                        </SelectTrigger>
                      </FormControl>
                      <SelectContent>
                        <SelectItem value="USER">User</SelectItem>
                        <SelectItem value="ADMIN">Admin</SelectItem>
                      </SelectContent>
                    </Select>
                    <FormMessage />
                  </FormItem>
                )}
              />

              {editForm.formState.errors.root && (
                <div className="text-red-600 text-sm">
                  {editForm.formState.errors.root.message}
                </div>
              )}

              <DialogFooter>
                <Button
                  type="button"
                  variant="outline"
                  onClick={closeEditModal}
                  disabled={isSubmitting}
                >
                  Cancel
                </Button>
                <Button type="submit" disabled={isSubmitting}>
                  {isSubmitting ? "Updating..." : "Update User"}
                </Button>
              </DialogFooter>
            </form>
          </Form>
        </DialogContent>
      </Dialog>

      {/* Delete User Modal */}
      <Dialog open={isDeleteModalOpen} onOpenChange={setIsDeleteModalOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Delete User</DialogTitle>
          </DialogHeader>
          {currentUser && (
            <div className="py-4">
              <p className="text-sm text-gray-500">
                Are you sure you want to delete{" "}
                <strong>{currentUser.name}</strong>? This action cannot be
                undone.
              </p>
              <div className="flex justify-end space-x-2 mt-6">
                <Button
                  variant="outline"
                  onClick={() => setIsDeleteModalOpen(false)}
                  disabled={isDeleting}
                >
                  Cancel
                </Button>
                <Button
                  variant="destructive"
                  onClick={handleDeleteUser}
                  disabled={isDeleting}
                >
                  {isDeleting ? "Deleting..." : "Delete User"}
                </Button>
              </div>
            </div>
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
// import {
//   Dialog,
//   DialogTrigger,
//   DialogContent,
//   DialogHeader,
//   DialogTitle,
//   DialogFooter,
// } from "@/components/ui/dialog";
// import React from "react";
// import { useForm } from "react-hook-form";
// import { z } from "zod";
// import { zodResolver } from "@hookform/resolvers/zod";
// import {
//   Modal,
//   UserForm,
//   DeleteConfirmation,
// } from "@/components/ui-components";
// import {
//   createUser,
//   updateUser,
//   deleteUser,
//   getCurrentUserAndAllUsers,
//   getAllUsers,
// } from "@/lib/actions";

// export default function UsersPage() {
//   const router = useRouter();
//   const [users, setUsers] = useState([]);
//   const [user, setUser] = useState(null);
//   const [loading, setLoading] = useState(true);
//   const [error, setError] = useState(null);
//   const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
//   const [isEditModalOpen, setIsEditModalOpen] = useState(false);
//   const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);
//   const [currentUser, setCurrentUser] = useState(null);
//   const [formState, setFormState] = useState(null);
//   const [isDeleting, setIsDeleting] = useState(false);

//   useEffect(() => {
//     async function fetchData() {
//       try {
//         const result = await getCurrentUserAndAllUsers();

//         if (result.redirectTo) {
//           router.push(result.redirectTo);
//           return;
//         }

//         if (result.error) {
//           setError(result.error);
//           return;
//         }

//         setUser(result.user);
//         setUsers(result.users);
//       } catch (err) {
//         setError(err.message || "An error occurred");
//       } finally {
//         setLoading(false);
//       }
//     }

//     fetchData();
//   }, []);

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

//   //       // Fetch users
//   //       const usersRes = await fetch("/api/users");
//   //       if (!usersRes.ok) throw new Error("Failed to fetch users");
//   //       const usersData = await usersRes.json();
//   //       setUsers(usersData);
//   //     } catch (err) {
//   //       setError(err.message);
//   //     } finally {
//   //       setLoading(false);
//   //     }
//   //   }

//   //   fetchData();
//   // }, []);

//   const handleCreateUser = async (data) => {
//     try {
//       setFormState({ pending: true });

//       const result = await createUser(data);

//       if (result.error) {
//         setFormState({ error: result.error });
//         return;
//       }

//       // ✅ Use server action to get updated users
//       const usersResult = await getAllUsers();

//       if (usersResult.error) {
//         setFormState({ error: usersResult.error });
//         return;
//       }

//       setUsers(usersResult.users);
//       setFormState({ success: result.success });

//       setTimeout(() => {
//         setIsCreateModalOpen(false);
//         setFormState(null);
//       }, 1500);
//     } catch (err) {
//       setFormState({ error: err.message || "An error occurred" });
//     }
//   };

//   // const handleCreateUser = async (data) => {
//   //   try {
//   //     setFormState({ pending: true });

//   //     // Directly call the server action
//   //     const result = await createUser(data);

//   //     if (result.error) {
//   //       setFormState({ error: result.error });
//   //       return;
//   //     }

//   //     setFormState({ success: result.success });

//   //     // Fetch updated users list to refresh UI
//   //     const usersRes = await fetch("/api/users"); // or use a dedicated client fetch function
//   //     const usersData = await usersRes.json();
//   //     setUsers(usersData);

//   //     setTimeout(() => {
//   //       setIsCreateModalOpen(false);
//   //       setFormState(null);
//   //     }, 1500);
//   //   } catch (err) {
//   //     setFormState({ error: err.message || "An error occurred" });
//   //   }
//   // };

//   // const handleCreateUser = async (formData) => {
//   //   try {
//   //     setFormState({ pending: true })
//   //     const data2= await createUser(formData)

//   //     const res = await fetch("/api/users", {
//   //       method: "POST",
//   //       headers: {
//   //         "Content-Type": "application/json",
//   //       },
//   //       body: JSON.stringify(formData),
//   //     })

//   //     const data = await res.json()

//   //     if (!res.ok) {
//   //       setFormState({ error: data.error || "Failed to create user" })
//   //       return
//   //     }

//   //     setFormState({ success: "User created successfully" })

//   //     // Refresh users list
//   //     const usersRes = await fetch("/api/users")
//   //     const usersData = await usersRes.json()
//   //     setUsers(usersData)

//   //     // Close modal after a delay
//   //     setTimeout(() => {
//   //       setIsCreateModalOpen(false)
//   //       setFormState(null)
//   //     }, 1500)
//   //   } catch (err) {
//   //     setFormState({ error: err.message || "An error occurred" })
//   //   }
//   // }

//   const handleUpdateUser = async (data) => {
//     try {
//       setFormState({ pending: true });

//       // Directly call the server action
//       const result = await updateUser(data);

//       if (result.error) {
//         setFormState({ error: result.error });
//         return;
//       }

//       const usersResult = await getAllUsers();

//       if (usersResult.error) {
//         setFormState({ error: usersResult.error });
//         return;
//       }

//       setUsers(usersResult.users);
//       setFormState({ success: result.success });

//       setTimeout(() => {
//         setIsCreateModalOpen(false);
//         setFormState(null);
//       }, 1500);
//     } catch (err) {
//       setFormState({ error: err.message || "An error occurred" });
//     }
//   };

//   const handleDeleteUser = async () => {
//     try {
//       setIsDeleting(true);

//       // Delete user using server action
//       const result = await deleteUser({ id: currentUser.id });

//       if (result.error) {
//         throw new Error(result.error);
//       }

//       // ✅ Use server action instead of API call
//       const usersResult = await getAllUsers();

//       if (usersResult.error) {
//         throw new Error(usersResult.error);
//       }

//       setUsers(usersResult.users);
//       setIsDeleteModalOpen(false);
//     } catch (err) {
//       setError(err.message);
//     } finally {
//       setIsDeleting(false);
//     }
//   };

//   // const handleDeleteUser = async () => {
//   //   try {
//   //     setIsDeleting(true);

//   //     // Directly call server action
//   //     const result = await deleteUser({ id: currentUser.id });

//   //     if (result.error) {
//   //       throw new Error(result.error);
//   //     }

//   //     // Refresh users list
//   //     const usersRes = await fetch("/api/users"); // Or replace with your own fetch logic
//   //     const usersData = await usersRes.json();
//   //     setUsers(usersData);

//   //     setIsDeleteModalOpen(false);
//   //   } catch (err) {
//   //     setError(err.message);
//   //   } finally {
//   //     setIsDeleting(false);
//   //   }
//   // };

//   if (loading) {
//     return (
//       <div className="flex justify-center items-center h-screen">
//         Loading...
//       </div>
//     );
//   }

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
//               Manage Users
//             </h1>
//             <Button
//               className="hover:text-blue-700 hover:border-gray-300 cursor-pointer"
//               onClick={() => setIsCreateModalOpen(true)}
//             >
//               {" "}
//               Add User{" "}
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
//                     Name
//                   </th>
//                   <th
//                     scope="col"
//                     className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
//                   >
//                     Email
//                   </th>
//                   <th
//                     scope="col"
//                     className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
//                   >
//                     Role
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
//                 {users.map((user) => (
//                   <tr key={user.id}>
//                     <td className="px-6 py-4 whitespace-nowrap">
//                       <div className="text-sm font-medium text-gray-900">
//                         {user.name}
//                       </div>
//                     </td>
//                     <td className="px-6 py-4 whitespace-nowrap">
//                       <div className="text-sm text-gray-500">{user.email}</div>
//                     </td>
//                     <td className="px-6 py-4 whitespace-nowrap">
//                       <span
//                         className={`px-2 py-1 text-xs font-medium rounded-full ${
//                           user.role === "ADMIN"
//                             ? "bg-purple-100 text-purple-800"
//                             : "bg-green-100 text-green-800"
//                         }`}
//                       >
//                         {user.role}
//                       </span>
//                     </td>
//                     <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
//                       <Button
//                         variant="outline"
//                         size="sm"
//                         onClick={() => {
//                           setCurrentUser(user);
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
//                           setCurrentUser(user);
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
//       <Dialog open={isCreateModalOpen} onOpenChange={setIsCreateModalOpen}>
//         <DialogContent>
//           <DialogHeader>
//             <DialogTitle>Create User</DialogTitle>
//           </DialogHeader>
//           <UserForm onSubmit={handleCreateUser} formState={formState} />
//         </DialogContent>
//       </Dialog>
//       <Dialog open={isEditModalOpen} onOpenChange={setIsEditModalOpen}>
//         <DialogContent>
//           <DialogHeader>
//             <DialogTitle>Edit User</DialogTitle>
//           </DialogHeader>
//           {currentUser && (
//             <UserForm
//               user={currentUser}
//               onSubmit={handleUpdateUser}
//               formState={formState}
//             />
//           )}
//         </DialogContent>
//       </Dialog>
//       <Dialog open={isDeleteModalOpen} onOpenChange={setIsDeleteModalOpen}>
//         <DialogContent>
//           <DialogHeader>
//             <DialogTitle>Delete User</DialogTitle>
//           </DialogHeader>
//           {currentUser && (
//             <DeleteConfirmation
//               onConfirm={handleDeleteUser}
//               onCancel={() => setIsDeleteModalOpen(false)}
//               isDeleting={isDeleting}
//             />
//           )}
//         </DialogContent>
//       </Dialog>
//     </div>
//   );
// }

// // {/* Create User Modal */}
// // <Modal
// //   isOpen={isCreateModalOpen}
// //   onClose={() => {
// //     setIsCreateModalOpen(false);
// //     setFormState(null);
// //   }}
// //   title="Create User"
// // >
// //   <UserForm onSubmit={handleCreateUser} formState={formState} />
// // </Modal>

// // {/* Edit User Modal */}
// // <Modal
// //   isOpen={isEditModalOpen}
// //   onClose={() => {
// //     setIsEditModalOpen(false);
// //     setFormState(null);
// //   }}
// //   title="Edit User"
// // >
// //   {currentUser && (
// //     <UserForm
// //       user={currentUser}
// //       onSubmit={handleUpdateUser}
// //       formState={formState}
// //     />
// //   )}
// // </Modal>

// // {/* Delete User Modal */}
// // <Modal
// //   isOpen={isDeleteModalOpen}
// //   onClose={() => setIsDeleteModalOpen(false)}
// //   title="Delete User"
// // >
// //   {currentUser && (
// //     <DeleteConfirmation
// //       onConfirm={handleDeleteUser}
// //       onCancel={() => setIsDeleteModalOpen(false)}
// //       isDeleting={isDeleting}
// //     />
// //   )}
// // </Modal>
