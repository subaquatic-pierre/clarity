from typing import List

# Import necessary types/interfaces from your local clarity modules
from clarity.config import Config
from clarity.models.work_item import WorkItem
from clarity.log import logger
from clarity.clients.interface import ClientEnum, IClient


class ConsoleClient(IClient):
    """
    A dummy client implementation that outputs work item actions to the console
    instead of pushing them to an external API (like Azure DevOps).
    """

    def __init__(self, config: Config):
        # Configuration is accepted but not strictly used,
        # as this client performs no external calls.
        logger.info("ConsoleClient initialized. All actions will be logged locally.")
        pass

    def name(self) -> ClientEnum:
        return ClientEnum.CONSOLE

    def create_work_items(
        self,
        workspace_slug: str,
        project_id: str,
        work_items: List[WorkItem],
        iteration: str,
    ) -> bool:
        """
        Processes a list of WorkItem objects, outputting their creation
        to the console.
        """
        if not work_items:
            logger.warning("No work items provided. Nothing to output.")
            return True

        logger.info(f"\n--- ConsoleClient: Creating {len(work_items)} Work Items ---")
        logger.info(f"Target Workspace: {workspace_slug}")
        logger.info(f"Target Project: {project_id}")
        logger.info(f"Target Iteration: {iteration}\n")

        success_count = 0

        for item in work_items:
            if self.create_work_item(workspace_slug, project_id, item, iteration):
                success_count += 1

        # Final Summary
        if success_count == len(work_items):
            logger.success(
                f"All {success_count} work items successfully *simulated* for creation."
            )
            return True
        else:
            # Note: In the ConsoleClient, this path is unlikely unless
            # create_work_item() is explicitly programmed to fail.
            logger.error(
                f"ConsoleClient completed simulation with {success_count} successes "
                f"out of {len(work_items)} total work items."
            )
            return False

    def create_work_item(
        self, workspace: str, project: str, work_item: WorkItem, iteration: str
    ) -> bool:
        """
        Simulates the creation of a single WorkItem by outputting its details.
        """

        # Simulated ID for demonstration
        simulated_id = hash(work_item.title) % 10000
        work_item_type = "Task"  # Assume default type for simulation

        # Output the item's details to the console
        logger.info(
            f"SIMULATING creation of {work_item_type} [{simulated_id}]: {work_item.title}"
        )
        logger.info(f"  > Project: {project}")
        logger.info(f"  > Iteration: {iteration}")
        logger.info(f"  > Description (excerpt): {work_item.description[:50]}...")

        # The to_azure_json_payload line is removed, as it's Azure-specific
        # patch_document: List[JsonPatchOperation] = work_item.to_azure_json_payload(iteration)

        # In a successful simulation, we always return True
        return True

    def list_work_items(self, workspace: str, project: str):
        """
        Simulates listing existing work items by outputting a sample list
        to the console, since we cannot query a real backend.
        """

        # Simulated data for demonstration
        mock_items = [
            {
                "id": 101,
                "type": "Bug",
                "title": "Simulated Issue: Navbar overflows on mobile",
                "status": "Active",
                "assigned": "User A",
            },
            {
                "id": 102,
                "type": "Feature",
                "title": "Simulated Feature: Add dark mode toggle",
                "status": "New",
                "assigned": "Unassigned",
            },
            {
                "id": 103,
                "type": "Task",
                "title": "Simulated Task: Update API documentation",
                "status": "Closed",
                "assigned": "User B",
            },
        ]

        logger.info(
            f"\n--- ConsoleClient: Simulated Work Item Listing for Project: {project} ---"
        )

        if not mock_items:
            logger.info("No mock work items found.")
            return

        for item in mock_items:
            logger.info(f"[{item['id']}] {item['type']}: {item['title']}")
            logger.info(f"  Status: {item['status']}")
            logger.info(f"  Assigned To: {item['assigned']}\n")
