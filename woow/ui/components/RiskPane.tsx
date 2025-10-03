
'use client'
import React, { useEffect, useState } from 'react'
export default function RiskPane() {
  const [pnl, setPnl] = useState<number | null>(null)
  const [roi, setRoi] = useState<number | null>(null)
  const [orders, setOrders] = useState<number | null>(null)
  useEffect(() => {
    async function poll() {
      try {
        const resp = await fetch('/api/metrics_summary', { cache: 'no-store' })
        const data = await resp.json()
        setPnl(data.pnl_total ?? null); setRoi(data.roi_total ?? null); setOrders(data.orders_placed_total ?? null)
      } catch {}
    }
    poll(); const id = setInterval(poll, 5000); return () => clearInterval(id)
  }, [])
  return (
    <div className="card p-4">
      <h3 className="text-lg font-semibold mb-3">Risk & Performance</h3>
      <div className="grid grid-cols-3 gap-4">
        <div className="p-3 rounded bg-neutral-800"><div className="text-xs text-neutral-400">P/L Total</div><div className="text-2xl font-bold">{pnl !== null ? pnl.toFixed(2) : '—'}</div></div>
        <div className="p-3 rounded bg-neutral-800"><div className="text-xs text-neutral-400">ROI</div><div className="text-2xl font-bold">{roi !== null ? (roi*100).toFixed(2) + '%' : '—'}</div></div>
        <div className="p-3 rounded bg-neutral-800"><div className="text-xs text-neutral-400">Orders placed</div><div className="text-2xl font-bold">{orders !== null ? orders : '—'}</div></div>
      </div>
      <p className="text-xs text-neutral-400 mt-3">Backed by Prometheus via the UI gateway & Next.js proxy.</p>
    </div>
  )
}
