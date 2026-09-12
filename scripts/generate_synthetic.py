from pathlib import Path

import numpy as np
import pandas as pd


# ============================================================
# ORCA — Synthetic India Coastal Dataset Generator
# ============================================================

SEED = 42
N_OBSERVATIONS = 5000

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "data" / "synthetic"

rng = np.random.default_rng(SEED)


# ============================================================
# Indian Coastal Regions
# ============================================================

REGIONS = {
    "Sundarbans": {
        "latitude": 21.95,
        "longitude": 89.18,
        "sst": 28.2,
        "salinity": 22.0,
        "rainfall": 18.0,
        "risk_bias": 0.10,
    },
    "Odisha Coast": {
        "latitude": 19.82,
        "longitude": 85.83,
        "sst": 29.0,
        "salinity": 30.5,
        "rainfall": 15.0,
        "risk_bias": 0.08,
    },
    "Visakhapatnam": {
        "latitude": 17.69,
        "longitude": 83.22,
        "sst": 28.5,
        "salinity": 33.5,
        "rainfall": 8.0,
        "risk_bias": 0.03,
    },
    "Chennai Coast": {
        "latitude": 13.08,
        "longitude": 80.27,
        "sst": 29.2,
        "salinity": 34.0,
        "rainfall": 7.0,
        "risk_bias": 0.04,
    },
    "Kerala Coast": {
        "latitude": 9.93,
        "longitude": 76.27,
        "sst": 28.3,
        "salinity": 34.2,
        "rainfall": 20.0,
        "risk_bias": 0.06,
    },
    "Mumbai Coast": {
        "latitude": 18.95,
        "longitude": 72.82,
        "sst": 28.0,
        "salinity": 34.5,
        "rainfall": 17.0,
        "risk_bias": 0.05,
    },
    "Gujarat Coast": {
        "latitude": 22.30,
        "longitude": 69.60,
        "sst": 27.5,
        "salinity": 36.0,
        "rainfall": 5.0,
        "risk_bias": 0.07,
    },
    "Goa Coast": {
        "latitude": 15.49,
        "longitude": 73.83,
        "sst": 28.2,
        "salinity": 34.0,
        "rainfall": 12.0,
        "risk_bias": 0.03,
    },
    "Andaman & Nicobar": {
        "latitude": 11.74,
        "longitude": 92.66,
        "sst": 29.0,
        "salinity": 33.0,
        "rainfall": 14.0,
        "risk_bias": 0.02,
    },
    "Lakshadweep": {
        "latitude": 10.57,
        "longitude": 72.64,
        "sst": 28.5,
        "salinity": 35.0,
        "rainfall": 8.0,
        "risk_bias": 0.02,
    },
}


# ============================================================
# Helper Functions
# ============================================================

def clamp(value, minimum, maximum):
    return np.clip(value, minimum, maximum)


def classify_risk(score):
    if score < 0.30:
        return "LOW"
    elif score < 0.60:
        return "MEDIUM"
    elif score < 0.80:
        return "HIGH"
    return "CRITICAL"


def generate_dataset():
    region_names = list(REGIONS.keys())

    selected_regions = rng.choice(
        region_names,
        size=N_OBSERVATIONS,
        replace=True,
    )

    timestamps = pd.date_range(
        start="2025-01-01",
        end="2026-08-31",
        periods=N_OBSERVATIONS,
    )

    rows = []

    for i, region_name in enumerate(selected_regions):

        config = REGIONS[region_name]

        # ----------------------------------------------------
        # Location
        # ----------------------------------------------------

        latitude = config["latitude"] + rng.normal(0, 0.20)
        longitude = config["longitude"] + rng.normal(0, 0.20)

        timestamp = timestamps[i]

        # Seasonal component
        month = timestamp.month

        seasonal_temperature = 1.5 * np.sin(
            2 * np.pi * (month - 3) / 12
        )

        # ----------------------------------------------------
        # Weather
        # ----------------------------------------------------

        rainfall = max(
            0,
            config["rainfall"]
            + rng.normal(0, 8)
            + (
                30
                if month in [6, 7, 8, 9]
                else 0
            )
        )

        wind_speed = max(
            1,
            rng.normal(12, 5)
            + (
                5
                if month in [6, 7, 8, 9]
                else 0
            )
        )

        pressure = clamp(
            rng.normal(1012, 8)
            - rainfall * 0.08,
            980,
            1035,
        )

        humidity = clamp(
            rng.normal(72, 12)
            + rainfall * 0.25,
            35,
            100,
        )

        # ----------------------------------------------------
        # Marine Conditions
        # ----------------------------------------------------

        sst = (
            config["sst"]
            + seasonal_temperature
            + rng.normal(0, 0.8)
        )

        sst_anomaly = (
            sst
            - (
                config["sst"]
                + seasonal_temperature
            )
        )

        salinity = clamp(
            config["salinity"]
            - rainfall * 0.05
            + rng.normal(0, 1.2),
            15,
            40,
        )

        wave_height = clamp(
            0.7
            + wind_speed * 0.09
            + rng.normal(0, 0.35),
            0.2,
            6.0,
        )

        current_speed = clamp(
            rng.normal(0.65, 0.25)
            + wave_height * 0.05,
            0.05,
            2.5,
        )

        current_direction = rng.uniform(0, 360)

        # ----------------------------------------------------
        # Satellite-derived style observations
        # ----------------------------------------------------

        turbidity = clamp(
            4
            + rainfall * 0.35
            + wind_speed * 0.12
            + rng.normal(0, 2.5),
            0.5,
            80,
        )

        chlorophyll = clamp(
            0.7
            + rainfall * 0.025
            + turbidity * 0.035
            + rng.normal(0, 0.35),
            0.05,
            12,
        )

        # SST anomaly can influence oceanographic features
        eddy_probability = clamp(
            0.25
            + abs(sst_anomaly) * 0.12
            + current_speed * 0.15
            + rng.normal(0, 0.08),
            0,
            1,
        )

        eddy_present = int(
            rng.random() < eddy_probability
        )

        if eddy_present:
            eddy_type = rng.choice(
                ["cyclonic", "anticyclonic"]
            )
        else:
            eddy_type = "none"

        # ----------------------------------------------------
        # Ecological indicators
        # ----------------------------------------------------

        phytoplankton_index = clamp(
            0.25
            + chlorophyll * 0.10
            + rainfall * 0.005
            + rng.normal(0, 0.08),
            0,
            1,
        )

        fish_activity_index = clamp(
            0.65
            + phytoplankton_index * 0.25
            - abs(sst_anomaly) * 0.10
            - turbidity * 0.004
            + rng.normal(0, 0.08),
            0,
            1,
        )

        biodiversity_index = clamp(
            0.75
            - abs(sst_anomaly) * 0.12
            - turbidity * 0.006
            + phytoplankton_index * 0.10
            + rng.normal(0, 0.07),
            0,
            1,
        )

        # ----------------------------------------------------
        # Ecological Risk
        # ----------------------------------------------------

        risk_score = (
            abs(sst_anomaly) * 0.16
            + turbidity / 80 * 0.20
            + rainfall / 100 * 0.12
            + wave_height / 6 * 0.10
            + (1 - fish_activity_index) * 0.15
            + (1 - biodiversity_index) * 0.17
            + eddy_present * 0.04
            + config["risk_bias"]
        )

        # Small natural noise
        risk_score += rng.normal(0, 0.035)

        risk_score = float(
            clamp(risk_score, 0, 1)
        )

        ecological_risk = classify_risk(risk_score)

        # ----------------------------------------------------
        # Final record
        # ----------------------------------------------------

        rows.append(
            {
                "id": i + 1,
                "region": region_name,
                "latitude": round(latitude, 5),
                "longitude": round(longitude, 5),
                "timestamp": timestamp.strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),

                # Marine
                "sst": round(float(sst), 3),
                "sst_anomaly": round(
                    float(sst_anomaly), 3
                ),
                "salinity": round(
                    float(salinity), 3
                ),
                "wave_height": round(
                    float(wave_height), 3
                ),
                "current_speed": round(
                    float(current_speed), 3
                ),
                "current_direction": round(
                    float(current_direction), 2
                ),

                # Weather
                "wind_speed": round(
                    float(wind_speed), 3
                ),
                "rainfall": round(
                    float(rainfall), 3
                ),
                "pressure": round(
                    float(pressure), 3
                ),
                "humidity": round(
                    float(humidity), 3
                ),

                # Satellite
                "chlorophyll": round(
                    float(chlorophyll), 3
                ),
                "turbidity": round(
                    float(turbidity), 3
                ),
                "eddy_present": eddy_present,
                "eddy_type": eddy_type,

                # Ecology
                "phytoplankton_index": round(
                    float(phytoplankton_index), 3
                ),
                "fish_activity_index": round(
                    float(fish_activity_index), 3
                ),
                "biodiversity_index": round(
                    float(biodiversity_index), 3
                ),
                "ecological_risk_score": round(
                    risk_score, 3
                ),
                "ecological_risk": ecological_risk,

                # Provenance
                "data_source": "SYNTHETIC_DEMO_DATA",
            }
        )

    return pd.DataFrame(rows)


# ============================================================
# Save Agent-Specific Datasets
# ============================================================

def save_datasets(df):
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    # --------------------------------------------------------
    # Master dataset
    # --------------------------------------------------------

    master_path = (
        OUTPUT_DIR / "india_coastal.csv"
    )

    df.to_csv(
        master_path,
        index=False,
    )

    # --------------------------------------------------------
    # Marine Agent
    # --------------------------------------------------------

    marine_columns = [
        "id",
        "region",
        "latitude",
        "longitude",
        "timestamp",
        "sst",
        "sst_anomaly",
        "salinity",
        "wave_height",
        "current_speed",
        "current_direction",
        "data_source",
    ]

    df[marine_columns].to_csv(
        OUTPUT_DIR / "marine_observations.csv",
        index=False,
    )

    # --------------------------------------------------------
    # Weather Agent
    # --------------------------------------------------------

    weather_columns = [
        "id",
        "region",
        "latitude",
        "longitude",
        "timestamp",
        "wind_speed",
        "rainfall",
        "pressure",
        "humidity",
        "data_source",
    ]

    df[weather_columns].to_csv(
        OUTPUT_DIR / "weather_observations.csv",
        index=False,
    )

    # --------------------------------------------------------
    # Satellite Agent
    # --------------------------------------------------------

    satellite_columns = [
        "id",
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

    df[satellite_columns].to_csv(
        OUTPUT_DIR / "satellite_observations.csv",
        index=False,
    )

    # --------------------------------------------------------
    # Ecology Agent
    # --------------------------------------------------------

    ecology_columns = [
        "id",
        "region",
        "latitude",
        "longitude",
        "timestamp",
        "phytoplankton_index",
        "fish_activity_index",
        "biodiversity_index",
        "ecological_risk_score",
        "ecological_risk",
        "data_source",
    ]

    df[ecology_columns].to_csv(
        OUTPUT_DIR / "ecological_observations.csv",
        index=False,
    )


# ============================================================
# Main
# ============================================================

def main():
    print("=" * 70)
    print("ORCA — SYNTHETIC MARINE DATA GENERATOR")
    print("=" * 70)

    print(f"\nGenerating {N_OBSERVATIONS:,} observations...")
    print(f"Random seed: {SEED}")

    df = generate_dataset()

    save_datasets(df)

    print("\nDataset generation complete.")
    print("\nGenerated files:")

    files = [
        "india_coastal.csv",
        "marine_observations.csv",
        "weather_observations.csv",
        "satellite_observations.csv",
        "ecological_observations.csv",
    ]

    for filename in files:
        path = OUTPUT_DIR / filename
        size_kb = path.stat().st_size / 1024

        print(
            f"  ✓ {filename:<32} "
            f"{size_kb:>8.1f} KB"
        )

    print("\nDataset statistics:")
    print(f"  Observations : {len(df):,}")
    print(f"  Regions      : {df['region'].nunique()}")
    print(
        f"  Date range   : "
        f"{df['timestamp'].min()} → "
        f"{df['timestamp'].max()}"
    )

    print("\nRisk distribution:")
    print(
        df["ecological_risk"]
        .value_counts()
        .sort_index()
        .to_string()
    )

    print("\nData source:")
    print("  SYNTHETIC_DEMO_DATA")

    print("\nOutput directory:")
    print(f"  {OUTPUT_DIR}")

    print("\n" + "=" * 70)
    print("READY FOR ORCA AGENTS")
    print("=" * 70)


if __name__ == "__main__":
    main()