'use client';

import { useState } from 'react';

interface BusinessContext {
  company_name: string;
  industry: string;
  size: string;
  location: string;
  pain_points: string[];
  additional_context?: string;
}

interface ResiliencePlan {
  executive_summary: string;
  key_risks_identified: string[];
  recommended_actions: string[];
  prioritised_timeline: string[];
  monitoring_kpis: string[];
  next_steps_human_approval: string[];
}

const HEADACHES = [
  "Regulatory & compliance overload",
  "Supply-chain volatility & fragmentation",
  "ESG / sustainability & climate disclosure pressure",
  "Cybersecurity & third-party risk",
  "Labor shortages, talent gaps & upskilling"
];

export default function ResiAgentDashboard() {
  const [formData, setFormData] = useState<BusinessContext>({
    company_name: '',
    industry: '',
    size: 'SME',
    location: '',
    pain_points: [],
    additional_context: '',
  });
  const [plan, setPlan] = useState<ResiliencePlan | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const togglePainPoint = (point: string) => {
    setFormData(prev => ({
      ...prev,
      pain_points: prev.pain_points.includes(point)
        ? prev.pain_points.filter(p => p !== point)
        : [...prev.pain_points, point]
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.company_name || !formData.industry || !formData.location) {
      setError('Please fill in company name, industry, and location');
      return;
    }

    setLoading(true);
    setError('');
    setPlan(null);

    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });

      if (!res.ok) throw new Error('Failed to generate plan');

      const data: ResiliencePlan = await res.json();
      setPlan(data);
    } catch (err) {
      setError('Error connecting to ResiAgent API. Make sure the backend is running.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-zinc-950 text-white">
      <div className="max-w-5xl mx-auto px-6 py-12">
        {/* Header */}
        <div className="flex items-center justify-between mb-12">
          <div>
            <h1 className="text-5xl font-semibold tracking-tighter">ResiAgent</h1>
            <p className="text-xl text-zinc-400 mt-1">Universal Business Resilience Platform</p>
          </div>
          <div className="px-4 py-1.5 rounded-full bg-zinc-900 text-sm border border-zinc-800">
            Phase 1 • Live
          </div>
        </div>

        {/* Input Form */}
        <div className="bg-zinc-900 border border-zinc-800 rounded-3xl p-8 mb-8">
          <h2 className="text-2xl font-semibold mb-6">Generate Global Resilience Plan</h2>
          
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium mb-2">Company Name</label>
                <input
                  type="text"
                  value={formData.company_name}
                  onChange={(e) => setFormData({ ...formData, company_name: e.target.value })}
                  className="w-full bg-zinc-950 border border-zinc-800 rounded-2xl px-4 py-3 focus:outline-none focus:border-zinc-600"
                  placeholder="Acme Corp"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-2">Industry</label>
                <input
                  type="text"
                  value={formData.industry}
                  onChange={(e) => setFormData({ ...formData, industry: e.target.value })}
                  className="w-full bg-zinc-950 border border-zinc-800 rounded-2xl px-4 py-3 focus:outline-none focus:border-zinc-600"
                  placeholder="Manufacturing, Retail, Fintech..."
                />
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium mb-2">Company Size</label>
                <select
                  value={formData.size}
                  onChange={(e) => setFormData({ ...formData, size: e.target.value })}
                  className="w-full bg-zinc-950 border border-zinc-800 rounded-2xl px-4 py-3 focus:outline-none focus:border-zinc-600"
                >
                  <option value="SME">SME (1-250 employees)</option>
                  <option value="Mid-market">Mid-market (251-2000)</option>
                  <option value="Enterprise">Enterprise (2000+)</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium mb-2">Primary Location / Jurisdiction</label>
                <input
                  type="text"
                  value={formData.location}
                  onChange={(e) => setFormData({ ...formData, location: e.target.value })}
                  className="w-full bg-zinc-950 border border-zinc-800 rounded-2xl px-4 py-3 focus:outline-none focus:border-zinc-600"
                  placeholder="Germany, United States, Singapore..."
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium mb-3">Select Pain Points (the 5 universal 2026 headaches)</label>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                {HEADACHES.map((point) => (
                  <label key={point} className="flex items-center gap-3 bg-zinc-950 border border-zinc-800 rounded-2xl px-4 py-3 cursor-pointer hover:bg-zinc-900">
                    <input
                      type="checkbox"
                      checked={formData.pain_points.includes(point)}
                      onChange={() => togglePainPoint(point)}
                      className="accent-white"
                    />
                    <span className="text-sm">{point}</span>
                  </label>
                ))}
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">Additional Context (optional)</label>
              <textarea
                value={formData.additional_context}
                onChange={(e) => setFormData({ ...formData, additional_context: e.target.value })}
                className="w-full bg-zinc-950 border border-zinc-800 rounded-2xl px-4 py-3 h-24 focus:outline-none focus:border-zinc-600 resize-none"
                placeholder="Any specific regulations, markets, or challenges..."
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-white text-black font-semibold py-4 rounded-2xl hover:bg-zinc-200 transition disabled:opacity-50"
            >
              {loading ? 'Generating Global Resilience Plan...' : 'Generate Resilience Plan'}
            </button>
          </form>

          {error && <p className="text-red-400 mt-4 text-sm">{error}</p>}
        </div>

        {/* Results */}
        {plan && (
          <div className="bg-zinc-900 border border-zinc-800 rounded-3xl p-8">
            <div className="flex items-center justify-between mb-8">
              <h2 className="text-3xl font-semibold">Global Resilience Plan</h2>
              <div className="text-xs px-3 py-1 bg-emerald-900 text-emerald-400 rounded-full">PHASE 1 • STUB</div>
            </div>

            <div className="space-y-8 text-sm">
              <div>
                <h3 className="font-semibold text-lg mb-3 text-zinc-400">Executive Summary</h3>
                <p className="leading-relaxed text-zinc-300">{plan.executive_summary}</p>
              </div>

              <div>
                <h3 className="font-semibold text-lg mb-3 text-zinc-400">Key Risks Identified</h3>
                <ul className="space-y-2">
                  {plan.key_risks_identified.map((risk, i) => (
                    <li key={i} className="flex gap-3"><span className="text-zinc-500">•</span> {risk}</li>
                  ))}
                </ul>
              </div>

              <div>
                <h3 className="font-semibold text-lg mb-3 text-zinc-400">Recommended Actions</h3>
                <ul className="space-y-2">
                  {plan.recommended_actions.map((action, i) => (
                    <li key={i} className="flex gap-3"><span className="text-emerald-400">→</span> {action}</li>
                  ))}
                </ul>
              </div>

              <div>
                <h3 className="font-semibold text-lg mb-3 text-zinc-400">Prioritised Timeline</h3>
                <ul className="space-y-2">
                  {plan.prioritised_timeline.map((item, i) => (
                    <li key={i} className="flex gap-3"><span className="text-amber-400">•</span> {item}</li>
                  ))}
                </ul>
              </div>

              <div>
                <h3 className="font-semibold text-lg mb-3 text-zinc-400">Monitoring KPIs</h3>
                <ul className="space-y-2">
                  {plan.monitoring_kpis.map((kpi, i) => (
                    <li key={i} className="flex gap-3"><span className="text-blue-400">•</span> {kpi}</li>
                  ))}
                </ul>
              </div>

              <div>
                <h3 className="font-semibold text-lg mb-3 text-zinc-400">Next Steps &amp; Human Approval Needed</h3>
                <ul className="space-y-2">
                  {plan.next_steps_human_approval.map((step, i) => (
                    <li key={i} className="flex gap-3"><span className="text-purple-400">•</span> {step}</li>
                  ))}
                </ul>
              </div>
            </div>

            <div className="mt-10 pt-8 border-t border-zinc-800 text-xs text-zinc-500">
              This is a Phase 1 structured plan. Full multi-agent LangGraph orchestration coming in Phase 2.
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
