# 🌟 Clarity PMA (Project Manager Assistant)

Clarity PMA is an intelligent, local-first Project Manager Assistant designed to automatically convert unstructured meeting notes and video transcripts into clear, actionable work items for your project management platform.

By leveraging local Large Language Models (LLMs) via Ollama, Clarity PMA acts as "The Watcher"—it analyzes your raw source material and generates structured task breakdowns, ensuring every decision and requirement from your meetings is immediately captured in your plan.

## 🚀 Key Features

- **Transcript-to-Task Conversion:** Automatically processes raw `.txt` transcripts (from meetings, videos, etc.) to identify tasks, owners, and next steps.
- **Structured Output:** Guarantees reliable data by forcing the LLM (via Ollama) to return task data in a structured JSON schema.
- **Plane Integration:** Seamlessly posts the generated work items directly to your self-hosted **Plane** instance.
- **Local-First & Private:** Uses local models via Ollama, keeping your sensitive project transcripts secure and off public clouds.
- **Modular Python Architecture:** Easy to extend and customize thanks to its clean `clarity` module structure.

## ⚙️ How It Works

Clarity PMA follows a simple, robust workflow:

1.  **Input:** You place a meeting transcript (e.g., `meeting_transcript.txt`) into the `agent_data/transcripts/` directory.
2.  **Analysis:** `main.py` executes, reading the transcript and sending it to your local **Ollama** server.
3.  **Breakdown:** The LLM applies the **Task Breakdown** prompt and returns a structured JSON list of work items.
4.  **Integration:** The system validates the structured output and uses the `clarity/plane.py` module to post the new tasks directly to your Plane project.

## 🛠️ Installation and Setup

### Prerequisites

You must have the following running locally:

1.  **Docker** and **Docker Compose**
2.  **Ollama** server running (and a compatible model like `llama3` downloaded).
3.  A running instance of **Plane** (or access to its API).

### Step-by-Step

1.  **Clone the Repository:**

    ```bash
    git clone [YOUR_REPO_URL]
    cd clarity-pma
    ```

2.  **Configure Environment:**
    Copy the example environment file and fill in your details:

    ```bash
    cp example.env env
    ```

    Edit `env` to include your `PLANE_API_KEY`, `PLANE_PROJECT_ID`, and the local `OLLAMA_API_URL`.

3.  **Run with Docker Compose:**
    Use the provided `docker-compose.yaml` to ensure all services (or at least your local environment) are set up correctly.

4.  **Execute the Assistant:**
    Place a transcript file in `agent_data/transcripts/` and run the main script:
    ```bash
    python main.py
    ```

## 🏗️ Project Structure

The project is logically divided into a core `clarity` package and configuration/data directories:

## 🤝 Contribution

Contributions are welcome! If you have ideas for adding support for other project management tools (like Jira, GitLab), improving the prompt engineering, or enhancing the JSON parsing, please open an issue or submit a pull request.
