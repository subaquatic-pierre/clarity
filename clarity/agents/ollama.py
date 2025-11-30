import ollama
from ollama import Client

from clarity.agents.interface import IAgent
from clarity.config import Config
from clarity.work_item import WorkItemList
from clarity.log import logger


class OllamaAgent(IAgent):
    def __init__(self, config: Config) -> None:
        self.model_name: str = config.MODEL_NAME

        ollama_client = Client(host=config.OLLAMA_HOST_URL)
        self.client: Client = ollama_client

    def generate_work_items(self, prompt: str, transcript: str) -> str:
        """Sends the transcript and prompt to the local Ollama API using the OllamaAgent."""
        # 3. Use the imported 'logger' directly
        logger.info(f"Sending transcript to {self.model_name} for analysis...")

        raw_json_string = ""

        try:
            messages = [
                {"role": "system", "content": prompt},
                {"role": "user", "content": transcript},
            ]

            response = self.client.chat(
                model=self.model_name,
                messages=messages,
                format=WorkItemList.model_json_schema(),
                options={
                    "temperature": 0,
                },
            )

            raw_json_string = response["message"]["content"].strip()
            # 4. Use logger.success
            logger.success("Ollama analysis completed successfully.")

        except ollama.ResponseError as e:
            # 5. Use logger.error
            logger.error(f"Ollama API call failed with a response error. Details: {e}")

        except Exception as e:
            # 6. Use logger.error
            logger.error(
                f"Could not connect to Ollama. Ensure Ollama is running and the port is mapped correctly. Details: {e}"
            )

        return raw_json_string
