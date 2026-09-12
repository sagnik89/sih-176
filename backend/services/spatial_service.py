import pandas as pd

from backend.data.query import DataQuery


# ============================================================
# ORCA — Spatial / Satellite Service
# ============================================================


class SpatialService:
    """Analyzes spatial and satellite-style observations."""

    def __init__(self, dataframe: pd.DataFrame):
        self.df = dataframe.copy()
        self.query = DataQuery(self.df)

    def analyze(
        self,
        region: str | None = None,
    ) -> dict:
        """Generate a spatial and satellite condition summary."""

        df = (
            self.query.by_region(region)
            if region
            else self.df
        )

        if df.empty:
            return {
                "agent": "SatelliteAgent",
                "status": "no_data",
                "region": region,
                "findings": [
                    f"No satellite observations found for {region}."
                    if region
                    else "No satellite observations available."
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
                "chlorophyll",
                "turbidity",
            ],
        )

        findings = []

        # ----------------------------------------------------
        # SST anomaly
        # ----------------------------------------------------

        anomaly = averages.get(
            "sst_anomaly",
            0.0,
        )

        if abs(anomaly) >= 1.5:
            direction = (
                "positive"
                if anomaly > 0
                else "negative"
            )

            findings.append(
                f"A significant {direction} SST anomaly "
                f"of {anomaly:+.2f}°C is detected."
            )
        elif abs(anomaly) >= 0.8:
            findings.append(
                f"A moderate SST anomaly of "
                f"{anomaly:+.2f}°C is present."
            )
        else:
            findings.append(
                f"SST conditions are close to the local "
                f"baseline with an anomaly of "
                f"{anomaly:+.2f}°C."
            )

        # ----------------------------------------------------
        # Chlorophyll
        # ----------------------------------------------------

        chlorophyll = averages.get(
            "chlorophyll",
            0.0,
        )

        if chlorophyll >= 5:
            findings.append(
                f"High chlorophyll concentration is indicated "
                f"at approximately {chlorophyll:.2f} mg/m³."
            )
        elif chlorophyll >= 2:
            findings.append(
                f"Moderate chlorophyll concentration is indicated "
                f"at approximately {chlorophyll:.2f} mg/m³."
            )
        else:
            findings.append(
                f"Chlorophyll concentration is relatively low "
                f"at approximately {chlorophyll:.2f} mg/m³."
            )

        # ----------------------------------------------------
        # Turbidity
        # ----------------------------------------------------

        turbidity = averages.get(
            "turbidity",
            0.0,
        )

        if turbidity >= 35:
            findings.append(
                f"Very high water turbidity is detected "
                f"at approximately {turbidity:.2f} NTU."
            )
        elif turbidity >= 20:
            findings.append(
                f"Elevated water turbidity is detected "
                f"at approximately {turbidity:.2f} NTU."
            )
        elif turbidity >= 10:
            findings.append(
                f"Moderate water turbidity is present "
                f"at approximately {turbidity:.2f} NTU."
            )
        else:
            findings.append(
                f"Water turbidity is relatively low "
                f"at approximately {turbidity:.2f} NTU."
            )

        # ----------------------------------------------------
        # Eddy analysis
        # ----------------------------------------------------

        eddy_present_count = 0

        if "eddy_present" in df.columns:
            eddy_present_count = int(
                pd.to_numeric(
                    df["eddy_present"],
                    errors="coerce",
                )
                .fillna(0)
                .sum()
            )

        total_records = len(df)

        eddy_percentage = (
            eddy_present_count / total_records * 100
            if total_records
            else 0
        )

        if eddy_percentage >= 40:
            findings.append(
                f"Strong mesoscale activity is indicated, "
                f"with eddy signatures in approximately "
                f"{eddy_percentage:.1f}% of observations."
            )
        elif eddy_percentage >= 20:
            findings.append(
                f"Moderate mesoscale activity is indicated, "
                f"with eddy signatures in approximately "
                f"{eddy_percentage:.1f}% of observations."
            )
        else:
            findings.append(
                f"Eddy signatures occur in approximately "
                f"{eddy_percentage:.1f}% of observations."
            )

        # ----------------------------------------------------
        # Geographic coverage
        # ----------------------------------------------------

        geographic = {}

        if {
            "latitude",
            "longitude",
        }.issubset(df.columns):

            geographic = {
                "min_latitude": round(
                    float(df["latitude"].min()),
                    5,
                ),
                "max_latitude": round(
                    float(df["latitude"].max()),
                    5,
                ),
                "min_longitude": round(
                    float(df["longitude"].min()),
                    5,
                ),
                "max_longitude": round(
                    float(df["longitude"].max()),
                    5,
                ),
            }

        # ----------------------------------------------------
        # Evidence
        # ----------------------------------------------------

        evidence = []

        evidence_columns = [
            "region",
            "latitude",
            "longitude",
            "timestamp",
            "sst",
            "sst_anomaly",
            "chlorophyll",
            "turbidity",
            "eddy_present",
            "eddy_type",
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
            0.65 + min(total_records, 1000) / 1000 * 0.30,
        )

        return {
            "agent": "SatelliteAgent",
            "status": "success",
            "region": region,
            "findings": findings,
            "metrics": {
                **averages,
                "eddy_observation_count": eddy_present_count,
                "eddy_percentage": round(
                    eddy_percentage,
                    2,
                ),
                **geographic,
            },
            "evidence": evidence,
            "confidence": round(
                confidence,
                3,
            ),
            "data_source": "SYNTHETIC_DEMO_DATA",
        }