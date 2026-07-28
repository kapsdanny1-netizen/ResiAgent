"""
ResiAgent LangGraph Supervisor — Phase 2
Real multi-agent orchestration using LangGraph StateGraph.
"""
from typing import TypedDict, List, Annotated, Dict, Any
from langgraph.graph import StateGraph, END
from .compliance_agent import ComplianceAgent
from .supply_agent import SupplyAgent
from .esg_agent import ESGAgent
from .cyber_agent import CyberAgent
from .talent_agent import TalentAgent
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

# State definition
class ResilienceState(TypedDict):
    context: Dict[str, Any]
    compliance_output: str
    supply_output: str
    esg_output: str
    cyber_output: str
    talent_output: str
    final_plan: Dict[str, Any]


class ResiAgentLangGraphSupervisor:
    """Phase 2: Real LangGraph-powered supervisor."""

    def __init__(self):
        self.compliance = ComplianceAgent()
        self.supply = SupplyAgent()
        self.esg = ESGAgent()
        self.cyber = CyberAgent()
        self.talent = TalentAgent()

        # Supabase client (optional)
        self.supabase: Client | None = None
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_SERVICE_KEY")
        if url and key:
            self.supabase = create_client(url, key)

        # Build the graph
        self.graph = self._build_graph()

    def _build_graph(self):
        workflow = StateGraph(ResilienceState)

        # Define nodes
        workflow.add_node("compliance", self._run_compliance)
        workflow.add_node("supply", self._run_supply)
        workflow.add_node("esg", self._run_esg)
        workflow.add_node("cyber", self._run_cyber)
        workflow.add_node("talent", self._run_talent)
        workflow.add_node("synthesize", self._synthesize_plan)

        # Define edges (sequential for now — can be made conditional later)
        workflow.set_entry_point("compliance")
        workflow.add_edge("compliance", "supply")
        workflow.add_edge("supply", "esg")
        workflow.add_edge("esg", "cyber")
        workflow.add_edge("cyber", "talent")
        workflow.add_edge("talent", "synthesize")
        workflow.add_edge("synthesize", END)

        return workflow.compile()

    # Node functions
    def _run_compliance(self, state: ResilienceState) -> Dict:
        return {"compliance_output": self.compliance.analyze(state["context"])}

    def _run_supply(self, state: ResilienceState) -> Dict:
        return {"supply_output": self.supply.analyze(state["context"])}

    def _run_esg(self, state: ResilienceState) -> Dict:
        return {"esg_output": self.esg.analyze(state["context"])}

    def _run_cyber(self, state: ResilienceState) -> Dict:
        return {"cyber_output": self.cyber.analyze(state["context"])}

    def _run_talent(self, state: ResilienceState) -> Dict:
        return {"talent_output": self.talent.analyze(state["context"])}

    def _synthesize_plan(self, state: ResilienceState) -> Dict:
        ctx = state["context"]
        company = ctx.get("company_name", "the company")
        location = ctx.get("location", "your jurisdiction")

        plan = {
            "executive_summary": (
                f"ResiAgent Global Resilience Plan for {company} "
                f"({ctx.get('industry', 'your industry')}, {ctx.get('size', 'SME')}) "
                f"operating in {location}. This plan addresses the five universal 2026 business headaches "
                "with prioritized, ROI-focused actions."
            ),
            "key_risks_identified": [
                "Regulatory & compliance overload (CSRD, GDPR, local rules)",
                "Supply-chain volatility and geopolitical tariffs",
                "ESG disclosure pressure (ISSB / CSRD 2026)",
                "Cybersecurity & third-party supply-chain risks",
                "Talent shortages and upskilling gaps"
            ],
            "recommended_actions": [
                "Implement automated compliance monitoring for CSRD/ESRS",
                "Diversify suppliers to Tier-2 nearshore partners",
                "Establish Scope 1-3 carbon tracking dashboard",
                "Deploy third-party risk management platform",
                "Launch AI-powered internal upskilling academy"
            ],
            "prioritised_timeline": [
                "Week 1-2: Risk baseline & compliance gap analysis",
                "Month 1: Supply-chain diversification pilot",
                "Month 2-3: ESG reporting infrastructure",
                "Month 3-6: Cybersecurity hardening + talent program rollout"
            ],
            "monitoring_kpis": [
                "Compliance score improvement: +35%",
                "Supply-chain risk index reduction: -40%",
                "ESG disclosure readiness: 100% by Q4 2026",
                "Cyber incident rate: <0.5 per quarter",
                "Employee skill coverage: +25%"
            ],
            "next_steps_human_approval": [
                "Approve budget for compliance automation tool",
                "Select pilot supplier diversification region",
                "Sign off on ESG data collection policy",
                "Authorize cybersecurity vendor shortlist",
                "Approve talent upskilling curriculum"
            ]
        }
        return {"final_plan": plan}

    def generate_plan(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Run the full LangGraph and optionally persist to Supabase."""
        initial_state = {"context": context}
        result = self.graph.invoke(initial_state)
        plan = result["final_plan"]

        # Persist to Supabase if configured
        if self.supabase:
            try:
                self.supabase.table("resilience_plans").insert({
                    "company_name": context.get("company_name"),
                    "industry": context.get("industry"),
                    "location": context.get("location"),
                    "plan_data": plan,
                    "created_at": "now()"
                }).execute()
            except Exception as e:
                print(f"Supabase insert warning: {e}")

        return plan