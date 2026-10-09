import { redirect } from "next/navigation";
import { getSession } from "@/lib/auth";
import { cookies } from "next/headers";
import prisma from "@/lib/prisma";

export default async function Home() {
  // const user = await getSession();

  // // const userId = await cookies().get("userId")?.value
  // // console.log("user_id-----------------",userId)
  // // if (!userId) {
  // //   return null
  // // }

  // // const user = await prisma.user.findUnique({
  // //   where: { id: userId },
  // // })

  // if (user) {
  //   redirect("/dashboard");
  // } else {
  //   redirect("/login");
  // }
  return null;
}
