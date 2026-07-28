# ResiAgent — Universal Business Resilience Platform

**ResiAgent** deploys a coordinated team of autonomous AI agents to help any business in any country solve the five universal 2026 business headaches:

1. Regulatory & compliance overload
2. Supply-chain volatility & fragmentation
3. ESG / sustainability & climate disclosure pressure
4. Cybersecurity & third-party risk
5. Labor shortages, talent gaps & upskilling

The platform delivers structured **Global Resilience Plans** with ROI estimates, measurable KPIs, and clear next steps.

---

## Current Phase: Phase 2 (Complete)

- ✅ FastAPI backend with `POST /analyze` endpoint
- ✅ Five specialist agents (Compliance, Supply, ESG, Cyber, Talent) with exact system prompts
- ✅ ResiAgentSupervisor that orchestrates all agents
- ✅ Next.js 15 frontend dashboard (Tailwind + clean UI)
- ✅ Strict separation: Python owns all agent logic, Next.js owns the UI

**Phase 2** (next): Full LangGraph supervisor graph + plan history in Supabase.

---

## Tech Stack (Strict)

**Frontend**
- Next.js 15 (App Router)
- Tailwind CSS
- TypeScript

**Backend (AI Core)**
- FastAPI
- LangGraph (ready for Phase 2)
- langchain-openai → FreeLLMAPI (OpenAI-compatible proxy)
- Python type hints

**Shared**
- python-dotenv
- Environment variables only (no hard-coded secrets)

---

## Quick Start (Local)

### 1. Backend (Python)

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# Add your FreeLLMAPI key (already pre-filled in example)

uvicorn main:app --reload
```

### 2. Frontend (Next.js)

```bash
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

---

## Vercel Deployment (Recommended)

1. Push this repo to GitHub (already done on `arena/019faa1e-resiagent`)
2. Go to [vercel.com/new](https://vercel.com/new)
3. Import the repository
4. Set **Root Directory** to `frontend`
5. Add these Environment Variables:
   - `NEXT_PUBLIC_API_URL` → your deployed backend URL (Railway / Render / Fly.io)
   - `NEXT_PUBLIC_SUPABASE_URL`
   - `NEXT_PUBLIC_SUPABASE_ANON_KEY`

Backend can be deployed separately on Railway or Render (recommended for Python + LangGraph).

### 3. Generate Your First Resilience Plan

1. Open the frontend
2. Fill in company details, industry, location, and select pain points
3. Click **"Generate Resilience Plan"**
4. View the professionally structured output following the exact `FINAL_PLAN` format

---

## API Reference

### `POST /analyze`

**Request body:**
```json
{
  "company_name": "Acme Corp",
  "industry": "Manufacturing",
  "size": "Mid-market",
  "location": "Germany",
  "pain_points": ["Regulatory & compliance overload", "ESG / sustainability & climate disclosure pressure"],
  "additional_context": "Exporting to EU markets"
}
```

**Response:** Structured `ResiliencePlan` with:
- Executive Summary
- Key Risks Identified
- Recommended Actions
- Prioritised Timeline
- Monitoring KPIs
- Next Steps & Human Approval Needed

---

## Environment Variables

### Backend (`backend/.env`)
```
FREELLMAPI_API_KEY=your_key
FREELLMAPI_BASE_URL=http://localhost:3001/v1
FREELLMAPI_MODEL=auto
```

### Frontend (`frontend/.env.local`)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## Architecture Rules (Never Violate)

- Python (FastAPI + LangGraph) owns **all** agent logic and plan generation
- Next.js owns the UI, authentication, and dashboard
- All communication happens through clean REST endpoints (`/analyze`)
- Never put heavy agent logic inside Next.js API routes
- Agent system prompts are **frozen** unless explicitly changed by the user

---

## Roadmap

| Phase | Status     | Focus                              |
|-------|------------|------------------------------------|
| 0     | Done       | Core agents + FreeLLMAPI           |
| 1     | ✅ Done    | FastAPI + Next.js dashboard        |
| 2     | Next       | LangGraph supervisor + Supabase    |
| 3     | Future     | Auth, billing, marketplace         |

---

## Contributing

This is the official ResiAgent codebase. All work must follow the strict architecture and prompt rules defined in the system.

---

*Built with excellence for global business resilience — 2026 and beyond.*