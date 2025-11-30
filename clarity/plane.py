import requests
from typing import List, Any
import os  # Import os for robust URL joining

# Assuming these are defined and imported from your project
from clarity.config import Config
from clarity.work_item import WorkItem
from clarity.log import logger


class PlaneClient:
    def __init__(self, config: Config):
        # Configuration setup
        # Ensure self.host_url is clean (e.g., just 'localhost:80' or 'plane.io')
        self.host_url: str = config.PLANE_HOST_URL.rstrip("/")
        self.api_token: str = config.PLANE_API_TOKEN

        # Standard headers for Plane API requests
        self.headers: dict = {
            "x-api-key": f"{self.api_token}",
            "Content-Type": "application/json",
        }

    def create_work_items(
        self, workspace_slug: str, project_id: str, work_items: List[WorkItem]
    ) -> bool:
        """
        Posts a list of WorkItem objects to the Plane API to create new issues.

        Returns: True if all items were created successfully, False otherwise.
        """

        if not work_items:
            logger.warning("No work items provided to create in Plane.")
            return True

        success_count = 0

        # Iterate through work items and track successes
        for item in work_items:
            if self.create_work_item(workspace_slug, project_id, item):
                success_count += 1

        # Final Summary
        if success_count == len(work_items):
            logger.success(
                f"All {success_count} work items successfully created in Plane."
            )
            return True
        else:
            logger.error(
                f"Completed Plane creation with {success_count} successes "
                f"out of {len(work_items)} total work items."
            )
            return False

    def create_work_item(
        self, workspace_slug: str, project_id: str, work_item: WorkItem
    ) -> bool:

        payload = work_item.to_plane_json_payload()
        item_name = payload.get(
            "name", "Unknown Work Item"
        )  # Safer way to get name for logs

        # Assumes host_url doesn't start with http:// or https://, or handles it safely
        url = f"{self.host_url}/api/v1/workspaces/{workspace_slug}/projects/{project_id}/work-items/"

        headers = self.headers

        try:
            response = requests.post(url, headers=headers, json=payload)

            # The API returns the key/ID in 'name' or 'issue_key' depending on the version
            # Use 'name' for the log, or fall back to the provided title if response fails
            response_data = response.json()
            work_item_name = response_data.get("name", item_name)

            if response.status_code == 201:
                logger.success(f"Created Plane work item: {work_item_name}")
                return True
            else:
                # Log API-specific error details
                logger.error(
                    f"Failed to create item '{item_name}'. "
                    f"Status: {response.status_code}. "
                    f"Response: {response.text[:200]}"
                )
                return False

        except requests.exceptions.RequestException as e:
            # Log network/connection errors
            logger.error(f"Network error while posting issue '{item_name}': {e}")
            return False

        except Exception as e:
            # Log any unexpected errors (e.g., in payload generation)
            logger.error(f"Unexpected error for issue '{item_name}': {e}")
            return False
