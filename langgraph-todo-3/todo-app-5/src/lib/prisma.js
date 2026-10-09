import { PrismaClient } from "@prisma/client"

const globalForPrisma = globalThis

const prisma = globalForPrisma.prisma ?? new PrismaClient()

if (process.env.NODE_ENV !== "production") globalForPrisma.prisma = prisma

export default prisma



// import { PrismaClient } from '@prisma/client'

// // Prevent multiple instances of Prisma Client in development
// const prismaClientSingleton = () => {
//   try {
//     return new PrismaClient()
//   } catch (error) {
//     console.error('Failed to initialize Prisma Client:', error)
//     // Return a mock PrismaClient to prevent crashes
//     return {}
//   }
// }

// const globalForPrisma = global

// export const prisma = globalForPrisma.prisma ?? prismaClientSingleton()

// if (process.env.NODE_ENV !== 'production') globalForPrisma.prisma = prisma

// export default prisma