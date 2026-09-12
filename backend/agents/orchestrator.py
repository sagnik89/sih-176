from typing import Any, Dict, List, Optional

from backend.agents.ecology_agent import EcologyAgent
from backend.agents.marine_agent import MarineAgent
from backend.agents.reasoning_agent import ReasoningAgent
from backend.agents.satellite_agent import SatelliteAgent
from backend.agents.weather_agent import WeatherAgent
from backend.data.schemas import ORCAResponse


class ORCAOrchestrator:
    """Coordinates specialized agents and the final reasoning layer."""

    def __init__(self, dataframe):
        self.dataframe = dataframe

        self.marine_agent = MarineAgent(dataframe)
        self.weather_agent = WeatherAgent(dataframe)
        self.satellite_agent = SatelliteAgent(dataframe)
        self.ecology_agent = EcologyAgent(dataframe)

        self.reasoning_agent = ReasoningAgent()

    def _detect_region(self, query: str) -> Optional[str]:
        query_lower = query.lower()

        regions = self.dataframe["region"].dropna().unique()

        for region in regions:
            if str(region).lower() in query_lower:
                return str(region)

        return None

    def _run_specialized_agents(
        self,
        region: Optional[str],
    ) -> List[Dict[str, Any]]:
        agents = [
            self.marine_agent,
            self.weather_agent,
            self.satellite_agent,
            self.ecology_agent,
        ]

        evidence = []

        for agent in agents:
            result = agent.run(region)

            if hasattr(result, "model_dump"):
                evidence.append(result.model_dump())
            else:
                evidence.append(result)

        return evidence

    def run(self, query: str) -> ORCAResponse:
        if not query or not query.strip():
            return ORCAResponse(
                query=query,
                answer="Please provide a marine or ecological question.",
                agents_used=[],
            )

        region = self._detect_region(query)

        evidence = self._run_specialized_agents(region)

        reasoning = self.reasoning_agent.run(
            query=query,
            evidence=evidence,
        )

        risk_score = reasoning.get("risk_score", 0.0)
        risk_level = reasoning.get("risk_level", "UNKNOWN")

        return ORCAResponse(
            query=query,
            region=region,
            answer=reasoning.get("answer", ""),
            risk={
                "level": risk_level,
                "score": risk_score,
                "explanation": reasoning.get("answer", ""),
                "contributing_factors": reasoning.get(
                    "contributing_factors",
                    [],
                ),
            },
            findings=reasoning.get(
                "key_findings",
                [],
            ),
            evidence=evidence,
            agents_used=[
                "MarineAgent",
                "WeatherAgent",
                "SatelliteAgent",
                "EcologyAgent",
                "ReasoningAgent",
            ],
            model_used=reasoning.get("model_used"),
            data_mode="SYNTHETIC_DEMO_DATA",
        )

    def capabilities(self):
        return {
            "MarineAgent": self.marine_agent.capabilities(),
            "WeatherAgent": self.weather_agent.capabilities(),
            "SatelliteAgent": self.satellite_agent.capabilities(),
            "EcologyAgent": self.ecology_agent.capabilities(),
            "ReasoningAgent": self.reasoning_agent.capabilities(),
        }