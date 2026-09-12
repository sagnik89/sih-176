from backend.data.schemas import AgentEvidence
from backend.services.spatial_service import SpatialService


class SatelliteAgent:
    """Specialized agent for satellite-derived and spatial observations."""

    name = "SatelliteAgent"

    def __init__(self, dataframe):
        self.service = SpatialService(dataframe)

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
            "sea surface temperature mapping",
            "SST anomaly analysis",
            "chlorophyll analysis",
            "turbidity analysis",
            "eddy detection",
            "spatial marine condition analysis",
        ]