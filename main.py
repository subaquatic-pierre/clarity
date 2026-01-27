import sys
from clarity.clients.azure import AzureClient
from clarity.config import Config
from clarity.manager import WorkflowManager
from clarity.prompt import PromptType
from clarity.work_item import WorkItem

if __name__ == "__main__":
    filename = sys.argv[1]
    pm = WorkflowManager.ollama_azure()
    # pm = WorkflowManager.ollama_console()
    # pm = WorkflowManager.ollama_plane()

    iteration = "TCS7"
    prompt = PromptType.C

    pm.run(filename, prompt_type=prompt, iteration=iteration)

    # config = Config()

    # az = AzureClient(config)
    # # az.list_work_items(config.AZURE_WORKSPACE, config.AZURE_PROJECT)

    # wi = WorkItem.create_dummy_item()
    # az.create_work_item(config.AZURE_WORKSPACE, config.AZURE_PROJECT, wi, iteration)
