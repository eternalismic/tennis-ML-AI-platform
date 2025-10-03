
import { NextRequest } from "next/server"
import { getServerSession } from "next-auth"
import { authOptions } from "@/lib/auth"
export async function GET(_req: NextRequest) {
  const session = await getServerSession(authOptions)
  // @ts-ignore
  const token: string | undefined = session?.access_token
  const base = process.env.GATEWAY_BASE || process.env.NEXT_PUBLIC_GATEWAY_BASE || "http://localhost:8080"
  const resp = await fetch(`${base}/api/metrics_summary`, { headers: { ...(token ? { Authorization: `Bearer ${token}` } : {}) }, cache: "no-store" })
  if (!resp.ok) return new Response("Bad gateway", { status: 502 })
  const data = await resp.text()
  return new Response(data, { headers: { "Content-Type": "application/json" } })
}
