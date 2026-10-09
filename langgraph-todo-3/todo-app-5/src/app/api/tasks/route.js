import { NextResponse } from "next/server";
import prisma from "@/lib/prisma";
import { requireAdmin, requireAuth } from "@/lib/auth";

export async function GET() {
  try {
    // Ensure user is authenticated
    const user = await requireAuth();

    // Determine query based on user role
    const where = user.role === "ADMIN" ? {} : { assigneeId: user.id };

    const tasks = await prisma.task.findMany({
      where,
      include: {
        assignee: {
          select: {
            id: true,
            name: true,
            email: true,
          },
        },
      },
      orderBy: {
        updatedAt: "desc",
      },
    });

    return NextResponse.json(tasks);
  } catch (error) {
    console.error("Error in GET /api/tasks:", error);

    if (error.message === "UNAUTHORIZED") {
      return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
    }

    return NextResponse.json(
      { error: "Internal Server Error" },
      { status: 500 }
    );
  }
}

export async function POST(request) {
  try {
    // Ensure user is admin
    await requireAdmin();

    const body = await request.json();
    const { title, description, assigneeId, status = "TODO" } = body;

    // Validate data
    if (!title) {
      return NextResponse.json({ error: "Title is required" }, { status: 400 });
    }

    // Create task
    const task = await prisma.task.create({
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
    });

    return NextResponse.json(task, { status: 201 });
  } catch (error) {
    console.error("Error in POST /api/tasks:", error);

    if (error.message === "UNAUTHORIZED") {
      return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
    }

    return NextResponse.json(
      { error: "Internal Server Error" },
      { status: 500 }
    );
  }
}
