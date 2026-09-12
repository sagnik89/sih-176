import pandas as pd


# ============================================================
# ORCA — Data Normalizer
# ============================================================


class DataNormalizer:
    """Normalizes and cleans ORCA observation datasets."""

    @staticmethod
    def normalize(
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:
        """Clean and normalize a dataframe."""

        df = dataframe.copy()

        # ----------------------------------------------------
        # Normalize column names
        # ----------------------------------------------------

        df.columns = [
            column.strip().lower().replace(" ", "_")
            for column in df.columns
        ]

        # ----------------------------------------------------
        # Timestamp
        # ----------------------------------------------------

        if "timestamp" in df.columns:
            df["timestamp"] = pd.to_datetime(
                df["timestamp"],
                errors="coerce",
            )

        # ----------------------------------------------------
        # Numeric columns
        # ----------------------------------------------------

        numeric_columns = [
            "latitude",
            "longitude",
            "sst",
            "sst_anomaly",
            "salinity",
            "wave_height",
            "current_speed",
            "current_direction",
            "wind_speed",
            "rainfall",
            "pressure",
            "humidity",
            "chlorophyll",
            "turbidity",
            "eddy_present",
            "phytoplankton_index",
            "fish_activity_index",
            "biodiversity_index",
            "ecological_risk_score",
        ]

        for column in numeric_columns:
            if column in df.columns:
                df[column] = pd.to_numeric(
                    df[column],
                    errors="coerce",
                )

        # ----------------------------------------------------
        # Remove invalid coordinates
        # ----------------------------------------------------

        if "latitude" in df.columns:
            df = df[
                df["latitude"].between(-90, 90)
            ]

        if "longitude" in df.columns:
            df = df[
                df["longitude"].between(-180, 180)
            ]

        # ----------------------------------------------------
        # Remove duplicate records
        # ----------------------------------------------------

        if "id" in df.columns:
            df = df.drop_duplicates(
                subset=["id"]
            )

        # ----------------------------------------------------
        # Sort chronologically
        # ----------------------------------------------------

        if "timestamp" in df.columns:
            df = df.sort_values(
                "timestamp"
            )

        # ----------------------------------------------------
        # Reset index
        # ----------------------------------------------------

        df = df.reset_index(drop=True)

        return df

    @staticmethod
    def fill_missing(
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:
        """Fill missing numeric values using column medians."""

        df = dataframe.copy()

        numeric_columns = df.select_dtypes(
            include="number"
        ).columns

        for column in numeric_columns:
            if df[column].isna().any():
                df[column] = df[column].fillna(
                    df[column].median()
                )

        return df

    @staticmethod
    def prepare(
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:
        """Perform the complete normalization pipeline."""

        df = DataNormalizer.normalize(
            dataframe
        )

        df = DataNormalizer.fill_missing(
            df
        )

        return df