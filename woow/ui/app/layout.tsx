
import './globals.css'
import React from 'react'
import LoginBar from '@/components/LoginBar'
export const metadata = { title: 'Tennis MCP Console', description: 'Live decision console' }
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (<html lang="en"><body><div className="max-w-7xl mx-auto p-4"><div className="flex items-center justify-between mb-4"><h1 className="text-2xl font-bold">Tennis MCP Console</h1><LoginBar /></div>{children}</div></body></html>)
}
