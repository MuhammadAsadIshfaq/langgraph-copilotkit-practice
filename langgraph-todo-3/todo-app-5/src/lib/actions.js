"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import prisma from "./prisma";
import { hashPassword, login as authLogin, logout as authLogout } from "./auth";
import { getSession } from "./auth";

// User actions
export async function createUser(data) {
  const { name, email, password, role } = data;

  // const name = formData.get("name")
  // const email = formData.get("email")
  // const password = formData.get("password")
  // const role = formData.get("role")

  // Validate data
  if (!name || !email || !password || !role) {
    return { error: "All fields are required" };
  }

  try {
    // Check if user already exists
    const existingUser = await prisma.user.findUnique({
      where: { email },
    });

    if (existingUser) {
      return { error: "User with this email already exists" };
    }

    // Hash password
    const hashedPassword = await hashPassword(password);

    // Create user
    await prisma.user.create({
      data: {
        name,
        email,
        password: hashedPassword,
        role,
      },
    });

    revalidatePath("/admin/users");
    return { success: "User created successfully" };
  } catch (error) {
    console.error("Error creating user:", error);
    return { error: "Failed to create user" };
  }
}

export async function updateUser(data) {
  const { id, name, email, password, role } = data;

  // const id = formData.get("id")
  // const name = formData.get("name")
  // const email = formData.get("email")
  // const role = formData.get("role")
  // const password = formData.get("password")

  try {
    const data = {
      name,
      email,
      role,
    };

    // Only update password if provided
    if (password) {
      data.password = await hashPassword(password);
    }

    await prisma.user.update({
      where: { id },
      data,
    });

    revalidatePath("/admin/users");
    return { success: "User updated successfully" };
  } catch (error) {
    console.error("Error updating user:", error);
    return { error: "Failed to update user" };
  }
}

export async function deleteUser(data) {
  const { id } = data;

  try {
    await prisma.user.delete({
      where: { id },
    });

    revalidatePath("/admin/users");
    return { success: "User deleted successfully" };
  } catch (error) {
    console.error("Error deleting user:", error);
    return { error: "Failed to delete user" };
  }
}

// Task actions
export async function createTask(data) {
  const { title, description, assigneeId } = data;

  // Validate data
  if (!title) {
    return { error: "Title is required" };
  }

  try {
    await prisma.task.create({
      data: {
        title,
        description,
        assigneeId: assigneeId || null,
      },
    });

    revalidatePath("/admin/tasks");
    return { success: "Task created successfully" };
  } catch (error) {
    console.error("Error creating task:", error);
    return { error: "Failed to create task" };
  }
}

export async function updateTask(data) {
  const { id, title, description, assigneeId, status } = data;

  // const id = formData.get("id");
  // const title = formData.get("title");
  // const description = formData.get("description");
  // const status = formData.get("status");
  // const assigneeId = formData.get("assigneeId");

  try {
    await prisma.task.update({
      where: { id },
      data: {
        title,
        description,
        status,
        assigneeId: assigneeId || null,
      },
    });

    revalidatePath("/admin/tasks");
    revalidatePath("/dashboard");
    return { success: "Task updated successfully" };
  } catch (error) {
    console.error("Error updating task:", error);
    return { error: "Failed to update task" };
  }
}

export async function updateTaskStatus(formData) {
  const id = formData.get("id");
  const status = formData.get("status");

  try {
    await prisma.task.update({
      where: { id },
      data: { status },
    });

    revalidatePath("/dashboard");
    return { success: "Task status updated successfully" };
  } catch (error) {
    console.error("Error updating task status:", error);
    return { error: "Failed to update task status" };
  }
}

export async function deleteTask(id) {
  try {
    await prisma.task.delete({
      where: { id },
    });

    revalidatePath("/admin/tasks");
    return { success: "Task deleted successfully" };
  } catch (error) {
    console.error("Error deleting task:", error);
    return { error: "Failed to delete task" };
  }
}
import { cookies } from "next/headers";

export async function login(data) {
  const { email, password } = data;

  if (!email || !password) {
    return { error: "Email and password are required" };
  }

  try {
    const user = await authLogin(email, password);

    if (!user) {
      return { error: "Invalid email or password" };
    }

    // Await cookies() because it's async in your Next.js version
    const cookieStore = await cookies();
    cookieStore.set("userId", String(user.id), {
      httpOnly: true,
      path: "/",
      maxAge: 60 * 60 * 24 * 7, // 1 week
      secure: process.env.NODE_ENV === "production",
    });

    // Return success instead of redirecting
    return { success: "Login successful", user };
  } catch (error) {
    console.error("Error logging in:", error);
    return { error: "Failed to log in" };
  }
}

// Auth actions
// export async function login(data) {
//   const { email, password } = data;

//   // const email = formData.get("email");
//   // const password = formData.get("password");

//   // Validate data
//   if (!email || !password) {
//     return { error: "Email and password are required" };
//   }

//   try {
//     const user = await authLogin(email, password);

//     if (!user) {
//       return { error: "Invalid email or password" };
//     }

//     // redirect("/dashboard");
//   } catch (error) {
//     if (error.digest === "NEXT_REDIRECT") throw error;
//     console.error("Error logging in:", error);
//     return { error: "Failed to log in" };
//   }
// }

export async function logout() {
  await authLogout();
}

// Seed database with initial data
export async function seedDatabase() {
  try {
    // Check if admin exists
    const adminExists = await prisma.user.findFirst({
      where: { role: "ADMIN" },
    });

    if (!adminExists) {
      // Create admin user
      await prisma.user.create({
        data: {
          name: "Admin User",
          email: "admin@example.com",
          password: await hashPassword("admin123"),
          role: "ADMIN",
        },
      });
    }

    // Create some regular users if none exist
    const usersExist = await prisma.user.findFirst({
      where: { role: "USER" },
    });

    if (!usersExist) {
      await prisma.user.createMany({
        data: [
          {
            name: "John Doe",
            email: "john@example.com",
            password: await hashPassword("password123"),
            role: "USER",
          },
          {
            name: "Jane Smith",
            email: "jane@example.com",
            password: await hashPassword("password123"),
            role: "USER",
          },
        ],
      });
    }

    // Create some tasks if none exist
    const tasksExist = await prisma.task.findFirst({});

    if (!tasksExist) {
      // Get user IDs
      const users = await prisma.user.findMany({
        where: { role: "USER" },
        select: { id: true },
      });

      if (users.length > 0) {
        await prisma.task.createMany({
          data: [
            {
              title: "Complete project documentation",
              description: "Write comprehensive documentation for the project",
              status: "TODO",
              assigneeId: users[0].id,
            },
            {
              title: "Fix login bug",
              description: "Address the issue with login functionality",
              status: "IN_PROGRESS",
              assigneeId: users[0].id,
            },
            {
              title: "Design new landing page",
              description: "Create mockups for the new landing page",
              status: "TODO",
              assigneeId: users.length > 1 ? users[1].id : users[0].id,
            },
          ],
        });
      }
    }

    return { success: "Database seeded successfully" };
  } catch (error) {
    console.error("Error seeding database:", error);
    return { error: "Failed to seed database" };
  }
}

export async function getCurrentUserAndAllUsers() {
  const user = await getSession();

  if (!user) {
    return { redirectTo: "/login" };
  }

  if (user.role !== "ADMIN") {
    return { redirectTo: "/dashboard" };
  }

  try {
    const users = await prisma.user.findMany({
      select: { id: true, name: true, email: true, role: true },
    });

    return {
      user,
      users,
    };
  } catch (err) {
    console.error("Error fetching users:", err);
    return { error: "Failed to fetch users" };
  }
}

export const fetchTasksFromAPI = async () => {
  try {
    const response = await fetch("http://localhost:8000/tasks", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      throw new Error("Failed to fetch tasks");
    }

    const data = await response.json();
    return { tasks: data };
  } catch (error) {
    return { error: error.message };
  }
};

// export async function getTasks() {
//   try {
//     const tasks = await prisma.task.findMany({
//       include: {
//         assignee: true, // optional: include related user data
//       },
//       orderBy: {
//         createdAt: "desc",
//       },
//     });

//     return { tasks };
//   } catch (error) {
//     console.error("Error fetching tasks:", error);
//     return { error: "Failed to fetch tasks" };
//   }
// }

export async function fetchCurrentUser() {
  const user = await getSession();
  if (!user) return null;
  return user;
}

export async function getUsers() {
  try {
    const users = await prisma.user.findMany();
    return { users };
  } catch (error) {
    console.error("Error fetching users:", error);
    return { error: "Failed to fetch users" };
  }
}

export async function getAllUsers() {
  try {
    const users = await prisma.user.findMany({
      select: {
        id: true,
        name: true,
        email: true,
        role: true,
        // Add any other fields you want
      },
    });

    return { users };
  } catch (error) {
    return { error: "Failed to fetch users" };
  }
}
