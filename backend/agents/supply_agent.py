"""
Supply Chain Agent — Global Supply Chain Resilience Specialist
"""
from typing import Dict, Any


class SupplyAgent:
    """Global Supply Chain Resilience Specialist Agent for ResiAgent."""

    SYSTEM_PROMPT = """You are the Global Supply Chain Resilience Specialist Agent.

Expert in geopolitical tariffs, critical minerals, cyber supply-chain attacks, climate, labor, nearshoring.

Use analyze_supply_risk tool.

Output exactly:
**Current Supply Risks**
**Recommended Sourcing & Diversification Changes**
**Cost Savings & Resilience Opportunities**
**Risk Mitigation Plan**"""

    def analyze(self, context: Dict[str, Any]) -> str:
        location = context.get("location", "global")
        industry = context.get("industry", "your industry")

        return f"""**Current Supply Risks**
- Heavy reliance on single-region suppliers exposed to geopolitical tariffs
- Cyber supply-chain attack surface in Tier-2/3 vendors
- Climate and labor disruption risk in key sourcing countries

**Recommended Sourcing & Diversification Changes**
- Qualify 2–3 nearshore suppliers in {location} region or friendly jurisdictions
- Implement dual-sourcing for top 20% of spend categories
- Add supply-chain mapping and Tier-2 visibility

**Cost Savings & Resilience Opportunities**
- 12–18% logistics and tariff cost reduction via nearshoring
- Reduced single-point-of-failure risk (estimated 35% lower disruption probability)

**Risk Mitigation Plan**
- Quarterly supplier risk scoring + cyber due diligence
- Establish 90-day inventory buffer for critical components
- Create supplier diversification roadmap with phased rollout"""