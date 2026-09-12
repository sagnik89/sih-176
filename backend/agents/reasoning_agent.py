import json
from typing import Any, Dict, List, Optional

from backend.ai.router import AIRouter


class ReasoningAgent:
    """Combines specialized agent evidence into an explainable ORCA answer."""

    name = "ReasoningAgent"

    SYSTEM_INSTRUCTION = """
You are ORCA, a marine ecosystem intelligence reasoning agent.

Your task is to reason over evidence produced by specialized marine,
weather, satellite, and ecology agents.

Rules:
1. Use ONLY the supplied evidence.
2. Never invent measurements, locations, dates, or data sources.
3. Clearly distinguish observations from interpretations.
4. Explain how multiple environmental factors relate to the conclusion.
5. If evidence is insufficient, explicitly say so.
6. The supplied prototype data is SYNTHETIC_DEMO_DATA.
7. Never claim that synthetic data is live ISRO, satellite, or ocean data.
8. Keep the answer concise but useful for an engineering demonstration.
9. Return valid JSON only.

Required JSON format:
{
  "answer": "natural language explanation",
  "risk_level": "LOW | MODERATE | HIGH | UNKNOWN",
  "risk_score": 0.0,
  "contributing_factors": [],
  "key_findings": [],
  "recommendations": []
}
""".strip()

    def __init__(self, router: Optional[AIRouter] = None):
        self.router = router or AIRouter()

    def _build_prompt(
        self,
        query: str,
        evidence: List[Dict[str, Any]],
    ) -> str:
        evidence_json = json.dumps(
            evidence,
            indent=2,
            default=str,
        )

        return f"""
User query:
{query}

Specialized agent evidence:
{evidence_json}

Analyze the evidence and produce the required JSON response.
""".strip()

    def _extract_json(self, text: str) -> Optional[Dict[str, Any]]:
        if not text:
            return None

        text = text.strip()

        if text.startswith("```"):
            lines = text.splitlines()

            if lines and lines[0].startswith("```"):
                lines = lines[1:]

            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]

            text = "\n".join(lines).strip()

        try:
            parsed = json.loads(text)

            if isinstance(parsed, dict):
                return parsed

        except json.JSONDecodeError:
            pass

        start = text.find("{")
        end = text.rfind("}")

        if start != -1 and end != -1 and end > start:
            try:
                parsed = json.loads(text[start:end + 1])

                if isinstance(parsed, dict):
                    return parsed

            except json.JSONDecodeError:
                pass

        return None

    def _fallback_result(
        self,
        evidence: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        findings = []

        for item in evidence:
            findings.extend(item.get("findings", []))

        risk_scores = []

        for item in evidence:
            metrics = item.get("metrics", {})

            score = metrics.get("ecological_risk_score")

            if score is not None:
                try:
                    risk_scores.append(float(score))
                except (TypeError, ValueError):
                    pass

        if risk_scores:
            risk_score = sum(risk_scores) / len(risk_scores)

            if risk_score >= 0.70:
                risk_level = "HIGH"
            elif risk_score >= 0.40:
                risk_level = "MODERATE"
            else:
                risk_level = "LOW"
        else:
            risk_score = 0.0
            risk_level = "UNKNOWN"

        return {
            "answer": (
                "The specialized ORCA agents identified the following "
                "environmental conditions from the available evidence."
            ),
            "risk_level": risk_level,
            "risk_score": round(risk_score, 3),
            "contributing_factors": [],
            "key_findings": findings[:10],
            "recommendations": [
                "Review the underlying observations before making "
                "operational decisions."
            ],
        }

    def run(
        self,
        query: str,
        evidence: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        prompt = self._build_prompt(query, evidence)

        result = self.router.generate(
            prompt=prompt,
            system_instruction=self.SYSTEM_INSTRUCTION,
        )

        if not result.get("success"):
            fallback = self._fallback_result(evidence)

            return {
                **fallback,
                "success": True,
                "model_used": None,
                "provider": "deterministic_fallback",
            }

        parsed = self._extract_json(result.get("text", ""))

        if parsed is None:
            fallback = self._fallback_result(evidence)

            return {
                **fallback,
                "success": True,
                "model_used": result.get("model"),
                "provider": result.get("provider"),
            }

        return {
            "answer": str(parsed.get("answer", "")),
            "risk_level": str(
                parsed.get("risk_level", "UNKNOWN")
            ).upper(),
            "risk_score": float(
                parsed.get("risk_score", 0.0)
            ),
            "contributing_factors": parsed.get(
                "contributing_factors",
                [],
            ),
            "key_findings": parsed.get(
                "key_findings",
                [],
            ),
            "recommendations": parsed.get(
                "recommendations",
                [],
            ),
            "success": True,
            "model_used": result.get("model"),
            "provider": result.get("provider"),
        }

    def capabilities(self):
        return [
            "multi-agent evidence fusion",
            "environmental risk reasoning",
            "cross-domain reasoning",
            "explainable decision generation",
            "evidence-grounded natural language response",
        ]