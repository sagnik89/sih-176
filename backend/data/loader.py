from pathlib import Path
from typing import Dict

import pandas as pd


# ============================================================
# ORCA — Data Loader
# ============================================================

ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = ROOT / "data" / "synthetic"


DATASETS = {
    "master": "india_coastal.csv",
    "marine": "marine_observations.csv",
    "weather": "weather_observations.csv",
    "satellite": "satellite_observations.csv",
    "ecology": "ecological_observations.csv",
}


class ORCADataLoader:
    """Loads and provides access to ORCA synthetic datasets."""

    def __init__(self):
        self.datasets: Dict[str, pd.DataFrame] = {}

    def load_all(self) -> Dict[str, pd.DataFrame]:
        """Load all available datasets."""

        for name, filename in DATASETS.items():
            path = DATA_DIR / filename

            if not path.exists():
                raise FileNotFoundError(
                    f"Dataset not found: {path}"
                )

            self.datasets[name] = pd.read_csv(path)

        return self.datasets

    def get(self, dataset_name: str) -> pd.DataFrame:
        """Return a loaded dataset."""

        if dataset_name not in self.datasets:
            raise KeyError(
                f"Dataset '{dataset_name}' is not loaded."
            )

        return self.datasets[dataset_name]

    def load(self, dataset_name: str) -> pd.DataFrame:
        """Load and return a single dataset."""

        if dataset_name not in DATASETS:
            raise KeyError(
                f"Unknown dataset: {dataset_name}"
            )

        path = DATA_DIR / DATASETS[dataset_name]

        if not path.exists():
            raise FileNotFoundError(
                f"Dataset not found: {path}"
            )

        dataframe = pd.read_csv(path)
        self.datasets[dataset_name] = dataframe

        return dataframe

    def dataset_info(self) -> Dict[str, dict]:
        """Return basic information about loaded datasets."""

        info = {}

        for name, dataframe in self.datasets.items():
            info[name] = {
                "rows": len(dataframe),
                "columns": list(dataframe.columns),
            }

        return info

    def reload(self) -> Dict[str, pd.DataFrame]:
        """Clear cached datasets and load everything again."""

        self.datasets.clear()

        return self.load_all()


# ============================================================
# Shared Loader Instance
# ============================================================

data_loader = ORCADataLoader()