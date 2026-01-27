import json
import os
import time
from typing import List

import re
import os

from clarity.config import Config
from clarity.models.work_item import WorkItem
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
        self.ensure_data_directories_exist()

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

        if inpath.endswith(".vtt"):
            content = self.clean_vtt_string(content)
            logger.success(f"Cleaned VTT content: {inpath}")

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

    def ensure_data_directories_exist(self):
        """Checks for and creates necessary data directories."""

        # 1. Input Transcripts Directory
        if not os.path.exists(self.transcript_dir):
            logger.info(f"Creating transcript directory: {self.transcript_dir}")
            os.makedirs(self.transcript_dir, exist_ok=True)

        # 2. Output Work Items Directory
        if not os.path.exists(self.work_package_dir):
            logger.info(f"Creating work items directory: {self.work_package_dir}")
            os.makedirs(self.work_package_dir, exist_ok=True)

        logger.info("Data directories are ready.")

    def clean_vtt_string(self, vtt_content: str) -> str:
        """
        Cleans a VTT transcript string by removing timestamps, cue numbers,
        and the WEBVTT header, leaving only the spoken text.
        """
        # 1. Remove the WEBVTT header
        vtt_content = re.sub(r"WEBVTT\n?", "", vtt_content)

        # 2. Remove cue identifiers (optional, like '1', '2', '3', etc.)
        # This assumes identifiers are simple numbers at the start of a line
        vtt_content = re.sub(r"^\d+\n", "", vtt_content, flags=re.MULTILINE)

        # 3. Remove timestamp lines (e.g., 00:00:01.630 --> 00:00:07.690)
        # This is the most crucial step
        vtt_content = re.sub(
            r"^\d{2}:\d{2}:\d{2}\.\d{3} --> .+\n", "", vtt_content, flags=re.MULTILINE
        )

        # 4. Remove extra blank lines created by the removals
        vtt_content = re.sub(r"\n{2,}", "\n", vtt_content)

        # 5. Remove any leading/trailing whitespace
        return vtt_content.strip()
