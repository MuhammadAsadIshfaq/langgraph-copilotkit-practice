// app/layout.js or app/layout.jsx

import { Inter } from "next/font/google";
import "./globals.css";
import Navbar from "@/components/navbar";
import { getSession } from "@/lib/auth"; // or use requireAuth()
import { headers } from "next/headers"; // to get the current pathname
import { CopilotSidebar } from "@copilotkit/react-ui";
import { CopilotKit } from "@copilotkit/react-core";
import "@copilotkit/react-ui/styles.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata = {
  title: "Todo App",
  description: "A Next.js Todo application with admin and user roles",
};

export default async function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
          <CopilotKit runtimeUrl="/api/copilotkit">
            <CopilotSidebar
              defaultOpen={true}
              instructions={
                "You are assisting the user with a Todo application that has two roles: Admin and User. " +
                "The Admin can create users, assign tasks, edit tasks, and manage everything. " +
                "The User can only view tasks assigned to them and update the status of those tasks. " +
                "When the Admin is logged in, they have access to a dashboard with options to 'Manage Users' and 'Manage Tasks'. " +
                "In 'Manage Users', the Admin can add new users. In 'Manage Tasks', the Admin can create tasks, assign them to users, and edit tasks. and make add only one task on one prompt " +
                "Make sure to assist based on the role and available features."
              }
              labels={{
                title: "Sidebar Assistant",
                initial: "How can I help you today?",
              }}
            >
              {children}
            </CopilotSidebar>
          </CopilotKit>{" "}
        </main>
      </body>
    </html>
  );
}

// import { Inter } from "next/font/google";
// import "./globals.css";
// import Navbar from "@/components/navbar";

// const inter = Inter({ subsets: ["latin"] });

// export const metadata = {
//   title: "Todo App",
//   description: "A Next.js Todo application with admin and user roles",
// };

// export default function RootLayout({ children }) {
//   return (
//     <html lang="en">
//       <body className={inter.className}>
//         <Navbar />
//         {children}
//       </body>
//     </html>
//   );
// }
