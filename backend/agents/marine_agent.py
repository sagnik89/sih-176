from backend.data.schemas import AgentEvidence
from backend.services.marine_service import MarineService


class MarineAgent:
    """Specialized agent for marine/oceanographic analysis."""

    name = "MarineAgent"

    def __init__(self, dataframe):
        self.service = MarineService(dataframe)

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
            "sea surface temperature analysis",
            "SST anomaly detection",
            "salinity analysis",
            "wave condition analysis",
            "ocean current analysis",
        ]