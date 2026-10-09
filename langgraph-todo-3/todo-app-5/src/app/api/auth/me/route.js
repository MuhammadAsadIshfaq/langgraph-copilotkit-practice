import { NextResponse } from "next/server"
import { cookies } from "next/headers"

export async function GET() {
  try {
    // const userId = cookies().get("userId")?.value
    const cookieStore = await cookies()
    const userId = cookieStore.get("userId")?.value
    console.log("user_id-----------------",userId)
    if (!userId) {
        return null
    }

    const user = await prisma.user.findUnique({
        where: { id: userId },
    })
    

    if (!user) {
      return NextResponse.json({ error: "Unauthorized" }, { status: 401 })
    }

    // Don't return the password
    const { password, ...userWithoutPassword } = user

    return NextResponse.json(userWithoutPassword)
  } catch (error) {
    console.error("Error in /api/auth/me:", error)
    return NextResponse.json({ error: "Internal Server Error" }, { status: 500 })
  }
}
