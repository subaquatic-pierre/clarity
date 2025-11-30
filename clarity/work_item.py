from typing import Literal, List, Optional
from pydantic import BaseModel, Field
from azure.devops.v7_1.work_item_tracking.models import JsonPatchOperation


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

    def to_azure_json_payload(self, iteration) -> List[JsonPatchOperation]:
        """
        Generates the required JSON Patch document for Azure DevOps API creation.

        Azure DevOps requires a list of operations describing changes to fields
        using 'add', 'replace', or 'remove' operations.
        """
        patch_document = [
            # 1. Add Title
            JsonPatchOperation(op="add", path="/fields/System.Title", value=self.title),
            # 2. Add Description
            JsonPatchOperation(
                op="add", path="/fields/System.Description", value=self.description
            ),
        ]

        patch_document.append(
            JsonPatchOperation(
                op="add", path="/fields/System.IterationPath", value=iteration
            )
        )

        # 3. Optionally add Assignee
        # if self.assigned_to_email:
        #     # Assignee is set via the email address in the 'System.AssignedTo' path
        #     patch_document.append(
        #         JsonPatchOperation(
        #             op="add",
        #             path="/fields/System.AssignedTo",
        #             value=self.assigned_to_email,
        #         )
        #     )

        return patch_document

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

    @staticmethod
    def create_dummy_item() -> "WorkItem":
        """
        Creates a simple, default WorkItem instance for testing and demonstration.
        """
        return WorkItem(
            title="Feat: Implement OIDC Authentication Flow",
            description=(
                "The team decided in the Q3 planning meeting that all internal tools "
                "must use OpenID Connect (OIDC) for centralized identity management. "
                "This task covers integrating the backend service with the Okta IDP."
            ),
            acceptance_criteria=[
                "User is redirected to Okta login page when accessing the tool.",
                "Successful authentication redirects the user back with a valid token.",
                "User details (email, name) are correctly mapped and stored in the session.",
                "A non-authenticated user cannot access any API endpoints.",
            ],
            task_breakdown=[
                "Update dependencies for OIDC client library.",
                "Configure Okta client ID and secret in environment variables.",
                "Implement `/login` and `/callback` endpoints.",
                "Add middleware to validate tokens on all protected routes.",
            ],
            task_type="Task",
            component="Backend: Auth",
        )


class WorkItemList(BaseModel):
    """The root structure required to hold the array of work packages."""

    work_items: List[WorkItem]
