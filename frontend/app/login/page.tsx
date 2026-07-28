'use client'

import { useState } from 'react'
import { supabase } from '@/lib/supabase'

export default function Login() {
  const [email, setEmail] = useState('')
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState('')

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    const { error } = await supabase.auth.signInWithOtp({ email })
    
    if (error) {
      setMessage(error.message)
    } else {
      setMessage('Check your email for the magic link!')
    }
    setLoading(false)
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-zinc-950 text-white">
      <div className="max-w-md w-full p-8 bg-zinc-900 rounded-3xl border border-zinc-800">
        <h1 className="text-3xl font-semibold mb-2">Sign in to ResiAgent</h1>
        <p className="text-zinc-400 mb-8">Access your resilience plans and history</p>

        <form onSubmit={handleLogin} className="space-y-4">
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="you@company.com"
            className="w-full bg-zinc-950 border border-zinc-800 rounded-2xl px-4 py-3"
            required
          />
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-white text-black py-3 rounded-2xl font-semibold disabled:opacity-50"
          >
            {loading ? 'Sending magic link...' : 'Send magic link'}
          </button>
        </form>

        {message && <p className="mt-4 text-sm text-center text-zinc-400">{message}</p>}
      </div>
    </div>
  )
}