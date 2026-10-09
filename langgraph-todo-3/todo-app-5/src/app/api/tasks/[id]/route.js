import { NextResponse } from "next/server"
import prisma from "@/lib/prisma"
import { requireAdmin, requireAuth } from "@/lib/auth"

export async function GET(request, { params }) {
  try {
    // Ensure user is authenticated
    const user = await requireAuth()

    const { id } = params

    const task = await prisma.task.findUnique({
      where: { id },
      include: {
        assignee: {
          select: {
            id: true,
            name: true,
            email: true,
          },
        },
      },
    })

    if (!task) {
      return NextResponse.json({ error: "Task not found" }, { status: 404 })
    }

    // If user is not admin, ensure they can only access their own tasks
    if (user.role !== "ADMIN" && task.assigneeId !== user.id) {
      return NextResponse.json({ error: "Unauthorized" }, { status: 401 })
    }

    return NextResponse.json(task)
  } catch (error) {
    console.error(`Error in GET /api/tasks/${params.id}:`, error)

    if (error.message === "UNAUTHORIZED") {
      return NextResponse.json({ error: "Unauthorized" }, { status: 401 })
    }

    return NextResponse.json({ error: "Internal Server Error" }, { status: 500 })
  }
}

export async function PUT(request, { params }) {
  try {
    // Ensure user is authenticated
    const user = await requireAuth()

    const { id } = params
    const body = await request.json()
    const { title, description, status, assigneeId } = body

    // Validate data
    if (!title) {
      return NextResponse.json({ error: "Title is required" }, { status: 400 })
    }

    // Check if task exists
    const existingTask = await prisma.task.findUnique({
      where: { id },
    })

    if (!existingTask) {
      return NextResponse.json({ error: "Task not found" }, { status: 404 })
    }

    // If user is not admin, ensure they can only update status of their own tasks
    if (user.role !== "ADMIN") {
      if (existingTask.assigneeId !== user.id) {
        return NextResponse.json({ error: "Unauthorized" }, { status: 401 })
      }

      // Regular users can only update status
      const task = await prisma.task.update({
        where: { id },
        data: { status },
        include: {
          assignee: {
            select: {
              id: true,
              name: true,
              email: true,
            },
          },
        },
      })

      return NextResponse.json(task)
    }

    // Admin can update all fields
    const task = await prisma.task.update({
      where: { id },
      data: {
        title,
        description,
        status,
        assigneeId: assigneeId || null,
      },
      include: {
        assignee: {
          select: {
            id: true,
            name: true,
            email: true,
          },
        },
      },
    })

    return NextResponse.json(task)
  } catch (error) {
    console.error(`Error in PUT /api/tasks/${params.id}:`, error)

    if (error.message === "UNAUTHORIZED") {
      return NextResponse.json({ error: "Unauthorized" }, { status: 401 })
    }

    return NextResponse.json({ error: "Internal Server Error" }, { status: 500 })
  }
}

export async function DELETE(request, { params }) {
  try {
    // Ensure user is admin
    await requireAdmin()

    const { id } = params

    // Check if task exists
    const existingTask = await prisma.task.findUnique({
      where: { id },
    })

    if (!existingTask) {
      return NextResponse.json({ error: "Task not found" }, { status: 404 })
    }

    // Delete task
    await prisma.task.delete({
      where: { id },
    })

    return NextResponse.json({ message: "Task deleted successfully" })
  } catch (error) {
    console.error(`Error in DELETE /api/tasks/${params.id}:`, error)

    if (error.message === "UNAUTHORIZED") {
      return NextResponse.json({ error: "Unauthorized" }, { status: 401 })
    }

    return NextResponse.json({ error: "Internal Server Error" }, { status: 500 })
  }
}
