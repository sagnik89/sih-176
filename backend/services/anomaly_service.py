from typing import Any, Dict

import pandas as pd


class AnomalyService:
    """Detects environmental anomalies and estimates anomaly-driven risk."""

    def detect(self, dataframe: pd.DataFrame) -> Dict[str, Any]:
        if dataframe.empty:
            return {
                "anomalies": [],
                "score": 0.0,
                "severity": "LOW",
                "count": 0,
            }

        anomalies = []

        rules = {
            "sst_anomaly": {
                "threshold": 1.5,
                "label": "Elevated sea surface temperature anomaly",
            },
            "turbidity": {
                "threshold": 8.0,
                "label": "Elevated water turbidity",
            },
            "wave_height": {
                "threshold": 3.5,
                "label": "High wave activity",
            },
            "wind_speed": {
                "threshold": 25.0,
                "label": "High wind activity",
            },
            "rainfall": {
                "threshold": 20.0,
                "label": "Elevated rainfall",
            },
            "biodiversity_index": {
                "threshold": 0.40,
                "label": "Low biodiversity index",
                "inverse": True,
            },
            "fish_activity_index": {
                "threshold": 0.35,
                "label": "Low fish activity",
                "inverse": True,
            },
        }

        for column, rule in rules.items():

            if column not in dataframe.columns:
                continue

            values = pd.to_numeric(
                dataframe[column],
                errors="coerce",
            ).dropna()

            if values.empty:
                continue

            threshold = rule["threshold"]

            if rule.get("inverse", False):
                mask = values < threshold
            else:
                mask = values > threshold

            count = int(mask.sum())

            if count > 0:
                anomalies.append(
                    {
                        "variable": column,
                        "label": rule["label"],
                        "count": count,
                        "percentage": round(
                            (count / len(values)) * 100,
                            2,
                        ),
                    }
                )

        total_records = max(len(dataframe), 1)

        anomaly_records = sum(
            anomaly["count"]
            for anomaly in anomalies
        )

        anomaly_score = min(
            anomaly_records / total_records,
            1.0,
        )

        if anomaly_score >= 0.70:
            severity = "HIGH"
        elif anomaly_score >= 0.40:
            severity = "MODERATE"
        elif anomaly_score > 0:
            severity = "LOW"
        else:
            severity = "NORMAL"

        return {
            "anomalies": anomalies,
            "score": round(float(anomaly_score), 3),
            "severity": severity,
            "count": anomaly_records,
        }

    def risk_contribution(
        self,
        dataframe: pd.DataFrame,
    ) -> Dict[str, Any]:
        """Return anomaly contribution to ecological risk."""

        result = self.detect(dataframe)

        risk_factors = [
            anomaly["label"]
            for anomaly in result["anomalies"]
        ]

        return {
            "score": result["score"],
            "severity": result["severity"],
            "count": result["count"],
            "risk_factors": risk_factors,
        }