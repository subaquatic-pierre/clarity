from abc import ABC, abstractmethod
from enum import Enum
from typing import List

from clarity.work_item import WorkItem


class ClientEnum(Enum):
    AZURE = "Azure"
    PLANE = "Plane"


class IClient(ABC):
    @abstractmethod
    def name(self) -> ClientEnum:
        pass

    @abstractmethod
    def create_work_items(
        self, workspace: str, project: str, work_items: List[WorkItem], iteration: str
    ) -> bool:
        """
        Posts a list of WorkItem objects to the Project Management Board API to create new issues.

        Returns: True if all items were created successfully, False otherwise.
        """
        pass
