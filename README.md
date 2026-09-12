# ORCA — Marine EcOsystem Reasoning with Collaborative Agents

## SIH26176

**Organization:** Indian Space Research Organisation (ISRO)
**Category:** Software
**Problem Statement:** SIH26176
**Project Type:** Agentic Artificial Intelligence and Marine Intelligence Platform

---

## 1. Overview

ORCA (Marine EcOsystem Reasoning with Collaborative Agents) is an agentic artificial intelligence platform designed to support marine ecosystem analysis through collaborative specialized agents.

The system accepts natural-language queries related to marine and environmental conditions and coordinates multiple analytical agents to investigate oceanographic, meteorological, satellite-derived, and ecological information.

Instead of relying on a single analytical component, ORCA decomposes a query into domain-specific analysis tasks and combines their outputs through a dedicated reasoning layer.

The platform is designed around five principal capabilities:

* Marine condition analysis
* Weather and atmospheric condition analysis
* Satellite and spatial observation analysis
* Ecological condition and anomaly analysis
* Cross-domain reasoning and evidence synthesis

The current prototype operates using synthetic demonstration data specifically designed to model relationships between marine, weather, satellite, and ecological variables.

---

## 2. Problem Context

Marine ecosystems are influenced by multiple interacting environmental factors. Sea surface temperature, salinity, currents, wave conditions, atmospheric conditions, chlorophyll concentration, turbidity, biological activity, and other variables may need to be considered together when evaluating marine conditions.

Traditional analysis workflows often require users to manually access multiple datasets and independently interpret information from different domains.

ORCA addresses this workflow by providing an agent-based architecture capable of:

1. Understanding a natural-language query.
2. Identifying the relevant geographical region.
3. Delegating analysis to specialized agents.
4. Processing domain-specific observations.
5. Detecting anomalies and environmental stress indicators.
6. Combining evidence from multiple agents.
7. Producing an explainable assessment.
8. Returning supporting evidence and contributing factors.

---

## 3. Objectives

The primary objectives of ORCA are:

* Develop a collaborative multi-agent architecture for marine intelligence.
* Provide natural-language interaction with marine environmental data.
* Perform domain-specific marine, weather, satellite, and ecological analysis.
* Enable contextual reasoning across multiple environmental variables.
* Detect potentially abnormal or stressed environmental conditions.
* Provide evidence-grounded analytical responses.
* Maintain a modular architecture allowing additional data sources and agents to be integrated later.
* Provide a completely local fallback inference capability using Ollama.
* Demonstrate the proposed workflow using reproducible synthetic data.

---

## 4. System Architecture

ORCA follows a modular multi-agent architecture.

```text
                         User Query
                              |
                              v
                    +-------------------+
                    |   ORCA API Layer  |
                    +---------+---------+
                              |
                              v
                    +-------------------+
                    |    Orchestrator   |
                    +---------+---------+
                              |
             +----------------+----------------+
             |                |                |
             v                v                v
      +-------------+  +-------------+  +-------------+
      | Marine      |  | Weather     |  | Satellite   |
      | Agent       |  | Agent       |  | Agent       |
      +------+------+  +------+------+  +------+------+
             |                |                |
             +----------------+----------------+
                              |
                              v
                    +-------------------+
                    |  Ecology Agent    |
                    +---------+---------+
                              |
                              v
                    +-------------------+
                    | Reasoning Agent   |
                    +---------+---------+
                              |
                              v
                    +-------------------+
                    | Evidence-Based    |
                    | Response          |
                    +-------------------+
```

The architecture separates orchestration, domain analysis, data processing, AI inference, and presentation.

---

## 5. Specialized Agents

### 5.1 Marine Agent

The Marine Agent analyzes oceanographic variables including:

* Sea surface temperature
* Sea surface temperature anomalies
* Salinity
* Wave height
* Ocean current speed
* Ocean current direction

It produces domain-specific findings and supporting observations.

### 5.2 Weather Agent

The Weather Agent evaluates atmospheric and weather-related variables including:

* Wind speed
* Rainfall
* Atmospheric pressure
* Humidity

It classifies the observed weather conditions and contributes environmental context to the reasoning process.

### 5.3 Satellite Agent

The Satellite Agent performs spatial marine observation analysis using variables representing satellite-derived or spatially distributed observations.

Its analysis includes:

* Sea surface temperature
* Temperature anomalies
* Chlorophyll concentration
* Turbidity
* Eddy presence
* Geographic distribution of observations

### 5.4 Ecology Agent

The Ecology Agent evaluates ecosystem-level indicators including:

* Biodiversity index
* Fish activity index
* Phytoplankton index
* Environmental anomalies
* Ecological risk indicators

The agent combines ecological variables with anomaly detection results to identify potential environmental stress.

### 5.5 Reasoning Agent

The Reasoning Agent receives outputs from the specialized agents and performs cross-domain synthesis.

Its responsibilities include:

* Evidence aggregation
* Risk assessment
* Identification of contributing factors
* Finding synthesis
* Recommendation generation
* Natural-language response generation

The reasoning layer is explicitly designed to operate on supplied evidence rather than inventing observations unavailable in the analytical pipeline.

---

## 6. Data Processing Pipeline

The data pipeline consists of the following stages:

```text
Synthetic Data
      |
      v
Data Loader
      |
      v
Data Normalization
      |
      v
Query Layer
      |
      v
Domain Services
      |
      v
Specialized Agents
      |
      v
Anomaly Detection
      |
      v
Reasoning Agent
      |
      v
ORCA Response
```

The normalization layer performs operations such as:

* Column normalization
* Timestamp conversion
* Numeric conversion
* Coordinate validation
* Duplicate handling
* Missing-value handling
* Dataset ordering

---

## 7. Synthetic Demonstration Data

The current prototype uses synthetic data rather than claiming access to live ISRO or operational satellite datasets.

The datasets are generated specifically for demonstrating the ORCA architecture and include correlated marine, weather, satellite, and ecological observations.

The prototype contains approximately 5,000 observations covering 10 Indian coastal regions.

Example regions include:

* Sundarbans
* Odisha Coast
* Visakhapatnam
* Chennai Coast
* Kerala Coast
* Mumbai Coast
* Gujarat Coast
* Goa Coast
* Andaman & Nicobar
* Lakshadweep

The synthetic data is explicitly identified within the application as:

```text
SYNTHETIC_DEMO_DATA
```

This distinction is maintained to prevent the prototype from representing generated observations as operational or authoritative environmental measurements.

---

## 8. AI Architecture

ORCA uses a two-level AI inference strategy.

### Primary Model

Gemini is used as the primary reasoning model when an API key is configured and the service is available.

### Local Fallback

Ollama with `mistral:latest` provides a locally hosted fallback inference path.

```text
                  ORCA Reasoning Layer
                         |
                         v
                   AI Router
                   /        \
                  /          \
                 v            v
             Gemini        Ollama
             Primary       Fallback
```

The fallback architecture allows the analytical pipeline to continue operating without depending exclusively on an external model service.

---

## 9. Backend Architecture

The backend is implemented using Python and Flask.

```text
backend/
│
├── app.py
├── config.py
│
├── agents/
│   ├── orchestrator.py
│   ├── marine_agent.py
│   ├── weather_agent.py
│   ├── satellite_agent.py
│   ├── ecology_agent.py
│   └── reasoning_agent.py
│
├── ai/
│   ├── gemini.py
│   ├── ollama.py
│   └── router.py
│
├── data/
│   ├── loader.py
│   ├── normalizer.py
│   ├── query.py
│   └── schemas.py
│
├── services/
│   ├── marine_service.py
│   ├── weather_service.py
│   ├── spatial_service.py
│   └── anomaly_service.py
│
└── utils/
    ├── logger.py
    └── helpers.py
```

---

## 10. Frontend Architecture

The frontend uses standard web technologies without a frontend framework.

```text
frontend/
│
├── index.html
│
├── css/
│   └── style.css
│
└── js/
    ├── app.js
    ├── api.js
    ├── map.js
    └── ui.js
```

The interface provides:

* Natural-language query input
* Example queries
* Regional selection
* Agent execution status
* Risk assessment
* Findings
* Evidence trail
* System health information
* Synthetic data indicators

No external mapping service or map tile provider is required by the current prototype.

---

## 11. API Endpoints

The Flask backend exposes the following primary endpoints.

| Endpoint                 | Method | Purpose                                 |
| ------------------------ | ------ | --------------------------------------- |
| `/`                      | GET    | Serve ORCA frontend                     |
| `/api/health`            | GET    | System health and dataset status        |
| `/api/query`             | POST   | Process a natural-language marine query |
| `/api/locations`         | GET    | Retrieve supported coastal regions      |
| `/api/location/<region>` | GET    | Retrieve regional information           |
| `/api/capabilities`      | GET    | Retrieve ORCA capabilities              |

Example query request:

```json
{
  "query": "Analyze Chennai Coast."
}
```

---

## 12. Example Queries

The prototype supports natural-language queries such as:

```text
Analyze Chennai Coast.
```

```text
Ecological risk in Sundarbans?
```

```text
Which regions show environmental stress?
```

The orchestrator identifies the relevant region when possible and invokes the appropriate analytical agents.

---

## 13. Risk Assessment

ORCA generates an environmental risk assessment based on evidence collected by its analytical components.

The assessment contains:

* Risk level
* Risk score
* Explanation
* Contributing factors
* Key findings
* Recommendations

Anomaly detection currently evaluates indicators such as:

* Elevated SST anomaly
* Elevated turbidity
* High wave activity
* High wind activity
* Elevated rainfall
* Low biodiversity
* Low fish activity

These rules are intended for prototype demonstration and are not presented as operational environmental thresholds.

---

## 14. Explainability

Explainability is implemented through an evidence trail.

Each specialized agent contributes:

* Agent identity
* Analysis status
* Findings
* Metrics
* Evidence
* Confidence
* Data source designation

The final reasoning layer uses these outputs to construct the final assessment.

This provides visibility into how the final response was derived from the underlying analytical components.

---

## 15. Testing

The project includes automated tests covering the primary ORCA components.

```text
tests/
├── test_agents.py
├── test_api.py
├── test_data.py
└── test_orca.py
```

The integrated ORCA test suite contains 25 tests covering:

* Dataset loading
* Dataset schema
* Regional data
* Normalization
* Query processing
* Marine services
* Weather services
* Spatial services
* Anomaly detection
* Specialized agents
* AI routing
* Orchestration
* Full reasoning pipeline
* Flask API endpoints
* Frontend availability

Run the complete test suite with:

```bash
python -m unittest tests.test_orca -v
```

Current validation result:

```text
Ran 25 tests

OK
```

---

## 16. Installation

### Requirements

* Python 3.11 or later
* Git
* Ollama
* Internet connection for Gemini API usage
* Minimum recommended system memory: 8 GB

### Clone the Repository

```bash
git clone <repository-url>
cd ORCA_SIH26176_Demo
```

### Create a Virtual Environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 17. Environment Configuration

Create a `.env` file in the project root.

```env
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-3.1-flash-lite

OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=mistral:latest

FLASK_HOST=127.0.0.1
FLASK_PORT=5000
```

The Gemini API key should not be committed to the repository.

---

## 18. Ollama Configuration

Install Ollama and download the configured model:

```bash
ollama pull mistral:latest
```

Verify that Ollama is available:

```bash
ollama list
```

The application uses Ollama as the local AI fallback.

---

## 19. Generating Demonstration Data

The synthetic dataset can be regenerated using:

```bash
python scripts/generate_synthetic.py
```

The generated datasets are stored under:

```text
data/synthetic/
```

---

## 20. Running the Application

Start the Flask application from the project root:

```bash
python -m backend.app
```

The application runs by default at:

```text
http://127.0.0.1:5000
```

Open the address in a web browser to access the ORCA interface.

---

## 21. Project Structure

```text
ORCA_SIH26176_Demo/
│
├── README.md
├── requirements.txt
├── .env
├── .env.example
├── .gitignore
│
├── backend/
│   ├── app.py
│   ├── config.py
│   ├── agents/
│   ├── ai/
│   ├── data/
│   ├── services/
│   └── utils/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── synthetic/
│
├── scripts/
│   ├── generate_synthetic.py
│   └── preprocess.py
│
├── frontend/
│   ├── index.html
│   ├── css/
│   └── js/
│
└── tests/
    ├── test_agents.py
    ├── test_api.py
    ├── test_data.py
    └── test_orca.py
```

---

## 22. Design Principles

The prototype follows the following engineering principles:

### Modularity

Domain-specific capabilities are separated into independent services and agents.

### Separation of Concerns

Data processing, domain analysis, AI inference, orchestration, and presentation are implemented as separate layers.

### Evidence Grounding

The reasoning layer receives structured evidence from analytical agents before generating the final assessment.

### Local Fallback

The system can use Ollama for local inference when the primary Gemini service is unavailable.

### Reproducibility

Synthetic data generation and deterministic analytical components allow the prototype to be reproduced without requiring proprietary datasets.

### Extensibility

Additional data providers, domain agents, analytical services, and reasoning capabilities can be integrated without restructuring the complete system.

---

## 23. Current Prototype Scope

The current implementation demonstrates:

* Multi-agent marine analysis
* Cross-domain environmental reasoning
* Natural-language query processing
* Region-aware analysis
* Marine condition assessment
* Weather analysis
* Spatial and satellite-style analysis
* Ecological risk analysis
* Anomaly detection
* Evidence aggregation
* AI-assisted reasoning
* Local AI fallback
* REST API integration
* Interactive web interface
* Automated validation

The implementation is intended as a prototype demonstrator for SIH26176 rather than a production operational marine monitoring system.

---

## 24. Limitations

The current prototype has the following limitations:

1. The environmental observations are synthetic.
2. The prototype does not claim to provide live ISRO satellite observations.
3. Environmental thresholds used for anomaly detection are demonstration rules.
4. The system does not currently ingest operational satellite data streams.
5. The prototype does not implement a persistent database.
6. The current interface does not depend on an external map tile service.
7. AI-generated explanations depend on the availability and behavior of the configured inference model.

These limitations are intentional within the scope of the prototype demonstrator.

---

## 25. Future Development

Potential future development includes:

* Integration with authenticated satellite and oceanographic data services.
* Real-time marine data ingestion.
* Additional Indian coastal and offshore regions.
* Temporal trend analysis.
* Advanced spatial reasoning.
* Time-series anomaly detection.
* More specialized environmental agents.
* Historical event comparison.
* Multi-language natural-language interaction.
* Persistent conversational context.
* Advanced uncertainty estimation.
* Production-grade data governance and validation.
* Operational monitoring and alerting.

---

## 26. Security Considerations

API credentials are stored through environment variables and excluded from version control.

The application should not expose `.env` contents through the frontend or API.

Production deployment should additionally implement:

* Authentication
* Authorization
* Rate limiting
* Input validation
* API key rotation
* Secure secret management
* HTTPS
* Request logging
* Data access controls

---

## 27. Technology Stack

| Layer                      | Technology            |
| -------------------------- | --------------------- |
| Backend                    | Python, Flask         |
| API                        | REST                  |
| Data Processing            | Pandas, NumPy         |
| Scientific Data            | Xarray, netCDF4       |
| Machine Learning Utilities | Scikit-learn          |
| Data Validation            | Pydantic              |
| Primary AI                 | Gemini                |
| Local AI                   | Ollama                |
| Local Model                | Mistral               |
| Frontend                   | HTML, CSS, JavaScript |
| Configuration              | python-dotenv         |
| Testing                    | Python unittest       |
| Version Control            | Git                   |

---

## 28. License

This project is developed as a prototype for Smart India Hackathon 2026 and SIH problem statement SIH26176.

License and redistribution terms should be defined before public production distribution.

---

## 29. Acknowledgement

This prototype is developed in response to:

**Smart India Hackathon 2026 — SIH26176**

**ORCA: Marine EcOsystem Reasoning with Collaborative Agents**

**Organization: Indian Space Research Organisation (ISRO)**
# sih-176
