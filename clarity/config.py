import os
import sys

# --- Dynamic Path Calculation (as shown above) ---
# This block should be run once, typically in your main setup file or the config file itself.
try:
    # Use the directory of the file that Python recognized as the entry point
    entry_script_path = os.path.abspath(sys.argv[0])
    base_directory = os.path.dirname(entry_script_path)

    # Final check: ensure the path exists or fallback
    if not os.path.isdir(base_directory) or base_directory == "":
        base_directory = os.getcwd()

except Exception:
    # Safest fallback if sys.argv[0] is unreliable (e.g., in some IDEs)
    base_directory = os.getcwd()

# Use an absolute path to ensure consistency
ABSOLUTE_BASE_PATH = os.path.abspath(base_directory)
# --------------------------------------------------


class Config:
    # --- CONFIGURATION ---
    # Set the dynamically determined path
    BASE_PATH = ABSOLUTE_BASE_PATH

    # Ollama Config
    OLLAMA_HOST_URL = "http://localhost:11434"
    MODEL_NAME = "llama3:latest"

    # Plane Config
    PLANE_HOST_URL = "http://localhost:80"
    PLANE_API_TOKEN = "plane_api_1e1553d4385f4a1b98c52e0c406ad95a"
    PLANE_WORKSPACE_SLUG = "anyllm"
    PLANE_PROJECT_ID = "1e8bde5b-9e49-45a4-8b43-10341429f1e3"

    # Define relative paths for data directories
    TRANSCRIPT_REL_PATH = "agent_data/transcripts"
    WORK_PACKAGE_REL_PATH = "agent_data/work"

    # Construct the final absolute paths using os.path.join
    # This ensures that your application always knows exactly where to find/save files
    TRANSCRIPT_PATH = os.path.join(BASE_PATH, TRANSCRIPT_REL_PATH)
    WORK_PACKAGE_PATH = os.path.join(BASE_PATH, WORK_PACKAGE_REL_PATH)
