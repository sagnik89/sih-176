from backend.data.schemas import AgentEvidence
from backend.services.weather_service import WeatherService


class WeatherAgent:
    """Specialized agent for weather and atmospheric analysis."""

    name = "WeatherAgent"

    def __init__(self, dataframe):
        self.service = WeatherService(dataframe)

    def run(self, region=None):
        result = self.service.analyze(region)

        return AgentEvidence(
            agent=self.name,
            status=result.get("status", "success"),
            region=result.get("region"),
            findings=result.get("findings", []),
            metrics=result.get("metrics", {}),
            evidence=result.get("evidence", []),
            confidence=result.get("confidence", 0.0),
            data_source=result.get(
                "data_source",
                "SYNTHETIC_DEMO_DATA",
            ),
        )

    def capabilities(self):
        return [
            "wind speed analysis",
            "rainfall analysis",
            "atmospheric pressure analysis",
            "humidity analysis",
            "weather severity assessment",
        ]