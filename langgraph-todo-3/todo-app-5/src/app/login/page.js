import { getSession } from "@/lib/auth";
import { login, seedDatabase } from "@/lib/actions";
import { redirect } from "next/navigation";
import { SubmitButton } from "@/components/ui-components";
import { LoginForm } from "@/components/login-form";

export default async function LoginPage() {
  // const user = await getSession();

  // if (user) {
  //   redirect("/dashboard");
  //   return <p className="text-center mt-10">Redirecting...</p>; // optional
  // }
  return (
    <div className="flex min-h-svh flex-col items-center justify-center bg-muted p-6 md:p-10">
      <div className="w-full max-w-md">
        <LoginForm />
      </div>
    </div>
  );

  // return (
  //   <div className="min-h-screen flex items-center justify-center bg-gray-50">
  //     <div className="max-w-md w-full space-y-8 p-8 bg-white rounded-lg shadow">
  //       <div>
  //         <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">App Login</h2>
  //       </div>

  //       <form action={login} className="mt-8 space-y-6">
  //         <div className="rounded-md shadow-sm -space-y-px">
  //           <div>
  //             <label htmlFor="email" className="sr-only">
  //               Email address
  //             </label>
  //             <input
  //               id="email"
  //               name="email"
  //               type="email"
  //               autoComplete="email"
  //               required
  //               className="mb-5 appearance-none rounded relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm"
  //               placeholder="Email address"
  //             />
  //           </div>
  //           <div className="mb-4">
  //             <label htmlFor="password" className="sr-only" >
  //               Password
  //             </label>
  //             <input
  //               id="password"
  //               name="password"
  //               type="password"
  //               autoComplete="current-password"
  //               required
  //               className="appearance-none rounded relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm"
  //               placeholder="Password"
  //             />
  //           </div>
  //         </div>

  //         <div>
  //           <SubmitButton className="w-full">Sign in</SubmitButton>
  //         </div>
  //       </form>

  //       <div className="mt-6">
  //         <div className="relative">
  //           <div className="absolute inset-0 flex items-center">
  //             <div className="w-full border-t border-gray-300"></div>
  //           </div>
  //           <div className="relative flex justify-center text-sm">
  //             <span className="px-2 bg-white text-gray-500">First time here?</span>
  //           </div>
  //         </div>

  //         <div className="mt-4 text-xs text-gray-500">
  //           <p>you can log in with your email and password:</p>
  //           <p className="mt-1">
  //             <strong>Admin:</strong> admin@example.com / admin123
  //           </p>
  //           <p>
  //             <strong>User:</strong> john@example.com / password123
  //           </p>
  //         </div>
  //       </div>
  //     </div>
  //   </div>
  // )
}
