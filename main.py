import sys
from clarity.clients.azure import AzureClient
from clarity.clients.github import GithubClient
from clarity.config import Config
from clarity.manager import WorkflowManager
from clarity.prompt import PromptType
from clarity.work_item import WorkItem

if __name__ == "__main__":
    # filename = sys.argv[1]

    # pm = WorkflowManager.ollama_azure()
    # pm = WorkflowManager.ollama_console()
    # pm = WorkflowManager.ollama_plane()
    # pm = WorkflowManager.ollama_github()

    # iteration = "TCS7"
    # prompt = PromptType.C

    # pm.run(filename, prompt_type=prompt, iteration=iteration)

    config = Config()
    client = GithubClient(config)
    client.list_work_items(config.GITHUB_ORG, config.GITHUB_PROJECT)

    # az = AzureClient(config)
    # # az.list_work_items(config.AZURE_WORKSPACE, config.AZURE_PROJECT)

    # wi = WorkItem.create_dummy_item()
    # az.create_work_item(config.AZURE_WORKSPACE, config.AZURE_PROJECT, wi, iteration)
