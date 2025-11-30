import requests
from typing import List

from clarity.config import Config
from clarity.work_item import WorkItem
from clarity.log import logger
from clarity.clients.interface import ClientEnum, IClient

import os
from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
from azure.devops.v7_1.work_item_tracking.models import Wiql, JsonPatchOperation


class AzureClient(IClient):
    def __init__(self, config: Config):
        self.host_url: str = config.AZURE_HOST_URL
        self.pat: str = config.AZURE_PAT

        self.headers: dict = {
            "Content-Type": "application/json",
        }

    def name(self) -> ClientEnum:
        return ClientEnum.AZURE

    def create_work_items(
        self,
        workspace_slug: str,
        project_id: str,
        work_items: List[WorkItem],
        iteration: str,
    ) -> bool:
        """
        Posts a list of WorkItem objects to the Azure DevOps API to create new issues.

        Returns: True if all items were created successfully, False otherwise.
        """

        if not work_items:
            logger.warning("No work items provided to create in Azure DevOps.")
            return True

        success_count = 0

        for item in work_items:
            if self.create_work_item(workspace_slug, project_id, item, iteration):
                success_count += 1

        # Final Summary
        if success_count == len(work_items):
            logger.success(
                f"All {success_count} work items successfully created in Azure DevOps."
            )
            return True
        else:
            logger.error(
                f"Completed Azure DevOps creation with {success_count} successes "
                f"out of {len(work_items)} total work items."
            )
            return False

    def create_work_item(
        self, workspace: str, project: str, work_item: WorkItem, iteration: str
    ) -> bool:
        wit_client = self._get_wit_client(workspace)

        # 1. Generate the JSON Patch payload from the WorkItem model
        iteration = f"{project}\\{iteration}"
        patch_document: List[JsonPatchOperation] = work_item.to_azure_json_payload(
            iteration
        )
        item_title = work_item.title

        work_item_type = "Task"

        try:
            # 2. Call the create_work_item API
            # This method internally handles the JSON Patch payload and the correct API URL.
            new_item = wit_client.create_work_item(
                document=patch_document, project=project, type=work_item_type
            )

            logger.success(
                f"Created Azure DevOps {work_item_type} [{new_item.id}]: {new_item.fields['System.Title']}"
            )
            return new_item

        except Exception as e:
            logger.error(
                f"Failed to create item '{item_title}' as {work_item_type}. Error: {e}"
            )
            return False

    def list_work_items(self, workspace: str, project: str):
        """
        Connects to Azure DevOps, runs a Wiql query, and lists the titles
        and states of the returned work items.
        """
        if not self.pat:
            logger.error("Personal Access Token (PAT) is not set.")
            return

        wit_client = self._get_wit_client(workspace)

        # 2. Define the Query (Wiql)
        # This query retrieves all active tasks assigned to the current user
        # You can customize this query extensively.
        #     AND [System.WorkItemType] = 'Any'
        #     AND [System.State] = 'Any'
        wiql_query = Wiql(
            query=f"""
            SELECT
                [System.Id],
                [System.Title],
                [System.State]
            FROM
                WorkItems
            WHERE
                [System.TeamProject] = '{project}'
            ORDER BY
                [System.Id] DESC
            """
        )

        try:
            # 3. Execute the Query
            logger.info(f"--- Querying work items in project: {project} ---")
            wiql_result = wit_client.query_by_wiql(wiql_query)

            if not wiql_result.work_items:
                logger.info("No work items found matching the query criteria.")
                return

            # Extract IDs from the query result
            work_item_ids = [item.id for item in wiql_result.work_items]

            # 4. Fetch Full Details
            logger.info(
                f"Found {len(work_item_ids)} work item IDs. Fetching details..."
            )

            # Specify the fields you want to retrieve
            fields = [
                "System.Id",
                "System.Title",
                "System.State",
                "System.WorkItemType",
                "System.AssignedTo",
            ]

            # API call to get the work items by their IDs
            work_items = wit_client.get_work_items(work_item_ids, fields=fields)

            # 5. Print Results
            logger.info("\n--- Work Item Listing ---")
            for item in work_items:
                logger.info(
                    f"[{item.fields.get('System.Id', 'N/A')}] {item.fields.get('System.WorkItemType', 'N/A')}: {item.fields.get('System.Title', 'N/A')}"
                )
                logger.info(f"  Status: {item.fields.get('System.State', 'N/A')}")
                assigned_to = item.fields.get("System.AssignedTo", {}).get(
                    "displayName", "Unassigned"
                )
                logger.info(f"  Assigned To: {assigned_to}\n")

        except Exception as e:
            logger.error(f"An error occurred during Azure DevOps interaction: {e}")
            # In a real application, you might use logging.error(e) here.

    def _get_wit_client(self, workspace):
        credentials = BasicAuthentication("", self.pat)

        organization_url = f"{self.host_url}/{workspace}"
        connection = Connection(base_url=organization_url, creds=credentials)
        return connection.clients.get_work_item_tracking_client()
