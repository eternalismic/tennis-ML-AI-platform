
import McpCenter from '@/components/McpCenter'
import DecisionFeed from '@/components/DecisionFeed'
import RiskPane from '@/components/RiskPane'
export default function Page() {
  return (
    <main className="space-y-4">
      <McpCenter />
      <div className="grid grid-cols-1 xl:grid-cols-3 gap-4">
        <DecisionFeed />
        <RiskPane />
        <div className="card p-4">
          <h3 className="text-lg font-semibold">Notes</h3>
          <p className="text-sm text-neutral-300">This UI centers the <b>MCP interaction</b>—players, probabilities, fair odds, edge, and the live recommendation. Use the knobs to preview decisions via a secure server proxy.</p>
        </div>
      </div>
    </main>
  )
}
