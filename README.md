# 🌟 Clarity PMA (Project Manager Assistant)

**Clarity PMA** is an intelligent, local-first Project Manager Assistant designed to automatically convert unstructured meeting notes and video transcripts into clear, actionable work items for your project management platform (Plane).

By leveraging local Large Language Models (LLMs) via **Ollama**, Clarity PMA acts as "The Watcher"—it analyzes your raw source material and generates structured task breakdowns, ensuring every decision and requirement from your transcripts is immediately captured in your project plan.

## 🚀 Key Features

- **Transcript-to-Task Conversion:** Automatically processes raw `.txt` transcripts (from meetings, videos, etc.) to identify tasks, owners, and next steps.
- **Structured Task Breakdown:** Guarantees reliable data by forcing the LLM (via Ollama) to return task data in a structured JSON schema.
- **Plane Integration:** Seamlessly posts the generated work items directly to your **Plane** project instance.
- **Local-First & Private:** Uses local models via Ollama, keeping your sensitive project transcripts secure and off public clouds.

---

## ⚙️ How It Works (The Workflow)

The **WorkflowManager** in Clarity PMA orchestrates a multi-step process to ensure a reliable conversion from unstructured text to structured tasks:

1.  **Load:** The `WorkflowManager` loads the transcript from `agent_data/transcripts/` and the system prompt.
2.  **Generate:** The content is sent to the local **Ollama** server, which applies the **Task Breakdown** prompt.
3.  **Parse:** The JSON response is strictly validated against the `WorkItem` schema.
4.  **Save:** The validated tasks are saved locally to `agent_data/work/`.
5.  **Post:** The tasks are uploaded directly to your configured **Plane** project via the API.

---

## 🛠️ Installation and Setup

To run **Clarity PMA**, you need to configure access to two core services: a local Large Language Model provider (**Ollama**) and your project management platform (**Plane**).

### 1. Configure the Environment File

Copy the example environment file and update it with your configuration details. This file is named `.env`.

```bash
cp example.env .env
```

#### 1.2. Create Data Directories 📁

The application requires specific folders for storing input transcripts and saving generated work items. Run the following command from the project root to create the necessary structure:

```bash
mkdir -p agent_data/transcripts agent_data/work
```

This creates the required paths:

`agent_data/transcripts/`: Where you place your input .txt files.

`agent_data/work/`: Where the structured JSON output is saved before (and after) posting to Plane.

### 2. Set Up Ollama (The AI Processor)

Clarity PMA needs a running Ollama server to handle the AI processing.

#### A. Install and Run Ollama

We recommend following the official instructions to install Ollama directly on your machine for the simplest setup:

Link: https://ollama.com/download

#### B. Download the Model

Once Ollama is running, you must pull the model specified in your configuration:

```bash
ollama pull llama3
```

Ensure the `MODEL_NAME` in your `.env` matches the model you pull (e.g., llama3:latest).

### 3. Set Up Plane (The Destination)

Clarity PMA uses the Plane API to post tasks.

Sign Up & Setup: Sign up for an account at Plane.so. Set up your target Workspace and Project.

Link: https://docs.plane.so

**Generate API Key**: Create a new API Key within your Plane settings and set this value as `PLANE_API_TOKEN` in your `.env`.

**Find IDs**: Copy your Workspace Slug and Project ID into the corresponding variables in `.env`, `PLANE_WORKSPACE_SLUG` and `PLANE_PROJECT_ID`

### 4. Install Python Dependencies

Install the necessary Python libraries from the `requirements.txt` file into your virtual environment:

```bash
# Create and Activate your environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## 🚀 Running Clarity PMA

Once all setup steps are complete, you can run the assistant from the root directory.

1. **Place Input**: Add the video transcript or meeting notes as a .txt file into the agent_data/transcripts/ directory.

2. **Execute**: Run the main script, passing the filename as an argument:

```bash
python main.py meeting_transcript.txt
```

The `WorkflowManager` will execute the full sequence, generating tasks, saving them locally, and posting them to your Plane project.

---

## 🤝 Contributing

We welcome contributions! If you have suggestions for new features, bug fixes, or integrations with other project management tools, please follow these steps:

1. Fork the repository.
2. Create a new feature branch (git checkout -b feature/new-feature).
3. Commit your changes (git commit -m 'Add some AmazingFeature').
4. Push to the branch (git push origin feature/new-feature).
5. Open a Pull Request.

We appreciate your help in making Clarity PMA better!

---

## ⚖️ License

Distributed under the MIT License. See LICENSE for more information.
