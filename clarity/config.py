import os
import sys
from dotenv import dotenv_values
from typing import Dict, Any

try:
    entry_script_path = os.path.abspath(sys.argv[0])
    base_directory = os.path.dirname(entry_script_path)
    if not os.path.isdir(base_directory) or base_directory == "":
        base_directory = os.getcwd()
except Exception:
    base_directory = os.getcwd()

ABSOLUTE_BASE_PATH = os.path.abspath(base_directory)


class Config:
    _env_config: Dict[str, Any] = dotenv_values(
        os.path.join(ABSOLUTE_BASE_PATH, ".env")
    )

    BASE_PATH = ABSOLUTE_BASE_PATH

    # Ollama config
    OLLAMA_HOST_URL = _env_config.get("OLLAMA_HOST_URL", "http://localhost:11434")
    MODEL_NAME = _env_config.get("MODEL_NAME", "llama3:latest")

    # Plane Config
    PLANE_HOST_URL = _env_config.get("PLANE_HOST_URL", "http://localhost:80")
    PLANE_API_TOKEN = _env_config.get(
        "PLANE_API_TOKEN", "plane_api_1e1553d4385f4a1b98c52e0c406ad95a"
    )
    PLANE_WORKSPACE_SLUG = _env_config.get("PLANE_WORKSPACE_SLUG", "anyllm")
    PLANE_PROJECT_ID = _env_config.get(
        "PLANE_PROJECT_ID", "1e8bde5b-9e49-45a4-8b43-10341429f1e3"
    )

    # Azure Config
    AZURE_HOST_URL = _env_config.get(
        "AZURE_HOST_URL", "1e8bde5b-9e49-45a4-8b43-10341429f1e3"
    )

    AZURE_PAT = _env_config.get("AZURE_PAT", "1e8bde5b-9e49-45a4-8b43-10341429f1e3")
    AZURE_PROJECT = _env_config.get(
        "AZURE_PROJECT", "1e8bde5b-9e49-45a4-8b43-10341429f1e3"
    )
    AZURE_WORKSPACE = _env_config.get(
        "AZURE_WORKSPACE", "1e8bde5b-9e49-45a4-8b43-10341429f1e3"
    )

    TRANSCRIPT_REL_PATH = "data/transcripts"
    WORK_PACKAGE_REL_PATH = "data/work"

    # Construct the final absolute paths using os.path.join
    TRANSCRIPT_PATH = os.path.join(BASE_PATH, TRANSCRIPT_REL_PATH)
    WORK_PACKAGE_PATH = os.path.join(BASE_PATH, WORK_PACKAGE_REL_PATH)

    # Clean up the temporary config dict
    del _env_config
