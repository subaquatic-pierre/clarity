from enum import Enum
from dataclasses import dataclass
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime
from typing import Optional


class ProjectFieldType(str, Enum):
    TITLE = "title"
    ASSIGNEES = "assignees"
    STATUS = "single_select"
    LABELS = "labels"
    LINKED_PULL_REQUESTS = "linked_pull_requests"
    MILESTONE = "milestone"
    REPOSITORY = "repository"
    ISSUE_TYPE = "issue_type"
    REVIEWERS = "reviewers"
    PARENT_ISSUE = "parent_issue"
    SUB_ISSUES_PROGRESS = "sub_issues_progress"
    NUMBER = "number"
    DATE = "date"


@dataclass
class RichText:
    raw: str
    html: str

    def __str__(self) -> str:
        return self.raw


@dataclass
class ProjectFieldOption:
    id: str
    name: RichText
    description: Optional[RichText]
    color: str

    def __str__(self) -> str:
        return f"{self.name.raw} ({self.id})"


@dataclass
class ProjectField:
    id: int
    node_id: str
    name: str
    data_type: ProjectFieldType
    project_url: str
    created_at: datetime
    updated_at: datetime

    # Only present for single_select
    options: List[ProjectFieldOption] = field(default_factory=list)

    # -------- convenience helpers --------

    def is_single_select(self) -> bool:
        return self.data_type == ProjectFieldType.STATUS

    def option_by_name(self, raw_name: str) -> Optional[ProjectFieldOption]:
        for opt in self.options:
            if opt.name.raw == raw_name:
                return opt
        return None

    def __str__(self) -> str:
        base = f"ProjectField === id: {self.id} - name: {self.name}\nOptions: ==="

        if self.options:
            opts = ", ".join(f"(id: {o.id}, name: {o.name.raw})" for o in self.options)
            return f"{base} [{opts}]"

        return base

    @staticmethod
    def parse_project_field(payload: dict) -> "ProjectField":
        options = []
        for opt in payload.get("options", []):
            options.append(
                ProjectFieldOption(
                    id=opt["id"],
                    name=RichText(**opt["name"]),
                    description=(
                        RichText(**opt["description"])
                        if opt.get("description")
                        else None
                    ),
                    color=opt["color"],
                )
            )

        return ProjectField(
            id=payload["id"],
            node_id=payload["node_id"],
            name=payload["name"],
            data_type=ProjectFieldType(payload["data_type"]),
            project_url=payload["project_url"],
            created_at=datetime.fromisoformat(
                payload["created_at"].replace("Z", "+00:00")
            ),
            updated_at=datetime.fromisoformat(
                payload["updated_at"].replace("Z", "+00:00")
            ),
            options=options,
        )
