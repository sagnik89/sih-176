import pandas as pd

from backend.data.query import DataQuery


# ============================================================
# ORCA — Marine Service
# ============================================================


class MarineService:
    """Analyzes marine and oceanographic conditions."""

    def __init__(self, dataframe: pd.DataFrame):
        self.df = dataframe.copy()
        self.query = DataQuery(self.df)

    def analyze(
        self,
        region: str | None = None,
    ) -> dict:
        """Generate a marine condition summary."""

        df = (
            self.query.by_region(region)
            if region
            else self.df
        )

        if df.empty:
            return {
                "agent": "MarineAgent",
                "status": "no_data",
                "region": region,
                "findings": [
                    f"No marine observations found for {region}."
                    if region
                    else "No marine observations available."
                ],
                "metrics": {},
                "evidence": [],
                "confidence": 0.0,
                "data_source": "SYNTHETIC_DEMO_DATA",
            }

        averages = self.query.averages(
            region=region,
            columns=[
                "sst",
                "sst_anomaly",
                "salinity",
                "wave_height",
                "current_speed",
                "current_direction",
            ],
        )

        findings = []

        # ----------------------------------------------------
        # SST
        # ----------------------------------------------------

        if "sst" in averages:
            sst = averages["sst"]

            if sst >= 30:
                findings.append(
                    f"Sea surface temperature is elevated at "
                    f"{sst:.2f}°C."
                )
            elif sst <= 25:
                findings.append(
                    f"Sea surface temperature is relatively low "
                    f"at {sst:.2f}°C."
                )
            else:
                findings.append(
                    f"Sea surface temperature is approximately "
                    f"{sst:.2f}°C."
                )

        # ----------------------------------------------------
        # SST anomaly
        # ----------------------------------------------------

        if "sst_anomaly" in averages:
            anomaly = averages["sst_anomaly"]

            if abs(anomaly) >= 1.5:
                direction = (
                    "above"
                    if anomaly > 0
                    else "below"
                )

                findings.append(
                    f"SST anomaly is {abs(anomaly):.2f}°C "
                    f"{direction} the local baseline."
                )

        # ----------------------------------------------------
        # Waves
        # ----------------------------------------------------

        if "wave_height" in averages:
            wave_height = averages["wave_height"]

            if wave_height >= 3:
                findings.append(
                    f"Wave conditions are rough, with an average "
                    f"height of {wave_height:.2f} m."
                )
            elif wave_height >= 1.8:
                findings.append(
                    f"Moderate wave activity is present at "
                    f"{wave_height:.2f} m."
                )
            else:
                findings.append(
                    f"Wave activity is relatively calm at "
                    f"{wave_height:.2f} m."
                )

        # ----------------------------------------------------
        # Salinity
        # ----------------------------------------------------

        if "salinity" in averages:
            salinity = averages["salinity"]

            findings.append(
                f"Average surface salinity is "
                f"{salinity:.2f} PSU."
            )

        # ----------------------------------------------------
        # Current
        # ----------------------------------------------------

        if "current_speed" in averages:
            current_speed = averages["current_speed"]

            if current_speed >= 1.2:
                findings.append(
                    f"Strong surface currents are indicated, "
                    f"averaging {current_speed:.2f} m/s."
                )
            else:
                findings.append(
                    f"Average surface current speed is "
                    f"{current_speed:.2f} m/s."
                )

        # ----------------------------------------------------
        # Evidence
        # ----------------------------------------------------

        evidence = []

        evidence_columns = [
            "region",
            "timestamp",
            "sst",
            "sst_anomaly",
            "salinity",
            "wave_height",
            "current_speed",
            "current_direction",
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
            "agent": "MarineAgent",
            "status": "success",
            "region": region,
            "findings": findings,
            "metrics": averages,
            "evidence": evidence,
            "confidence": round(confidence, 3),
            "data_source": "SYNTHETIC_DEMO_DATA",
        }