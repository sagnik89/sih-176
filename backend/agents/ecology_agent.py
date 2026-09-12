from backend.data.query import DataQuery
from backend.services.anomaly_service import AnomalyService
from backend.data.schemas import AgentEvidence


class EcologyAgent:
    """Specialized agent for marine ecological analysis."""

    name = "EcologyAgent"

    def __init__(self, dataframe):
        self.dataframe = dataframe
        self.query = DataQuery(dataframe)
        self.anomaly_service = AnomalyService()

    def run(self, region=None):
        dataframe = self.query.by_region(region) if region else self.dataframe

        if dataframe.empty:
            return AgentEvidence(
                agent=self.name,
                status="no_data",
                region=region,
                findings=["No ecological observations were found."],
                metrics={},
                evidence=[],
                confidence=0.0,
            )

        columns = [
            "chlorophyll",
            "turbidity",
            "phytoplankton_index",
            "fish_activity_index",
            "biodiversity_index",
            "ecological_risk_score",
        ]

        available = [column for column in columns if column in dataframe.columns]

        averages = {
            column: round(float(dataframe[column].mean()), 3)
            for column in available
        }

        risk_score = averages.get("ecological_risk_score", 0.0)
        biodiversity = averages.get("biodiversity_index", 0.0)
        fish_activity = averages.get("fish_activity_index", 0.0)
        phytoplankton = averages.get("phytoplankton_index", 0.0)

        findings = []

        if risk_score >= 0.70:
            findings.append("Ecological risk is high in the analyzed region.")
        elif risk_score >= 0.40:
            findings.append("Ecological risk is moderate in the analyzed region.")
        else:
            findings.append("Ecological conditions are relatively stable.")

        if biodiversity < 0.60:
            findings.append("Biodiversity index indicates potential ecological stress.")

        if fish_activity < 0.50:
            findings.append("Fish activity index is below the normal synthetic baseline.")

        if phytoplankton > 0.70:
            findings.append("Elevated phytoplankton activity is detected.")

        anomaly_result = self.anomaly_service.risk_contribution(dataframe)

        evidence = [
            {
                "type": "ecological_metrics",
                "description": "Aggregated ecological indicators",
                "metrics": averages,
            },
            {
                "type": "anomaly_analysis",
                "description": "Cross-variable anomaly assessment",
                "score": anomaly_result["score"],
                "severity": anomaly_result["severity"],
                "count": anomaly_result["count"],
            },
        ]

        confidence = min(
            0.95,
            0.65 + min(len(dataframe) / 1000.0, 0.30),
        )

        return AgentEvidence(
            agent=self.name,
            status="success",
            region=region,
            findings=findings,
            metrics={
                **averages,
                "anomaly_score": anomaly_result["score"],
                "anomaly_severity": anomaly_result["severity"],
                "anomaly_count": anomaly_result["count"],
            },
            evidence=evidence,
            confidence=round(confidence, 3),
            data_source="SYNTHETIC_DEMO_DATA",
        )

    def capabilities(self):
        return [
            "biodiversity assessment",
            "fish activity analysis",
            "phytoplankton analysis",
            "ecological risk assessment",
            "marine ecosystem anomaly detection",
        ]