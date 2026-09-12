from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

from backend.config import config
from backend.agents.orchestrator import ORCAOrchestrator
from backend.data.loader import data_loader
from backend.data.normalizer import DataNormalizer
import traceback

ROOT_DIR = Path(__file__).resolve().parents[1]
FRONTEND_DIR = ROOT_DIR / "frontend"


app = Flask(__name__)
CORS(app)


def initialize_orca():
    """Load and normalize the ORCA synthetic dataset."""

    datasets = data_loader.load_all()

    master = datasets["master"]

    normalizer = DataNormalizer()
    master = normalizer.normalize(master)

    return master


DATAFRAME = initialize_orca()
ORCHESTRATOR = ORCAOrchestrator(DATAFRAME)


# ============================================================
# FRONTEND
# ============================================================

@app.route("/", methods=["GET"])
def frontend():
    return send_from_directory(
        FRONTEND_DIR,
        "index.html",
    )


@app.route("/chat", methods=["GET"])
def chat():
    return send_from_directory(
        FRONTEND_DIR,
        "chat.html",
    )


@app.route("/css/<path:filename>", methods=["GET"])
def frontend_css(filename):
    return send_from_directory(
        FRONTEND_DIR / "css",
        filename,
    )


@app.route("/js/<path:filename>", methods=["GET"])
def frontend_js(filename):
    return send_from_directory(
        FRONTEND_DIR / "js",
        filename,
    )


# ============================================================
# API
# ============================================================

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify(
        {
            "status": "healthy",
            "application": config.APP_NAME,
            "version": config.APP_VERSION,
            "data_mode": config.DATA_MODE,
            "records": len(DATAFRAME),
        }
    )


@app.route("/api/query", methods=["POST"])
def query():
    payload = request.get_json(silent=True) or {}

    user_query = payload.get("query", "")

    if not isinstance(user_query, str) or not user_query.strip():
        return (
            jsonify(
                {
                    "success": False,
                    "error": "Query cannot be empty.",
                }
            ),
            400,
        )

    try:
        result = ORCHESTRATOR.run(user_query)

        if hasattr(result, "model_dump"):
            response = result.model_dump()
        else:
            response = result

        response["success"] = True

        return jsonify(response)

    except Exception as exc:
        print("\n" + "=" * 70)
        print("ORCA QUERY ERROR")
        print("=" * 70)
        traceback.print_exc()
        print("=" * 70 + "\n")

        return (
            jsonify(
                {
                    "success": False,
                    "error": str(exc),
                }
            ),
            500,
        )


@app.route("/api/locations", methods=["GET"])
def locations():
    columns = [
        "region",
        "latitude",
        "longitude",
    ]

    available_columns = [
        column
        for column in columns
        if column in DATAFRAME.columns
    ]

    locations_data = (
        DATAFRAME[available_columns]
        .drop_duplicates("region")
        .to_dict(orient="records")
    )

    return jsonify(
        {
            "success": True,
            "data_mode": config.DATA_MODE,
            "locations": locations_data,
        }
    )


@app.route("/api/location/<path:region>", methods=["GET"])
def location(region):
    region_data = DATAFRAME[
        DATAFRAME["region"].str.lower() == region.lower()
    ]

    if region_data.empty:
        return (
            jsonify(
                {
                    "success": False,
                    "error": f"Region '{region}' not found.",
                }
            ),
            404,
        )

    result = ORCHESTRATOR.run(
        f"Analyze the marine ecosystem conditions in {region}."
    )

    if hasattr(result, "model_dump"):
        response = result.model_dump()
    else:
        response = result

    response["success"] = True

    return jsonify(response)


@app.route("/api/capabilities", methods=["GET"])
def capabilities():
    return jsonify(
        {
            "success": True,
            "capabilities": ORCHESTRATOR.capabilities(),
        }
    )


if __name__ == "__main__":
    app.run(
        host=config.HOST,
        port=config.PORT,
        debug=config.DEBUG,
    )
