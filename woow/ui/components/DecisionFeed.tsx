
'use client'
import React, { useEffect, useState } from 'react'
type Ev = { ts: number; kind: string; payload: any }
export default function DecisionFeed() {
  const [events, setEvents] = useState<Ev[]>([])
  useEffect(() => {
    const url = process.env.NEXT_PUBLIC_SSE_URL || '/api/sse'
    const src = new EventSource(url)
    src.onmessage = (e) => {
      try { const obj = JSON.parse(e.data); if (obj.kind === 'order_placed' || obj.kind === 'mcp_evaluation') { setEvents(prev => [obj, ...prev].slice(0, 15)) } } catch {}
    }
    return () => src.close()
  }, [])
  return (
    <div className="card p-4">
      <div className="flex justify-between items-center mb-2"><h3 className="text-lg font-semibold">Decision Feed</h3><span className="text-xs text-neutral-400">latest 15</span></div>
      <div className="space-y-2 max-h-80 overflow-auto">
        {events.map((e, idx) => (
          <div key={idx} className="border border-neutral-800 rounded p-2">
            <div className="text-xs text-neutral-400">{new Date(e.ts*1000).toLocaleTimeString()} · {e.kind}</div>
            <div className="text-sm">{e.kind === 'order_placed' ? (<span>Order: {e.payload.side} {e.payload.player} {e.payload.size}@{e.payload.price} (mkt {e.payload.market_id})</span>) : (<span>Eval: {e.payload.players?.join(' vs ')} · edge {(e.payload.edge ?? 0).toFixed(3)} · rec {e.payload.rec}</span>)}</div>
          </div>
        ))}
      </div>
    </div>
  )
}
