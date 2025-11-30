from abc import ABC, abstractmethod


class IAgent(ABC):
    @abstractmethod
    def generate_work_items(self, prompt: str, transcript: str) -> str:
        """Sends the transcript and prompt to the local Ollama API using the OllamaAgent."""
