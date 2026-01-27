import requests
from typing import List, Optional

from clarity.config import Config
from clarity.models.field import ProjectField
from clarity.models.work_item import WorkItem
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
        self.repo: str = config.GITHUB_REPO
        self.fields = []

        self.headers: dict = {
            "Accept": "application/vnd.github+json",
            # "Content-Type": "application/json",
            "X-GitHub-Api-Version": "2022-11-28",
            "Authorization": f"Bearer {self.pat}",
        }

    def name(self) -> ClientEnum:
        return ClientEnum.GITHUB

    def get_and_set_project_fields(
        self,
        workspace_slug: str,
        project_id: str,
    ):
        fields = self.list_fields(workspace_slug, project_id)
        self.fields = fields

    def get_field(self, field_name: str) -> Optional[ProjectField]:
        field = next(f for f in self.fields if f.name == field_name)
        return field

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

        # set internal project item fields
        self.get_and_set_project_fields(workspace_slug, project_id)

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

        try:
            issue_id = self.create_issue(workspace, work_item)

        except Exception as e:
            logger.error(f"Failed to create issue item {e}")
            return False

        try:
            new_item_id = self.create_project_item(workspace, project, issue_id)

        except Exception as e:
            logger.error(f"Failed to create project item {e}")
            return False

        try:
            # pass
            self.update_project_item(
                workspace, project, new_item_id, work_item, iteration
            )

        except Exception as e:
            logger.error(f"Failed to update project item {e}")
            return False

        return True

    def create_issue(self, workspace: str, work_item: WorkItem) -> str:
        issue_url = f"{self.host_url}/repos/{workspace}/{self.repo}/issues"

        headers = self.headers

        payload: dict = work_item.to_github_issue()

        # create issue
        res = requests.post(issue_url, headers=headers, json=payload)
        res.raise_for_status()
        issue = res.json()
        issue_id = issue["id"]
        logger.success(f"Created Github issue, {issue_id}")
        return issue_id

    def create_project_item(self, workspace: str, project: str, issue_id: str) -> str:
        # create project item
        headers = self.headers
        create_item_url = f"{self.host_url}/orgs/{workspace}/projectsV2/{project}/items"
        create_item_payload: dict = {
            "type": "Issue",
            "id": issue_id,
        }
        res = requests.post(create_item_url, headers=headers, json=create_item_payload)
        res.raise_for_status()
        new_item = res.json()
        new_item_id = new_item["id"]
        logger.success(
            f"Created Github project item with id: {new_item_id}, from issue id: {issue_id}"
        )

        return new_item_id

    def update_project_item(
        self,
        workspace: str,
        project: str,
        item_id: str,
        work_item: WorkItem,
        iteration: str = "Backlog",
    ):
        headers = self.headers

        # update project item
        update_item_url = (
            f"{self.host_url}/orgs/{workspace}/projectsV2/{project}/items/{item_id}"
        )
        fields = self.build_update_fields(work_item, iteration)

        update_payload: dict = {"fields": fields}

        print(f"update_payload: {update_payload}")
        res = requests.patch(update_item_url, headers=headers, json=update_payload)
        res.raise_for_status()
        project_item = res.json()
        item_id = project_item["id"]

        logger.success(f"Updated Github project item, {item_id}")

    def build_update_fields(self, work_item: WorkItem, iteration: str) -> List[dict]:
        fields = []

        # type_field = self.get_field("Type")
        # work_item_type = work_item.task_type
        # if type_field and work_item_type:
        #     fields.append(
        #         {"id": type_field.id, "value": work_item_type},  # Task type field
        #     )

        status_field = self.get_field("Status")
        if status_field:
            status_field_backlog_option = status_field.option_by_name(iteration)
            if status_field_backlog_option:
                fields.append(
                    {
                        "id": status_field.id,
                        "value": status_field_backlog_option.id,
                    },  # Status field
                )

        sprint_field = self.get_field("Sprint")
        if sprint_field:
            sprint_field_option = sprint_field.option_by_name(iteration)
            if sprint_field_option:
                fields.append(
                    {
                        "id": sprint_field.id,
                        "value": sprint_field_option.id,
                    },  # Sprint field
                )

        return fields

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

    def list_fields(self, workspace: str, project: str) -> List[ProjectField]:
        """
        Connects to Github and returns states of the returned work items.
        """

        url = f"{self.host_url}/orgs/{workspace}/projectsV2/{project}/fields"

        headers = self.headers

        try:
            response = requests.get(url, headers=headers)
            project_item_fields = response.json()
            fields = [ProjectField.parse_project_field(f) for f in project_item_fields]

            return fields
        except Exception as e:
            logger.error(f"An error occurred during Github API interaction: {e}")
            return []
