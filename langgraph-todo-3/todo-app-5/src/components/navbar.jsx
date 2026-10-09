import Link from "next/link";
import { logout } from "@/lib/actions";
import { cookies } from "next/headers";

import { Button } from "@/components/ui/button";

export default async function Navbar() {
  const cookieStore = await cookies();
  const userId = cookieStore.get("userId")?.value;
  const userRole = cookieStore.get("userRole")?.value;
  // const userName = cookieStore.get("userName")?.value || "User";

  const user = userId
    ? {
        role: userRole,
      }
    : null;

  return (
    <nav className="bg-white shadow">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16 items-center">
          <div className="flex items-center gap-6">
            <Link
              href="/dashboard"
              className="text-xl font-bold text-blue-600 cursor-pointer"
            >
              Todo App
            </Link>

            <Link href="/dashboard">
              <Button
                variant="ghost"
                className="hover:text-blue-700 cursor-pointer"
              >
                Dashboard
              </Button>
            </Link>

            {user?.role === "ADMIN" && (
              <>
                <Link href="/admin/users">
                  <Button
                    variant="ghost"
                    className="hover:text-blue-700 cursor-pointer"
                  >
                    Manage Users
                  </Button>
                </Link>
                <Link href="/admin/tasks">
                  <Button
                    variant="ghost"
                    className="hover:text-blue-700 cursor-pointer"
                  >
                    Manage Tasks
                  </Button>
                </Link>
              </>
            )}
          </div>

          <div className="flex items-center gap-4">
            {user && (
              <span className="text-sm text-gray-600">
                {user.name} ({user.role === "ADMIN" ? "Admin" : "User"})
              </span>
            )}
            <form action={logout}>
              <Button
                type="submit"
                className="hover:text-blue-700 cursor-pointer"
              >
                Logout
              </Button>
            </form>
          </div>
        </div>
      </div>
    </nav>
  );
}

// import Link from "next/link"
// import { logout } from "@/lib/actions"

// export default function Navbar({ user }) {
//   return (
//     <nav className="bg-white shadow">
//       <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
//         <div className="flex justify-between h-16">
//           <div className="flex">
//             <div className="flex-shrink-0 flex items-center">
//               <Link href="/dashboard" className="text-xl font-bold text-blue-600">
//                 Todo App
//               </Link>
//             </div>
//             <div className="ml-6 flex space-x-8">
//               <Link
//                 href="/dashboard"
//                 className="inline-flex items-center px-1 pt-1 border-b-2 border-transparent text-sm font-medium text-gray-500 hover:text-gray-700 hover:border-gray-300"
//               >
//                 Dashboard
//               </Link>

//               {user?.role === "ADMIN" && (
//                 <>
//                   <Link
//                     href="/admin/users"
//                     className="inline-flex items-center px-1 pt-1 border-b-2 border-transparent text-sm font-medium text-gray-500 hover:text-gray-700 hover:border-gray-300"
//                   >
//                     Manage Users
//                   </Link>
//                   <Link
//                     href="/admin/tasks"
//                     className="inline-flex items-center px-1 pt-1 border-b-2 border-transparent text-sm font-medium text-gray-500 hover:text-gray-700 hover:border-gray-300"
//                   >
//                     Manage Tasks
//                   </Link>
//                 </>
//               )}
//             </div>
//           </div>
//           <div className="flex items-center">
//             <div className="flex-shrink-0">
//               <span className="text-sm text-gray-500 mr-4">
//                 {user?.name} ({user?.role === "ADMIN" ? "Admin" : "User"})
//               </span>
//               <form action={logout}>
//                 <button type="submit" className="px-3 py-1 bg-gray-200 text-gray-700 rounded hover:bg-gray-300">
//                   Logout
//                 </button>
//               </form>
//             </div>
//           </div>
//         </div>
//       </div>
//     </nav>
//   )
// }
