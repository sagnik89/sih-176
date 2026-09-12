import pandas as pd

from backend.data.query import DataQuery


# ============================================================
# ORCA — Weather Service
# ============================================================


class WeatherService:
    """Analyzes marine weather conditions."""

    def __init__(self, dataframe: pd.DataFrame):
        self.df = dataframe.copy()
        self.query = DataQuery(self.df)

    def analyze(
        self,
        region: str | None = None,
    ) -> dict:
        """Generate a weather condition summary."""

        df = (
            self.query.by_region(region)
            if region
            else self.df
        )

        if df.empty:
            return {
                "agent": "WeatherAgent",
                "status": "no_data",
                "region": region,
                "findings": [
                    f"No weather observations found for {region}."
                    if region
                    else "No weather observations available."
                ],
                "metrics": {},
                "evidence": [],
                "confidence": 0.0,
                "data_source": "SYNTHETIC_DEMO_DATA",
            }

        averages = self.query.averages(
            region=region,
            columns=[
                "wind_speed",
                "rainfall",
                "pressure",
                "humidity",
            ],
        )

        findings = []

        # ----------------------------------------------------
        # Wind
        # ----------------------------------------------------

        if "wind_speed" in averages:
            wind = averages["wind_speed"]

            if wind >= 25:
                findings.append(
                    f"Very strong winds are indicated, "
                    f"averaging {wind:.2f} km/h."
                )
            elif wind >= 18:
                findings.append(
                    f"Strong wind conditions are present, "
                    f"averaging {wind:.2f} km/h."
                )
            elif wind >= 10:
                findings.append(
                    f"Moderate winds are present, "
                    f"averaging {wind:.2f} km/h."
                )
            else:
                findings.append(
                    f"Wind conditions are relatively calm, "
                    f"averaging {wind:.2f} km/h."
                )

        # ----------------------------------------------------
        # Rainfall
        # ----------------------------------------------------

        if "rainfall" in averages:
            rainfall = averages["rainfall"]

            if rainfall >= 50:
                findings.append(
                    f"Heavy rainfall conditions are indicated, "
                    f"averaging {rainfall:.2f} mm."
                )
            elif rainfall >= 25:
                findings.append(
                    f"Moderate-to-heavy rainfall is indicated, "
                    f"averaging {rainfall:.2f} mm."
                )
            elif rainfall >= 10:
                findings.append(
                    f"Moderate rainfall is indicated, "
                    f"averaging {rainfall:.2f} mm."
                )
            else:
                findings.append(
                    f"Rainfall is relatively low at "
                    f"{rainfall:.2f} mm."
                )

        # ----------------------------------------------------
        # Pressure
        # ----------------------------------------------------

        if "pressure" in averages:
            pressure = averages["pressure"]

            if pressure < 1000:
                findings.append(
                    f"Atmospheric pressure is relatively low "
                    f"at {pressure:.2f} hPa."
                )
            elif pressure > 1020:
                findings.append(
                    f"Atmospheric pressure is relatively high "
                    f"at {pressure:.2f} hPa."
                )
            else:
                findings.append(
                    f"Atmospheric pressure is approximately "
                    f"{pressure:.2f} hPa."
                )

        # ----------------------------------------------------
        # Humidity
        # ----------------------------------------------------

        if "humidity" in averages:
            humidity = averages["humidity"]

            if humidity >= 85:
                findings.append(
                    f"Very high atmospheric humidity is present "
                    f"at {humidity:.1f}%."
                )
            elif humidity >= 70:
                findings.append(
                    f"High atmospheric humidity is present "
                    f"at {humidity:.1f}%."
                )
            else:
                findings.append(
                    f"Average humidity is {humidity:.1f}%."
                )

        # ----------------------------------------------------
        # Weather severity
        # ----------------------------------------------------

        severity_score = 0.0

        wind = averages.get("wind_speed", 0)
        rainfall = averages.get("rainfall", 0)
        pressure = averages.get("pressure", 1012)

        if wind >= 18:
            severity_score += 0.35
        elif wind >= 10:
            severity_score += 0.15

        if rainfall >= 50:
            severity_score += 0.35
        elif rainfall >= 25:
            severity_score += 0.20
        elif rainfall >= 10:
            severity_score += 0.10

        if pressure < 1000:
            severity_score += 0.20

        severity_score = min(
            severity_score,
            1.0,
        )

        if severity_score >= 0.65:
            findings.append(
                "Overall weather conditions may contribute "
                "to elevated marine environmental stress."
            )
        elif severity_score >= 0.35:
            findings.append(
                "Weather conditions show moderate "
                "environmental influence."
            )
        else:
            findings.append(
                "Weather conditions show relatively "
                "limited environmental stress."
            )

        # ----------------------------------------------------
        # Evidence
        # ----------------------------------------------------

        evidence = []

        evidence_columns = [
            "region",
            "timestamp",
            "wind_speed",
            "rainfall",
            "pressure",
            "humidity",
            "data_source",
        ]

        available_columns = [
            column
            for column in evidence_columns
            if column in df.columns
        ]

        sample = df[
            available_columns
        ].tail(5)

        for _, row in sample.iterrows():
            record = {}

            for column in available_columns:
                value = row[column]

                if pd.isna(value):
                    continue

                if hasattr(value, "isoformat"):
                    value = value.isoformat()

                elif hasattr(value, "item"):
                    value = value.item()

                record[column] = value

            evidence.append(record)

        # ----------------------------------------------------
        # Confidence
        # ----------------------------------------------------

        confidence = min(
            1.0,
            0.65 + min(len(df), 1000) / 1000 * 0.30,
        )

        return {
            "agent": "WeatherAgent",
            "status": "success",
            "region": region,
            "findings": findings,
            "metrics": {
                **averages,
                "weather_severity_score": round(
                    severity_score,
                    3,
                ),
            },
            "evidence": evidence,
            "confidence": round(
                confidence,
                3,
            ),
            "data_source": "SYNTHETIC_DEMO_DATA",
        }