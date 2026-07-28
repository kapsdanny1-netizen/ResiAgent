"""
ESG Agent — Global ESG & Sustainability Specialist
"""
from typing import Dict, Any


class ESGAgent:
    """Global ESG & Sustainability Specialist Agent for ResiAgent."""

    SYSTEM_PROMPT = """You are the Global ESG & Sustainability Specialist Agent.

Expert in ISSB, GRI, EU CSRD, Scope 1-3, CSDDD, investor pressure.

Output exactly:
**ESG Risk Assessment**
**Reporting & Disclosure Requirements (2026)**
**Improvement Opportunities**
**Investor & Stakeholder Appeal Actions**"""

    def analyze(self, context: Dict[str, Any]) -> str:
        location = context.get("location", "global")

        return f"""**ESG Risk Assessment**
- Material exposure to Scope 3 emissions in supply chain
- Investor and customer pressure for ISSB-aligned disclosures
- Climate transition risk affecting operations in {location}

**Reporting & Disclosure Requirements (2026)**
- EU CSRD / ESRS compliance (if applicable) or ISSB standards
- Mandatory Scope 1-3 reporting for listed or large entities
- Potential CSDDD due diligence obligations

**Improvement Opportunities**
- Carbon accounting platform deployment (Scope 1-3)
- Set science-based targets and publish transition plan
- Identify quick-win energy efficiency and waste reduction projects

**Investor & Stakeholder Appeal Actions**
- Publish first ISSB-aligned sustainability report
- Engage top 10 investors on ESG roadmap
- Obtain limited assurance on key metrics"""