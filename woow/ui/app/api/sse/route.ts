
import { NextRequest } from "next/server"
import { getServerSession } from "next-auth"
import { authOptions } from "@/lib/auth"
export const runtime = "nodejs"
export const dynamic = "force-dynamic"
export async function GET(_req: NextRequest) {
  const session = await getServerSession(authOptions)
  // @ts-ignore
  const token: string | undefined = session?.access_token
  const base = process.env.GATEWAY_BASE || process.env.NEXT_PUBLIC_GATEWAY_BASE || "http://localhost:8080"
  const res = await fetch(`${base}/api/events`, { headers: { ...(token ? { Authorization: `Bearer ${token}` } : {}) } })
  if (!res.ok || !res.body) return new Response("Upstream SSE unavailable", { status: 502 })
  const headers = new Headers({ "Content-Type": "text/event-stream", "Cache-Control": "no-cache, no-transform", "Connection": "keep-alive", "X-Accel-Buffering": "no", "x-vercel-no-compression": "1" })
  return new Response(res.body, { headers })
}
