from typing import List

from clarity.agents.interface import IAgent
from clarity.clients.interface import IClient
from clarity.log import logger
from clarity.parse import WorkflowManagerParser
from clarity.clients.plane import PlaneClient
from clarity.prompt import PromptType, SystemPrompt
from clarity.storage import Storage
from clarity.agents.ollama import OllamaAgent
from clarity.work_item import WorkItem
from clarity.config import Config


class WorkflowManager:
    client: IClient
    agent: IAgent

    def __init__(self, agent: IAgent, client: IClient, config: Config):
        self.agent = agent
        self.client = client

        self.store = Storage(config)
        self.config = config

        logger.info("WorkflowManager initialized successfully.")
        logger.info(f"Targeting model: {self.config.MODEL_NAME}")
        logger.info(f"Using Plane Host: {self.config.PLANE_HOST_URL}")

    def load_transcript(self, filename: str) -> str:
        """Loads the transcript file content."""
        content = self.store.read_transcript(filename)
        return content

    def load_prompt(self, prompt_type: PromptType) -> str:
        """Loads the system prompt content based on the type."""
        prompt = SystemPrompt(prompt_type)
        return prompt.content()

    def save_work_items(self, work_items: List[WorkItem]) -> None:
        """Saves the generated work items to a local JSON file."""
        self.store.save_work_items(work_items)

    def generate_work_items(
        self, transcript_filename: str, prompt_type: PromptType = PromptType.A
    ) -> List[WorkItem]:
        """
        Loads prompt and transcript, sends to Ollama, and parses the JSON response.
        """
        logger.info(f"Starting work item generation process.")

        # 1. Load Data
        transcript = self.load_transcript(transcript_filename)
        if not transcript:
            logger.error(
                f"Transcript file '{transcript_filename}' could not be loaded. Aborting generation."
            )
            return []

        prompt = self.load_prompt(prompt_type)

        # 2. Generate Response
        response = self.agent.generate_work_items(prompt, transcript)

        if not response:
            logger.error("Ollama returned an empty response. Cannot parse work items.")
            return []

        work_items = WorkflowManagerParser.parse_work_package_json_str(response)

        if not work_items:
            logger.warning("No valid work items were extracted from the AI response.")
            return []

        logger.success(
            f"Successfully extracted and validated {len(work_items)} work items."
        )
        return work_items

    def create_plane_tasks(self, work_items: List[WorkItem]) -> None:
        """Uploads the generated work items to the Plane project management tool."""

        workspace_slug = self.config.PLANE_WORKSPACE_SLUG
        project_id = self.config.PLANE_PROJECT_ID

        if not workspace_slug or not project_id:
            logger.error(
                "Plane configuration (workspace_slug/project_id) is missing. Skipping upload."
            )
            return

        logger.info(
            f"Attempting to create {len(work_items)} items in Plane Project {project_id}..."
        )

        success = self.client.create_work_items(workspace_slug, project_id, work_items)

        if success:
            logger.success("All work items successfully posted to Plane.")
        else:
            logger.error(
                "One or more work items failed to post to Plane. Check previous error logs."
            )

    def run(
        self,
        transcript_filename: str = "meeting_transcript.txt",
        prompt_type: PromptType = PromptType.B,
    ) -> None:
        """
        The main execution flow: loads transcript, generates tasks, saves locally, and posts to Plane.
        """
        logger.info("--- Starting WorkflowManager Run ---")

        # 1. Generate Work Items
        work_items = self.generate_work_items(transcript_filename, prompt_type)

        if not work_items:
            logger.error("Run aborted: No work items generated.")
            return

        # 2. Save Locally
        self.save_work_items(work_items)

        # 3. Create Plane Tasks
        self.create_plane_tasks(work_items)

        logger.info("--- WorkflowManager Run Complete ---")

    @staticmethod
    def ollama_plane():
        config = Config()
        agent = OllamaAgent(config)
        client = PlaneClient(config)
        return WorkflowManager(agent, client, config)

    @staticmethod
    def ollama_azure():
        config = Config()
        agent = OllamaAgent(config)
        client = PlaneClient(config)
        return WorkflowManager(agent, client, config)
