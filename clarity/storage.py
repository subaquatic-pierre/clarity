from abc import ABC, abstractmethod
import json
import os
import time
from typing import List

from clarity.config import Config
from clarity.work_item import WorkItem
from clarity.log import logger


class Storage:
    # Class attributes for type hinting (no need for abstract methods here)
    base_path: str
    transcript_dir: str
    work_package_dir: str

    def __init__(self, config: Config):
        # NOTE: Using same name for local variables and attributes is fine,
        # but the type hints below are unnecessary for local vars.
        base_path: str = config.BASE_PATH
        transcript_dir: str = config.TRANSCRIPT_PATH
        work_package_dir: str = config.WORK_PACKAGE_PATH

        self.base_path = base_path
        self.transcript_dir = transcript_dir
        self.work_package_dir = work_package_dir

    def read_transcript(self, filename: str) -> str:
        """
        Loads the entire transcript file from the configured directory.
        Returns the file content as a string, or an empty string on failure.
        """

        inpath = os.path.join(self.base_path, self.transcript_dir, filename)
        content = ""

        try:
            with open(inpath, "r", encoding="utf-8") as f:
                content = f.read()

            # 2. Use logger.success for successful read
            logger.success(f"Successfully read transcript file: {inpath}")

        except FileNotFoundError:
            # 3. Use logger.error for FileNotFoundError
            logger.error(f"Transcript file not found at: {inpath}")

        except Exception as e:
            # 4. Use logger.error for other exceptions
            logger.error(
                f"Failed to read transcript file at {inpath}. Exception details: {e}"
            )

        return content

    def save_work_items(self, work_items: List[WorkItem]):
        timestamp = int(time.time())
        filename = f"{timestamp}_work_items.json"

        # 5. Use self.work_package_dir for the output path
        outpath = os.path.join(self.base_path, self.work_package_dir, filename)

        try:
            # Ensure the directory exists before attempting to open the file
            os.makedirs(os.path.dirname(outpath), exist_ok=True)

            with open(outpath, "w", encoding="utf-8") as f:
                json.dump([wp.model_dump() for wp in work_items], f, indent=2)

            # 6. Use logger.success for successful save
            logger.success(
                f"Successfully saved {len(work_items)} Work Packages to: {outpath}"
            )

        except Exception as e:
            # 7. Use logger.error for save failure
            logger.error(
                f"Failed to save work packages to {outpath}. Exception details: {e}"
            )
