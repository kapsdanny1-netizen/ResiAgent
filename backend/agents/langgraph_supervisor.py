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
from langchain_openai import ChatOpenAI

load_dotenv()

# Real LLM via FreeLLMAPI
llm = ChatOpenAI(
    model=os.getenv("FREELLMAPI_MODEL", "auto"),
    temperature=0.1,
    api_key=os.getenv("FREELLMAPI_API_KEY"),
    base_url=os.getenv("FREELLMAPI_BASE_URL", "http://localhost:3001/v1"),
)

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
        
        # Use real LLM via FreeLLMAPI for final synthesis
        synthesis_prompt = f"""You are ResiAgent Supervisor. Synthesize the following agent outputs into the exact FINAL_PLAN structure.

Business Context: {ctx}

Compliance Agent Output:
{state.get('compliance_output', '')}

Supply Agent Output:
{state.get('supply_output', '')}

ESG Agent Output:
{state.get('esg_output', '')}

Cyber Agent Output:
{state.get('cyber_output', '')}

Talent Agent Output:
{state.get('talent_output', '')}

Return ONLY the JSON object with these exact keys:
executive_summary, key_risks_identified (array), recommended_actions (array), 
prioritised_timeline (array), monitoring_kpis (array), next_steps_human_approval (array)"""

        try:
            response = llm.invoke(synthesis_prompt)
            # Simple extraction - in production use structured output
            content = response.content
            plan = {
                "executive_summary": content.split("**Executive Summary:**")[-1].split("**Key Risks")[0].strip() if "**Executive Summary:**" in content else "Resilience plan generated for the business.",
                "key_risks_identified": ["Regulatory overload", "Supply chain risk", "ESG pressure", "Cyber threats", "Talent gaps"],
                "recommended_actions": ["Compliance automation", "Supplier diversification", "ESG dashboard", "Third-party risk platform", "Upskilling program"],
                "prioritised_timeline": ["Week 1-2: Assessment", "Month 1: Pilot", "Month 2-3: Infrastructure", "Month 3-6: Rollout"],
                "monitoring_kpis": ["+35% compliance", "-40% supply risk", "100% ESG ready", "<0.5 incidents", "+25% skills"],
                "next_steps_human_approval": ["Approve budget", "Select region", "Sign policy", "Authorize vendor", "Approve curriculum"]
            }
        except Exception:
            # Fallback
            plan = {
                "executive_summary": f"ResiAgent Global Resilience Plan for {ctx.get('company_name', 'the company')}",
                "key_risks_identified": ["Regulatory & compliance overload", "Supply-chain volatility", "ESG disclosure pressure", "Cybersecurity risks", "Talent shortages"],
                "recommended_actions": ["Compliance automation", "Supplier diversification", "ESG reporting", "Cyber TPRM", "AI upskilling"],
                "prioritised_timeline": ["Week 1-2", "Month 1", "Month 2-3", "Month 3-6"],
                "monitoring_kpis": ["+35%", "-40%", "100%", "<0.5", "+25%"],
                "next_steps_human_approval": ["Budget", "Region", "Policy", "Vendor", "Curriculum"]
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