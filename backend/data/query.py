from typing import Any, Dict, List, Optional

import pandas as pd


# ============================================================
# ORCA — Data Query Engine
# ============================================================


class DataQuery:
    """Provides common filtering and aggregation operations."""

    def __init__(self, dataframe: pd.DataFrame):
        self.df = dataframe.copy()

    # --------------------------------------------------------
    # Region
    # --------------------------------------------------------

    def by_region(
        self,
        region: str,
    ) -> pd.DataFrame:
        """Return observations for a specific region."""

        if "region" not in self.df.columns:
            return pd.DataFrame()

        mask = (
            self.df["region"]
            .astype(str)
            .str.lower()
            .str.contains(
                region.lower(),
                regex=False,
            )
        )

        return self.df[mask].copy()

    # --------------------------------------------------------
    # Latest observations
    # --------------------------------------------------------

    def latest(
        self,
        region: Optional[str] = None,
        limit: int = 10,
    ) -> pd.DataFrame:
        """Return the most recent observations."""

        df = self.df

        if region:
            df = self.by_region(region)

        if df.empty:
            return df

        if "timestamp" in df.columns:
            df = df.sort_values(
                "timestamp",
                ascending=False,
            )

        return df.head(limit).copy()

    # --------------------------------------------------------
    # Geographic bounding box
    # --------------------------------------------------------

    def within_bounds(
        self,
        min_lat: float,
        max_lat: float,
        min_lon: float,
        max_lon: float,
    ) -> pd.DataFrame:
        """Return observations inside a geographic bounding box."""

        if not {
            "latitude",
            "longitude",
        }.issubset(self.df.columns):
            return pd.DataFrame()

        mask = (
            self.df["latitude"].between(
                min_lat,
                max_lat,
            )
            & self.df["longitude"].between(
                min_lon,
                max_lon,
            )
        )

        return self.df[mask].copy()

    # --------------------------------------------------------
    # Numeric summary
    # --------------------------------------------------------

    def summarize(
        self,
        dataframe: Optional[pd.DataFrame] = None,
        columns: Optional[List[str]] = None,
    ) -> Dict[str, Dict[str, float]]:
        """Calculate basic statistics for selected columns."""

        df = (
            dataframe.copy()
            if dataframe is not None
            else self.df.copy()
        )

        if columns:
            columns = [
                column
                for column in columns
                if column in df.columns
            ]
            df = df[columns]

        numeric_df = df.select_dtypes(
            include="number"
        )

        if numeric_df.empty:
            return {}

        summary = {}

        for column in numeric_df.columns:
            series = numeric_df[column].dropna()

            if series.empty:
                continue

            summary[column] = {
                "mean": float(series.mean()),
                "min": float(series.min()),
                "max": float(series.max()),
                "median": float(series.median()),
            }

        return summary

    # --------------------------------------------------------
    # Risk observations
    # --------------------------------------------------------

    def high_risk(
        self,
        region: Optional[str] = None,
    ) -> pd.DataFrame:
        """Return HIGH and CRITICAL ecological observations."""

        df = self.df

        if region:
            df = self.by_region(region)

        if "ecological_risk" not in df.columns:
            return pd.DataFrame()

        return df[
            df["ecological_risk"].isin(
                ["HIGH", "CRITICAL"]
            )
        ].copy()

    # --------------------------------------------------------
    # Column averages
    # --------------------------------------------------------

    def averages(
        self,
        region: Optional[str] = None,
        columns: Optional[List[str]] = None,
    ) -> Dict[str, float]:
        """Return average values for selected columns."""

        df = self.df

        if region:
            df = self.by_region(region)

        if df.empty:
            return {}

        if columns is None:
            columns = [
                "sst",
                "sst_anomaly",
                "salinity",
                "wave_height",
                "wind_speed",
                "rainfall",
                "pressure",
                "humidity",
                "chlorophyll",
                "turbidity",
                "current_speed",
                "phytoplankton_index",
                "fish_activity_index",
                "biodiversity_index",
                "ecological_risk_score",
            ]

        result = {}

        for column in columns:
            if column not in df.columns:
                continue

            value = pd.to_numeric(
                df[column],
                errors="coerce",
            ).mean()

            if pd.notna(value):
                result[column] = round(
                    float(value),
                    4,
                )

        return result

    # --------------------------------------------------------
    # Region overview
    # --------------------------------------------------------

    def region_overview(
        self,
        region: str,
    ) -> Dict[str, Any]:
        """Build a compact overview for an individual region."""

        df = self.by_region(region)

        if df.empty:
            return {
                "region": region,
                "found": False,
                "records": 0,
            }

        overview: Dict[str, Any] = {
            "region": region,
            "found": True,
            "records": len(df),
        }

        if {
            "latitude",
            "longitude",
        }.issubset(df.columns):
            overview["center"] = {
                "latitude": round(
                    float(df["latitude"].mean()),
                    5,
                ),
                "longitude": round(
                    float(df["longitude"].mean()),
                    5,
                ),
            }

        overview["averages"] = self.averages(
            region=region
        )

        if "ecological_risk" in df.columns:
            risk_counts = (
                df["ecological_risk"]
                .value_counts()
                .to_dict()
            )

            overview["risk_distribution"] = {
                str(key): int(value)
                for key, value in risk_counts.items()
            }

        return overview