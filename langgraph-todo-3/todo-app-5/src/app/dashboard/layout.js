import Navbar from "@/components/navbar";
import { getSession } from "@/lib/auth"; // or use requireAuth()
import { headers } from "next/headers"; // to get the current pathname

export default async function Layout({ children }) {
  //   const user = await getSession(); // Fetch user from cookies/session
  return (
    <>
      <Navbar />
      <main>{children}</main>
    </>
  );
}
