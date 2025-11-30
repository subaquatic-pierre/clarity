from abc import ABC, abstractmethod
from typing import List

from clarity.work_item import WorkItem


class IClient(ABC):
    @abstractmethod
    def create_work_items(
        self, workspace_slug: str, project_id: str, work_items: List[WorkItem]
    ) -> bool:
        """
        Posts a list of WorkItem objects to the Plane API to create new issues.

        Returns: True if all items were created successfully, False otherwise.
        """
        pass
