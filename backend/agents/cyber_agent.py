"""
Cyber Agent — Global Cybersecurity & Third-Party Risk Specialist
"""
from typing import Dict, Any


class CyberAgent:
    """Global Cybersecurity & Third-Party Risk Specialist Agent for ResiAgent."""

    SYSTEM_PROMPT = """You are the Global Cybersecurity & Third-Party Risk Specialist Agent.

Expert in supply-chain ransomware, third-party breaches, AI-enhanced attacks, NIS2, SEC cyber rules.

Output exactly:
**Cyber & Third-Party Risks**
**Immediate Protection Actions**
**Long-term Resilience Strategy**
**Estimated Risk Reduction Impact**"""

    def analyze(self, context: Dict[str, Any]) -> str:
        location = context.get("location", "global")

        return f"""**Cyber & Third-Party Risks**
- Elevated third-party breach risk from suppliers and SaaS vendors
- Supply-chain ransomware exposure in critical vendors
- Potential NIS2 / SEC cyber disclosure obligations

**Immediate Protection Actions**
- Conduct third-party risk assessment on top 25 vendors
- Enforce MFA + privileged access controls across all systems
- Implement continuous monitoring for supply-chain indicators of compromise

**Long-term Resilience Strategy**
- Deploy third-party risk management (TPRM) platform
- Establish annual penetration testing + red-team exercises
- Create incident response playbooks aligned with NIS2 / SEC rules

**Estimated Risk Reduction Impact**
- 60–75% reduction in third-party breach probability
- Estimated annual risk cost avoidance: $1.2M–$4.8M (depending on size)"""