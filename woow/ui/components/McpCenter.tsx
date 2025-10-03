
'use client'
import React, { useEffect, useMemo, useState } from 'react'
import { Area, AreaChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
type Ev = { ts: number; kind: string; payload: any }
export default function McpCenter() {
  const [events, setEvents] = useState<Ev[]>([])
  const [edgeThreshold, setEdgeThreshold] = useState(0.05)
  const [riskPct, setRiskPct] = useState(0.01)
  useEffect(() => {
    const url = process.env.NEXT_PUBLIC_SSE_URL || '/api/sse'
    const src = new EventSource(url)
    src.onmessage = (e) => { try { const obj = JSON.parse(e.data); setEvents(prev => [...prev.slice(-499), obj]) } catch {} }
    return () => src.close()
  }, [])
  const lastEval = useMemo(() => [...events].reverse().find(e => e.kind === 'mcp_evaluation'), [events])
  const edgeSeries = useMemo(() => events.filter(e => e.kind === 'mcp_evaluation').map(e => ({ ts: new Date(e.ts*1000).toLocaleTimeString(), edge: e.payload.edge ?? 0 })), [events])
  const fair = lastEval?.payload?.fair_odds
  const probs = lastEval?.payload?.probs
  const players = lastEval?.payload?.players || ['—','—']
  const rec = lastEval?.payload?.rec || '—'
  async function preview() {
    const resp = await fetch('/api/simulate', { method: 'POST', headers: { 'Content-Type':'application/json' }, body: JSON.stringify({ edgeThreshold, maxRiskPct: riskPct, bankroll: 1000, limit: 15 }) })
    const data = await resp.json()
    alert(`Preview decisions: ${data.count} (edge≥${edgeThreshold}, maxRisk=${riskPct})`)
  }
  return (
    <div className="grid grid-cols-1 xl:grid-cols-3 gap-4">
      <div className="card p-4 xl:col-span-2">
        <div className="flex justify-between items-center mb-3">
          <h2 className="text-xl font-semibold">MCP Interaction</h2>
          <span className="text-sm text-neutral-400">Live evaluations</span>
        </div>
        <div className="grid grid-cols-2 gap-4">
          <div className="card p-4">
            <div className="text-sm text-neutral-400">Players</div>
            <div className="text-2xl font-bold">{players[0]} <span className="text-neutral-500">vs</span> {players[1]}</div>
            <div className="mt-4 grid grid-cols-2 gap-4">
              <div>
                <div className="text-xs text-neutral-400">Fair {players[0]}</div>
                <div className="text-xl">{fair ? fair.A.toFixed(2) : '—'}</div>
                <div className="text-xs text-neutral-400">p(A)</div>
                <div className="text-lg">{probs ? (probs.A*100).toFixed(1) + '%' : '—'}</div>
              </div>
              <div>
                <div className="text-xs text-neutral-400">Fair {players[1]}</div>
                <div className="text-xl">{fair ? fair.B.toFixed(2) : '—'}</div>
                <div className="text-xs text-neutral-400">p(B)</div>
                <div className="text-lg">{probs ? (probs.B*100).toFixed(1) + '%' : '—'}</div>
              </div>
            </div>
            <div className="mt-4">
              <div className="text-xs text-neutral-400">Recommendation</div>
              <div className="text-2xl">{rec}</div>
            </div>
          </div>
          <div className="card p-4">
            <div className="text-sm text-neutral-400 mb-2">Edge over time</div>
            <div className="h-40">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={edgeSeries}>
                  <defs>
                    <linearGradient id="g" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#2563eb" stopOpacity={0.8}/>
                      <stop offset="95%" stopColor="#2563eb" stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <XAxis dataKey="ts" hide/>
                  <YAxis domain={[-0.2, 0.5]} />
                  <Tooltip />
                  <Area type="monotone" dataKey="edge" stroke="#2563eb" fillOpacity={1} fill="url(#g)" />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>
      </div>
      <div className="card p-4">
        <h3 className="text-lg font-semibold mb-3">Interact</h3>
        <div className="space-y-4">
          <div>
            <div className="flex justify-between text-sm"><span>Edge threshold</span><span className="text-neutral-400">{(edgeThreshold*100).toFixed(1)}%</span></div>
            <input type="range" min="0.0" max="0.20" step="0.01" value={edgeThreshold} onChange={e=>setEdgeThreshold(parseFloat(e.target.value))} className="w-full"/>
          </div>
          <div>
            <div className="flex justify-between text-sm"><span>Max risk %</span><span className="text-neutral-400">{(riskPct*100).toFixed(2)}%</span></div>
            <input type="range" min="0.0025" max="0.05" step="0.0025" value={riskPct} onChange={e=>setRiskPct(parseFloat(e.target.value))} className="w-full"/>
          </div>
          <button className="btn w-full" onClick={preview}>Preview decisions</button>
          <p className="text-xs text-neutral-400">This panel lets you explore how thresholds change recommendations.</p>
        </div>
      </div>
    </div>
  )
}
