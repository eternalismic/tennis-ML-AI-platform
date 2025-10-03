
import { NextRequest } from "next/server"
import { getServerSession } from "next-auth"
import { authOptions } from "@/lib/auth"
export async function POST(req: NextRequest) {
  const session = await getServerSession(authOptions)
  // @ts-ignore
  const token: string | undefined = session?.access_token
  const body = await req.text()
  const base = process.env.GATEWAY_BASE || process.env.NEXT_PUBLIC_GATEWAY_BASE || "http://localhost:8080"
  const resp = await fetch(`${base}/simulate`, { method: "POST", headers: { "Content-Type": "application/json", ...(token ? { Authorization: `Bearer ${token}` } : {}) }, body })
  const text = await resp.text()
  return new Response(text, { status: resp.status, headers: { "Content-Type": "application/json" } })
}
