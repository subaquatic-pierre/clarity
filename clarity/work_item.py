from typing import Literal, List, Optional
from pydantic import BaseModel, Field


class WorkItem(BaseModel):
    title: str = Field(
        ...,
        max_length=100,
        description="Use imperative mood, e.g., 'Fix: Enable dark mode toggle state' or 'Feat: Add API endpoint for user list'.",
    )
    description: str = Field(
        ...,
        description="A detailed explanation answering the WHAT (the problem/goal) and the WHY (the justification/business value), avoiding HOW (implementation details).",
    )
    acceptance_criteria: List[str] = Field(
        ...,
        description="A numbered list of observable, verifiable conditions that must be met for the task to be considered complete (e.g., '1. The user must see a success message. 2. The database must record the new user ID.').",
    )
    task_breakdown: List[str] = Field(
        ...,
        description="A numbered list of technical sub-tasks or implementation steps required to complete the main task (e.g., '1. Create new database migration. 2. Update service layer to handle new column.').",
    )
    task_type: Literal["Task", "Fix", "Chore", "Docs"] = Field(
        "Task",
        description="Conventional Commit type: 'Feat' (New Feature), 'Fix' (Bug Fix), 'Chore' (Maintenance/Build), 'Docs' (Documentation update). Default: 'Task'.",
    )
    component: Optional[str] = Field(
        None,
        description="The specific application area or module affected (e.g., 'API', 'Frontend: Checkout', 'Database'). Default: null.",
    )

    def to_plane_json_payload(self) -> dict:
        """
        Converts the WorkItem model into a dictionary formatted for the Plane API issue creation endpoint.

        Expected payload:
        {
            "name": "<string>",
            "description_html": "<string>",
            "state": "<string>",
            "assignees": ["<string>"],
            "priority": "<string>",
            "labels": ["<string>"],
            "parent": "<string>",
            "estimate_point": "<string>",
            "type": "<string>",
            "module": "<string>",
            "start_date": "<string>",
            "target_date": "<string>",
        }
        """

        html_desc = self.build_html_desc()

        plane_type = {
            "Task": "Task",
            "Fix": "Bug",
            "Chore": "Chore",
            "Docs": "Documentation",
        }.get(
            self.task_type, "Task"
        )  # Default to 'Task' if mapping fails

        payload = {
            "name": self.title,
            "description_html": html_desc,
            # CRITICAL: These placeholders must be replaced with actual Project-specific IDs (UUIDs)
            # "state": "Backlog",  # State name (e.g., 'Backlog', 'To Do') or UUID
            # "assignees": [],  # List of User IDs (UUIDs)
            # "priority": "Low",  # Priority name (e.g., 'Low', 'Medium', 'High') or UUID
            # "labels": (
            #     [self.component] if self.component else []
            # ),  # Uses component as a label
            # "parent": None,  # Used for sub-tasks; typically null/None for a top-level task
            # "estimate_point": None,  # Points estimate (number or string representation)
            # "type": plane_type,
            # "module": None,  # Module ID (UUID)
            # "start_date": None,  # YYYY-MM-DD
            # "target_date": None,  # YYYY-MM-DD
        }

        # Clean up lists that might contain None/null values
        # if not payload["assignees"]:
        #     del payload["assignees"]
        # if not payload["labels"]:
        #     del payload["labels"]

        return payload

    def to_azure_json_payload(self) -> dict:
        """
        Converts the WorkItem model into a dictionary formatted for the Plane API issue creation endpoint.

        Expected payload:
        {
            "name": "<string>",
            "description_html": "<string>",
            "state": "<string>",
            "assignees": ["<string>"],
            "priority": "<string>",
            "labels": ["<string>"],
            "parent": "<string>",
            "estimate_point": "<string>",
            "type": "<string>",
            "module": "<string>",
            "start_date": "<string>",
            "target_date": "<string>",
        }
        """

        return {}

    def build_html_desc(self) -> str:
        # --- 1. Construct the Rich HTML Description ---

        # Start with the main description
        html_desc = f"<h3>Description / Context</h3>\n<p>{self.description}</p>\n"

        # Add Acceptance Criteria as an unordered HTML list
        html_desc += "<h3>Acceptance Criteria</h3>\n<ul>\n"
        html_desc += "".join(f"<li>{item}</li>\n" for item in self.acceptance_criteria)
        html_desc += "</ul>\n"

        # Add Technical Task Breakdown as an ordered HTML list
        html_desc += "<h3>Technical Breakdown</h3>\n<ol>\n"
        html_desc += "".join(f"<li>{item}</li>\n" for item in self.task_breakdown)
        html_desc += "</ol>\n"

        return html_desc


class WorkItemList(BaseModel):
    """The root structure required to hold the array of work packages."""

    work_items: List[WorkItem]
