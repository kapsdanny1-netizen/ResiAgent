from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv
from agents.langgraph_supervisor import ResiAgentLangGraphSupervisor

load_dotenv()

app = FastAPI(
    title="ResiAgent API",
    description="Universal Business Resilience Platform - Phase 3 (Auth + History)",
    version="0.3.0"
)

supervisor = ResiAgentLangGraphSupervisor()


class BusinessContext(BaseModel):
    company_name: str
    industry: str
    size: str
    location: str
    pain_points: List[str]
    additional_context: Optional[str] = None
    user_id: Optional[str] = None


class ResiliencePlan(BaseModel):
    executive_summary: str
    key_risks_identified: List[str]
    recommended_actions: List[str]
    prioritised_timeline: List[str]
    monitoring_kpis: List[str]
    next_steps_human_approval: List[str]


@app.post("/analyze", response_model=ResiliencePlan)
async def analyze_business(context: BusinessContext):
    """Phase 3 endpoint — LangGraph + Supabase persistence"""
    context_dict = context.model_dump()
    plan_data = supervisor.generate_plan(context_dict)
    return ResiliencePlan(**plan_data)


@app.get("/plans/{user_id}")
async def get_user_plans(user_id: str):
    """Fetch all resilience plans for a user (Phase 3)"""
    if not supervisor.supabase:
        raise HTTPException(status_code=503, detail="Supabase not configured")

    try:
        result = supervisor.supabase.table("resilience_plans").select("*").eq("user_id", user_id).order("created_at", desc=True).execute()
        return result.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    return {"status": "healthy", "phase": "3", "service": "ResiAgent API"}