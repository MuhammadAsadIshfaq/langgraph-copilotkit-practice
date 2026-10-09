import { NextResponse } from "next/server";

export function middleware(request) {
  const path = request.nextUrl.pathname;
  const isPublicPath = path === "/login";
  const token = request.cookies.get("userId")?.value || "";
  console.log("Token is ------", token);

  if (path === "/" && token) {
    return NextResponse.redirect(new URL("/dashboard", request.url));
  }

  if (isPublicPath && token) {
    return NextResponse.redirect(new URL("/dashboard", request.url));
  }

  if (!isPublicPath && !token) {
    return NextResponse.redirect(new URL("/login", request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/", "/login", "/dashboard", "/admin", "/users", "/tasks"],
};

// import { NextResponse } from "next/server";
// import { getSession } from "@/lib/auth";

// /**
//  * Middleware to handle routing based on authentication.
//  * - Redirects unauthenticated users to `/login`
//  * - Forces logout if authenticated user visits `/login` or unknown routes
//  */
// export function middleware(request) {
//   const userId = request.cookies.get("userId")?.value;
//   const pathname = request.nextUrl.pathname;

//   const isLoginPage = pathname === "/login";

//   const isStaticAsset =
//     pathname.startsWith("/_next") ||
//     pathname.startsWith("/favicon.ico") ||
//     pathname.match(/\.(svg|png|jpg|jpeg|webp|css|js|ico)$/);

//   const isApi = pathname.startsWith("/api");

//   // Allow static assets and API
//   if (isStaticAsset || isApi) {
//     return NextResponse.next();
//   }

//   //   const user = getSession();

//   //   if (user) {
//   //     redirect("/dashboard");
//   //     return <p className="text-center mt-10">Redirecting...</p>; // optional
//   //   }

//   // If authenticated user visits /login — log out and redirect
//   if (userId && isLoginPage) {
//     const response = NextResponse.redirect(new URL("/dashboard", request.url));
//     // response.cookies.delete("userId");
//     return response;
//   }

//   // If authenticated user visits unknown route — log out and redirect
//   const allowedRoutes = ["/dashboard", "/admin", "/tasks", "/users"];
//   const isAllowedRoute = allowedRoutes.some((route) =>
//     pathname.startsWith(route)
//   );

//   if (userId && !isLoginPage && !isAllowedRoute) {
//     const response = NextResponse.redirect(new URL("/dashboard", request.url));
//     // response.cookies.delete("userId");
//     return response;
//   }

//   // If unauthenticated user tries to access anything but /login
//   if (!userId && !isLoginPage) {
//     return NextResponse.redirect(new URL("/login", request.url));
//   }

//   return NextResponse.next();
// }
// export const config = {
//   matcher: ["/((?!_next/static|_next/image|favicon.ico|api).*)"],
// };
