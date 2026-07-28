'use client'

import { useEffect, useState } from 'react'
import { supabase } from '@/lib/supabase'
import { useRouter } from 'next/navigation'

interface Plan {
  id: string
  company_name: string
  industry: string
  location: string
  plan_data: any
  created_at: string
}

export default function MyPlans() {
  const [plans, setPlans] = useState<Plan[]>([])
  const [loading, setLoading] = useState(true)
  const router = useRouter()

  useEffect(() => {
    const fetchPlans = async () => {
      const { data: { user } } = await supabase.auth.getUser()
      if (!user) {
        router.push('/login')
        return
      }

      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/plans/${user.id}`)
      if (res.ok) {
        const data = await res.json()
        setPlans(data)
      }
      setLoading(false)
    }

    fetchPlans()
  }, [router])

  if (loading) return <div className="p-12 text-center">Loading your plans...</div>

  return (
    <div className="max-w-5xl mx-auto px-6 py-12">
      <h1 className="text-4xl font-semibold mb-8">My Resilience Plans</h1>

      {plans.length === 0 ? (
        <p className="text-zinc-400">No plans yet. Generate your first one from the dashboard.</p>
      ) : (
        <div className="space-y-4">
          {plans.map((plan) => (
            <div key={plan.id} className="bg-zinc-900 border border-zinc-800 rounded-3xl p-6">
              <div className="flex justify-between items-start">
                <div>
                  <h3 className="font-semibold text-xl">{plan.company_name}</h3>
                  <p className="text-sm text-zinc-400">{plan.industry} • {plan.location}</p>
                </div>
                <div className="text-xs text-zinc-500">
                  {new Date(plan.created_at).toLocaleDateString()}
                </div>
              </div>
              <div className="mt-4 text-sm text-emerald-400">
                {plan.plan_data.executive_summary?.slice(0, 160)}...
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}