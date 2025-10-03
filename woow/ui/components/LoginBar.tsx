
'use client'
import React from 'react'
import { signIn, signOut, useSession } from 'next-auth/react'
export default function LoginBar() {
  const { data: session, status } = useSession()
  if (status === 'loading') return <div className="text-sm text-neutral-400">Loading…</div>
  return (
    <div className="flex items-center gap-3">
      {session?.user ? (<><span className="text-sm text-neutral-300">Hi, {session.user.name ?? 'user'}</span><button className="btn" onClick={() => signOut()}>Sign out</button></>)
        : (<button className="btn" onClick={() => signIn()}>Sign in</button>)}
    </div>
  )
}
