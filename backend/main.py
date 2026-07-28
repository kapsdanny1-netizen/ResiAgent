from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv

from agents.langgraph_supervisor import ResiAgentLangGraphSupervisor

load_dotenv()

app = FastAPI(
    title="ResiAgent API",
    description="Universal Business Resilience Platform - Phase 2 (LangGraph)",
    version="0.2.0"
)

supervisor = ResiAgentLangGraphSupervisor()


class BusinessContext(BaseModel):
    company_name: str
    industry: str
    size: str  # e.g. "SME", "Mid-market", "Enterprise"
    location: str  # Country / jurisdiction
    pain_points: List[str]  # subset of the 5 headaches
    additional_context: Optional[str] = None


class ResiliencePlan(BaseModel):
    executive_summary: str
    key_risks_identified: List[str]
    recommended_actions: List[str]
    prioritised_timeline: List[str]
    monitoring_kpis: List[str]
    next_steps_human_approval: List[str]


@app.post("/analyze", response_model=ResiliencePlan)
async def analyze_business(context: BusinessContext):
    """
    Phase 2 endpoint powered by ResiAgentLangGraphSupervisor.
    Real LangGraph StateGraph orchestration of all five specialist agents.
    Plans are automatically persisted to Supabase when configured.
    """
    context_dict = context.model_dump()
    plan_data = supervisor.generate_plan(context_dict)
    
    return ResiliencePlan(**plan_data)


@app.get("/health")
async def health_check():
    return {"status": "healthy", "phase": "1", "service": "ResiAgent API"}