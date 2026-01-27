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


class GithubClient(IClient):
    def __init__(self, config: Config):
        self.host_url: str = config.GITHUB_HOST_URL
        self.pat: str = config.GITHUB_PAT

        self.headers: dict = {
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
            "X-GitHub-Api-Version": "2022-11-28",
            "Authorization": f"Bearer {self.pat}",
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
        Posts a list of WorkItem objects to the Github API to create new issues.

        Returns: True if all items were created successfully, False otherwise.
        """

        if not work_items:
            logger.warning("No work items provided to create in Github API.")
            return True

        success_count = 0

        for item in work_items:
            if self.create_work_item(workspace_slug, project_id, item, iteration):
                success_count += 1

        # Final Summary
        if success_count == len(work_items):
            logger.success(
                f"All {success_count} work items successfully created in Github API."
            )
            return True
        else:
            logger.error(
                f"Completed Github API creation with {success_count} successes "
                f"out of {len(work_items)} total work items."
            )
            return False

    def create_work_item(
        self, workspace: str, project: str, work_item: WorkItem, iteration: str
    ) -> bool:
        payload = work_item.to_plane_json_payload()
        item_name = payload.get(
            "name", "Unknown Work Item"
        )  # Safer way to get name for logs

        # Assumes host_url doesn't start with http:// or https://, or handles it safely
        url = f"{self.host_url}/{workspace}/projectsV2/{project}/items"

        headers = self.headers

        # 1. Generate the JSON Patch payload from the WorkItem model
        payload: dict = work_item.to_github_payload()

        try:
            response = requests.post(url, headers=headers, json=payload)
            # This method internally handles the JSON Patch payload and the correct API URL.

            logger.success(f"Created Github issue")
            return True

        except Exception as e:
            logger.error(f"Failed to create item ")
            return False

    def list_work_items(self, workspace: str, project: str):
        """
        Connects to Github and returns states of the returned work items.
        """

        url = f"{self.host_url}/{workspace}/projectsV2/{project}/items"

        headers = self.headers

        try:
            response = requests.get(url, headers=headers)
            logger.info("\n--- Work Item Listings ---")
            work_items = response.json()
            for item in work_items:
                logger.info(f"Work Item: {item}\n")
        except Exception as e:
            logger.error("Personal Access Token (PAT) is not set.")
            logger.error(f"An error occurred during Github API interaction: {e}")
