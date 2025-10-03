
import Auth0Provider from "next-auth/providers/auth0"
import KeycloakProvider from "next-auth/providers/keycloak"
import type { NextAuthOptions } from "next-auth"
const provider = process.env.AUTH_PROVIDER || "auth0"
export const authOptions: NextAuthOptions = {
  providers: [
    provider === "keycloak"
      ? KeycloakProvider({ clientId: process.env.OIDC_CLIENT_ID!, clientSecret: process.env.OIDC_CLIENT_SECRET!, issuer: process.env.OIDC_ISSUER_URL })
      : Auth0Provider({ clientId: process.env.OIDC_CLIENT_ID!, clientSecret: process.env.OIDC_CLIENT_SECRET!, issuer: process.env.OIDC_ISSUER_URL })
  ],
  session: { strategy: "jwt" },
  callbacks: {
    async jwt({ token, account }) { if (account?.access_token) { /* @ts-ignore */ token.access_token = account.access_token } return token },
    async session({ session, token }) { /* @ts-ignore */ session.access_token = token.access_token; return session }
  }
}
