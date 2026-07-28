from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv

from agents.supervisor import ResiAgentSupervisor

load_dotenv()

app = FastAPI(
    title="ResiAgent API",
    description="Universal Business Resilience Platform - Phase 1",
    version="0.1.0"
)

supervisor = ResiAgentSupervisor()


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
    Phase 1 endpoint powered by ResiAgentSupervisor.
    All five specialist agents are invoked and the final structured plan is returned.
    Full LangGraph graph will be added in Phase 2.
    """
    context_dict = context.model_dump()
    plan_data = supervisor.generate_plan(context_dict)
    
    return ResiliencePlan(**plan_data)


@app.get("/health")
async def health_check():
    return {"status": "healthy", "phase": "1", "service": "ResiAgent API"}