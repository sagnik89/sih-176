import unittest

import pandas as pd

from backend.agents.ecology_agent import EcologyAgent
from backend.agents.marine_agent import MarineAgent
from backend.agents.satellite_agent import SatelliteAgent
from backend.agents.weather_agent import WeatherAgent
from backend.agents.reasoning_agent import ReasoningAgent
from backend.agents.orchestrator import ORCAOrchestrator

from backend.ai.router import ai_router

from backend.data.loader import ORCADataLoader
from backend.data.normalizer import DataNormalizer
from backend.data.query import DataQuery

from backend.services.anomaly_service import AnomalyService
from backend.services.marine_service import MarineService
from backend.services.weather_service import WeatherService
from backend.services.spatial_service import SpatialService

from backend.app import app, DATAFRAME, ORCHESTRATOR


class TestORCA(unittest.TestCase):
    """Complete ORCA prototype test suite."""

    @classmethod
    def setUpClass(cls):
        cls.dataframe = DATAFRAME
        cls.orchestrator = ORCHESTRATOR

        cls.client = app.test_client()

    # ==========================================================
    # DATA LAYER
    # ==========================================================

    def test_01_dataset_loaded(self):

        self.assertIsInstance(
            self.dataframe,
            pd.DataFrame,
        )

        self.assertGreater(
            len(self.dataframe),
            0,
        )

        self.assertGreaterEqual(
            len(self.dataframe),
            5000,
        )


    def test_02_required_columns_exist(self):

        required_columns = [
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
            "wind_speed",
            "rainfall",
            "pressure",
            "humidity",
            "chlorophyll",
            "turbidity",
            "phytoplankton_index",
            "fish_activity_index",
            "biodiversity_index",
            "ecological_risk_score",
            "ecological_risk",
            "data_source",
        ]

        for column in required_columns:

            self.assertIn(
                column,
                self.dataframe.columns,
                f"Missing column: {column}",
            )


    def test_03_regions_exist(self):

        regions = (
            self.dataframe["region"]
            .dropna()
            .unique()
            .tolist()
        )

        expected_regions = [
            "Sundarbans",
            "Odisha Coast",
            "Visakhapatnam",
            "Chennai Coast",
            "Kerala Coast",
            "Mumbai Coast",
            "Gujarat Coast",
            "Goa Coast",
            "Andaman & Nicobar",
            "Lakshadweep",
        ]

        for region in expected_regions:

            self.assertIn(
                region,
                regions,
            )

        self.assertEqual(
            len(regions),
            10,
        )


    def test_04_normalizer(self):

        normalizer = DataNormalizer()

        result = normalizer.normalize(
            self.dataframe.copy()
        )

        self.assertIsInstance(
            result,
            pd.DataFrame,
        )

        self.assertFalse(
            result.empty
        )


    def test_05_query_layer(self):

        query = DataQuery(
            self.dataframe
        )

        chennai = query.by_region(
            "Chennai Coast"
        )

        self.assertFalse(
            chennai.empty
        )

        self.assertTrue(
            all(
                chennai["region"]
                == "Chennai Coast"
            )
        )

        latest = query.latest(
            region="Chennai Coast",
            limit=5,
        )

        self.assertLessEqual(
            len(latest),
            5,
        )


    # ==========================================================
    # SERVICES
    # ==========================================================

    def test_06_marine_service(self):

        service = MarineService(
            self.dataframe
        )

        result = service.analyze(
            "Chennai Coast"
        )

        self.assertEqual(
            result["status"],
            "success",
        )

        self.assertIn(
            "sst",
            result["metrics"],
        )

        self.assertIn(
            "salinity",
            result["metrics"],
        )


    def test_07_weather_service(self):

        service = WeatherService(
            self.dataframe
        )

        result = service.analyze(
            "Chennai Coast"
        )

        self.assertEqual(
            result["status"],
            "success",
        )

        self.assertIn(
            "wind_speed",
            result["metrics"],
        )

        self.assertIn(
            "rainfall",
            result["metrics"],
        )


    def test_08_spatial_service(self):

        service = SpatialService(
            self.dataframe
        )

        result = service.analyze(
            "Chennai Coast"
        )

        self.assertEqual(
            result["status"],
            "success",
        )

        self.assertIn(
            "chlorophyll",
            result["metrics"],
        )

        self.assertIn(
            "turbidity",
            result["metrics"],
        )


    def test_09_anomaly_service(self):

        service = AnomalyService()

        result = service.detect(
            self.dataframe
        )

        self.assertIn(
            "score",
            result,
        )

        self.assertIn(
            "severity",
            result,
        )

        self.assertIn(
            "count",
            result,
        )

        self.assertGreaterEqual(
            result["score"],
            0.0,
        )

        self.assertLessEqual(
            result["score"],
            1.0,
        )


    # ==========================================================
    # SPECIALIZED AGENTS
    # ==========================================================

    def test_10_marine_agent(self):

        agent = MarineAgent(
            self.dataframe
        )

        result = agent.run(
            "Chennai Coast"
        )

        self.assertEqual(
            result.agent,
            "MarineAgent",
        )

        self.assertEqual(
            result.region,
            "Chennai Coast",
        )

        self.assertGreater(
            result.confidence,
            0,
        )

        self.assertGreater(
            len(result.findings),
            0,
        )


    def test_11_weather_agent(self):

        agent = WeatherAgent(
            self.dataframe
        )

        result = agent.run(
            "Chennai Coast"
        )

        self.assertEqual(
            result.agent,
            "WeatherAgent",
        )

        self.assertEqual(
            result.region,
            "Chennai Coast",
        )

        self.assertGreater(
            len(result.metrics),
            0,
        )


    def test_12_satellite_agent(self):

        agent = SatelliteAgent(
            self.dataframe
        )

        result = agent.run(
            "Chennai Coast"
        )

        self.assertEqual(
            result.agent,
            "SatelliteAgent",
        )

        self.assertEqual(
            result.region,
            "Chennai Coast",
        )

        self.assertIn(
            "chlorophyll",
            result.metrics,
        )


    def test_13_ecology_agent(self):

        agent = EcologyAgent(
            self.dataframe
        )

        result = agent.run(
            "Chennai Coast"
        )

        self.assertEqual(
            result.agent,
            "EcologyAgent",
        )

        self.assertEqual(
            result.region,
            "Chennai Coast",
        )

        self.assertIn(
            "ecological_risk_score",
            result.metrics,
        )

        self.assertIn(
            "anomaly_score",
            result.metrics,
        )


    # ==========================================================
    # REASONING
    # ==========================================================

    def test_14_reasoning_agent(self):

        agent = ReasoningAgent()

        evidence = [
            {
                "agent": "MarineAgent",
                "status": "success",
                "region": "Chennai Coast",
                "findings": [
                    "Marine conditions are relatively stable."
                ],
                "metrics": {
                    "sst": 29.4,
                    "sst_anomaly": 0.8,
                },
                "evidence": [],
                "confidence": 0.85,
                "data_source": "SYNTHETIC_DEMO_DATA",
            }
        ]

        result = agent.run(
            query="Analyze Chennai Coast.",
            evidence=evidence,
        )

        self.assertIn(
            "answer",
            result,
        )

        self.assertIn(
            "risk_level",
            result,
        )

        self.assertIn(
            "risk_score",
            result,
        )

        self.assertIn(
            "key_findings",
            result,
        )

        self.assertIn(
            "contributing_factors",
            result,
        )


    # ==========================================================
    # AI ROUTER
    # ==========================================================

    def test_15_ai_router_status(self):

        status = ai_router.status()

        self.assertIn(
            "gemini",
            status,
        )

        self.assertIn(
            "ollama",
            status,
        )

        self.assertIn(
            "model",
            status["gemini"],
        )

        self.assertIn(
            "model",
            status["ollama"],
        )


    # ==========================================================
    # ORCHESTRATOR
    # ==========================================================

    def test_16_orchestrator_region_detection(self):

        region = (
            self.orchestrator
            ._detect_region(
                "Analyze Chennai Coast."
            )
        )

        self.assertEqual(
            region,
            "Chennai Coast",
        )


    def test_17_orchestrator_agents(self):

        evidence = (
            self.orchestrator
            ._run_specialized_agents(
                "Chennai Coast"
            )
        )

        self.assertEqual(
            len(evidence),
            4,
        )

        agent_names = [
            item["agent"]
            for item in evidence
        ]

        expected_agents = [
            "MarineAgent",
            "WeatherAgent",
            "SatelliteAgent",
            "EcologyAgent",
        ]

        for agent in expected_agents:

            self.assertIn(
                agent,
                agent_names,
            )


    def test_18_orchestrator_full_pipeline(self):

        result = self.orchestrator.run(
            "Analyze Chennai Coast."
        )

        self.assertEqual(
            result.region,
            "Chennai Coast",
        )

        self.assertGreater(
            len(result.agents_used),
            0,
        )

        self.assertGreater(
            len(result.evidence),
            0,
        )

        self.assertTrue(
            result.answer
        )

        self.assertIsNotNone(
            result.risk
        )


    # ==========================================================
    # FLASK API
    # ==========================================================

    def test_19_health_api(self):

        response = self.client.get(
            "/api/health"
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        data = response.get_json()

        self.assertEqual(
            data["status"],
            "healthy",
        )

        self.assertEqual(
            data["application"],
            "ORCA",
        )

        self.assertGreaterEqual(
            data["records"],
            5000,
        )


    def test_20_locations_api(self):

        response = self.client.get(
            "/api/locations"
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        data = response.get_json()

        self.assertTrue(
            data["success"]
        )

        self.assertEqual(
            len(data["locations"]),
            10,
        )


    def test_21_capabilities_api(self):

        response = self.client.get(
            "/api/capabilities"
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        data = response.get_json()

        self.assertTrue(
            data["success"]
        )

        self.assertIn(
            "MarineAgent",
            data["capabilities"],
        )

        self.assertIn(
            "WeatherAgent",
            data["capabilities"],
        )

        self.assertIn(
            "SatelliteAgent",
            data["capabilities"],
        )

        self.assertIn(
            "EcologyAgent",
            data["capabilities"],
        )

        self.assertIn(
            "ReasoningAgent",
            data["capabilities"],
        )


    def test_22_query_api(self):

        response = self.client.post(
            "/api/query",
            json={
                "query":
                    "Analyze Chennai Coast."
            },
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        data = response.get_json()

        self.assertTrue(
            data["success"]
        )

        self.assertEqual(
            data["region"],
            "Chennai Coast",
        )

        self.assertTrue(
            data["answer"]
        )

        self.assertIsNotNone(
            data["risk"]
        )

        self.assertGreater(
            len(data["evidence"]),
            0,
        )


    def test_23_empty_query_api(self):

        response = self.client.post(
            "/api/query",
            json={
                "query": ""
            },
        )

        self.assertEqual(
            response.status_code,
            400,
        )

        data = response.get_json()

        self.assertFalse(
            data["success"]
        )


    def test_24_invalid_region_api(self):

        response = self.client.get(
            "/api/location/DoesNotExist"
        )

        self.assertEqual(
            response.status_code,
            404,
        )


    # ==========================================================
    # FRONTEND
    # ==========================================================

    def test_25_frontend(self):

        response = self.client.get(
            "/"
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        html = response.get_data(
            as_text=True
        )

        self.assertIn(
            "ORCA",
            html,
        )

        self.assertIn(
            "Ask ORCA",
            html,
        )

        self.assertIn(
            "SYNTHETIC DEMO DATA",
            html,
        )


if __name__ == "__main__":
    unittest.main(
        verbosity=2
    )