import { cookies } from "next/headers";
import { redirect } from "next/navigation";
import prisma from "./prisma";
import bcrypt from "bcryptjs";

export async function hashPassword(password) {
  return await bcrypt.hash(password, 10);
}

export async function comparePasswords(plainPassword, hashedPassword) {
  return await bcrypt.compare(plainPassword, hashedPassword);
}

export async function login(email, password) {
  const user = await prisma.user.findUnique({
    where: { email },
  });

  if (!user) {
    return null;
  }

  const passwordMatch = await comparePasswords(password, user.password);

  if (!passwordMatch) {
    return null;
  }

  // Set a cookie with the user ID

  const cookieStore = await cookies();
  cookieStore.set("userId", String(user.id), {
    httpOnly: true,
    secure: process.env.NODE_ENV === "production",
    maxAge: 60 * 60 * 24 * 7, // 1 week
    path: "/",
  });
  cookieStore.set("userRole", user.role, {
    httpOnly: true,
    secure: process.env.NODE_ENV === "production",
    maxAge: 60 * 60 * 24 * 7,
    path: "/",
  });

  return user;
}

// export async function logout() {
//   cookies().delete("userId");
//   redirect("/login");
// }

export async function logout() {
  const cookieStore = await cookies(); // ✅ await cookies()
  cookieStore.delete("userId"); // ✅ now you can use it
  redirect("/login");
}

export async function getSession() {
  // const userId1 = await cookies().get("userId")?.value
  const cookieStore = await cookies();
  const userId = cookieStore.get("userId")?.value;

  console.log("user_id-----------------", userId);
  if (!userId) {
    return null;
  }

  const user = await prisma.user.findUnique({
    where: { id: userId },
  });

  return user;
}

export async function requireAuth() {
  const user = await getSession();

  if (!user) {
    redirect("/login");
  }

  return user;
}

export async function requireAdmin() {
  const user = await requireAuth();

  if (user.role !== "ADMIN") {
    redirect("/dashboard");
  }

  return user;
}
