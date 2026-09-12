from pathlib import Path

# Root folder is the current directory
ROOT = Path.cwd()

# Directories to create
directories = [
    # Backend
    "backend",
    "backend/agents",
    "backend/ai",
    "backend/data",
    "backend/services",
    "backend/utils",

    # Data
    "data",
    "data/raw",
    "data/raw/oceanography",
    "data/raw/eddy",
    "data/raw/icoads",
    "data/processed",
    "data/synthetic",

    # Scripts
    "scripts",

    # Frontend
    "frontend",
    "frontend/css",
    "frontend/js",

    # Tests
    "tests",
]

# Files to create
files = [
    # Root
    "README.md",
    "requirements.txt",
    ".env",
    ".env.example",
    ".gitignore",

    # Backend
    "backend/app.py",
    "backend/config.py",

    # Agents
    "backend/agents/__init__.py",
    "backend/agents/orchestrator.py",
    "backend/agents/marine_agent.py",
    "backend/agents/weather_agent.py",
    "backend/agents/satellite_agent.py",
    "backend/agents/ecology_agent.py",
    "backend/agents/reasoning_agent.py",

    # AI
    "backend/ai/__init__.py",
    "backend/ai/gemini.py",
    "backend/ai/ollama.py",
    "backend/ai/router.py",

    # Data
    "backend/data/__init__.py",
    "backend/data/loader.py",
    "backend/data/normalizer.py",
    "backend/data/query.py",
    "backend/data/schemas.py",

    # Services
    "backend/services/__init__.py",
    "backend/services/marine_service.py",
    "backend/services/weather_service.py",
    "backend/services/spatial_service.py",
    "backend/services/anomaly_service.py",

    # Utils
    "backend/utils/__init__.py",
    "backend/utils/logger.py",
    "backend/utils/helpers.py",

    # Scripts
    "scripts/generate_synthetic.py",
    "scripts/preprocess.py",

    # Frontend
    "frontend/index.html",
    "frontend/css/style.css",
    "frontend/js/app.js",
    "frontend/js/api.js",
    "frontend/js/map.js",
    "frontend/js/ui.js",

    # Tests
    "tests/test_agents.py",
    "tests/test_data.py",
    "tests/test_api.py",
]


def create_structure():
    print("=" * 60)
    print("ORCA PROJECT STRUCTURE CREATOR")
    print("=" * 60)
    print(f"\nRoot: {ROOT}\n")

    # Create directories
    print("Creating directories...")
    for directory in directories:
        path = ROOT / directory
        path.mkdir(parents=True, exist_ok=True)
        print(f"  [DIR]  {directory}")

    # Create files only if they don't already exist
    print("\nCreating files...")
    for file in files:
        path = ROOT / file

        if path.exists():
            print(f"  [SKIP] {file} (already exists)")
        else:
            path.touch()
            print(f"  [FILE] {file}")

    print("\n" + "=" * 60)
    print("ORCA PROJECT STRUCTURE CREATED")
    print("=" * 60)

    print("\nProject location:")
    print(ROOT)

    print("\nNext step:")
    print("Install dependencies with:")
    print("    pip install -r requirements.txt")


if __name__ == "__main__":
    create_structure()