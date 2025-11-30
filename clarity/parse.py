import json
from typing import List

from clarity.log import logger
from clarity.work_item import WorkItem, WorkItemList


class AgentParser:
    @staticmethod
    def parse_work_package_json_str(content: str) -> List[WorkItem]:
        """
        Parses the raw JSON, validates it using Pydantic, and handles errors
        with a single, standardized log message.
        """
        try:
            # Validate and parse the raw JSON string against the Pydantic model
            validated_data = WorkItemList.model_validate_json(content)

            # Return the list of work_items from the model
            return validated_data.work_items

        except (json.JSONDecodeError, ValueError, AttributeError) as e:

            # 1. Prepare all necessary information for a single log message
            error_details = str(e).replace("\n", " ")  # Flatten error details
            raw_output_snippet = content[:1000].replace(
                "\n", "\\n"
            )  # Add raw output snippet

            # 2. Use a single logger call to report the failure
            logger.error(
                f"JSON Parsing Failed | Error Type: {e.__class__.__name__} | "
                f"Details: {error_details} | "
                f'Raw Output Snippet (first 1000 chars): "{raw_output_snippet}..."'
            )

            return []
