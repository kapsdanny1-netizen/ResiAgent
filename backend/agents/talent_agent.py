"""
Talent Agent — Global Talent & Labor Resilience Specialist
"""
from typing import Dict, Any


class TalentAgent:
    """Global Talent & Labor Resilience Specialist Agent for ResiAgent."""

    SYSTEM_PROMPT = """You are the Global Talent & Labor Resilience Specialist Agent.

Expert in skilled labor shortages, demographic shifts, AI upskilling, retention.

Output exactly:
**Talent & Labor Risks**
**Immediate Workforce Actions**
**Upskilling & Retention Strategy**
**Projected Productivity & Cost Impact**"""

    def analyze(self, context: Dict[str, Any]) -> str:
        location = context.get("location", "global")

        return f"""**Talent & Labor Risks**
- Critical skill shortages in AI, cybersecurity, and sustainability roles
- Demographic pressure and retention challenges in {location}
- Risk of talent attrition due to lack of upskilling programs

**Immediate Workforce Actions**
- Run skills gap analysis across all functions
- Launch targeted retention packages for high-risk roles
- Partner with local universities / bootcamps for pipeline development

**Upskilling & Retention Strategy**
- Deploy AI-powered internal learning academy (role-based pathways)
- Introduce quarterly skill-based career reviews
- Create internal mobility and gig-work marketplace

**Projected Productivity & Cost Impact**
- 18–25% productivity lift from targeted upskilling
- Estimated annual talent acquisition cost savings: $180k–$650k"""