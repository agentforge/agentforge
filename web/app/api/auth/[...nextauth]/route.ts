import NextAuth, { NextAuthOptions } from "next-auth";
import { PrismaAdapter } from "@next-auth/prisma-adapter";
import prisma from "@/lib/prisma";
import GoogleProvider from "next-auth/providers/google";
import CredentialsProvider from "next-auth/providers/credentials";

export const authOptions: NextAuthOptions = {
  adapter: PrismaAdapter(prisma),
  providers: [
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID as string,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET as string,
    }),
    CredentialsProvider({
      id: "password",
      name: "Email and Password",
      credentials: {
        email: { label: "Email", type: "text", placeholder: "john@gmail.com" },
        password: { label: "Password", type: "password" }
      },
      authorize: async (credentials, req) => {
        const user = { id: '1', name: 'J Smith', email: 'test@example.com' };
        if (user) {
          return user;
        } else {
          return null;
        }
      }
    }),
  ],
};

const handler = NextAuth(authOptions);

export { handler as GET, handler as POST };
