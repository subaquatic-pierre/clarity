import logging
import sys
from typing import Any

# Define the custom log level once at the module level (standard practice)
logging.addLevelName(25, "SUCCESS")


class StandardLogger:
    """
    A wrapper class for Python's logging module to standardize output format
    and provide simple success/error methods.
    """

    def __init__(self, name: str = "ApplicationLogger", level=logging.DEBUG):
        """
        Initializes the logger.

        Args:
            name (str): The name of the logger (will appear in log entries).
            level: The minimum logging level to process (e.g., logging.DEBUG, logging.INFO).
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # Prevent log entries from propagating to the root logger handlers
        self.logger.propagate = False

        setattr(
            self.logger,
            "success",
            lambda msg, *args, **kwargs: self.logger.log(25, msg, *args, **kwargs),
        )

        # Check if a handler is already attached to prevent duplicate messages
        if not self.logger.handlers:
            # Create a StreamHandler to output to the console (stderr is standard for logs)
            handler = logging.StreamHandler(sys.stderr)
            handler.setLevel(level)

            # Define the standardized format
            formatter = logging.Formatter(
                "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
            handler.setFormatter(formatter)

            self.logger.addHandler(handler)

    def info(self, message: str):
        """Logs an informational message."""
        self.logger.info(message)

    def warning(self, message: str):
        """Logs a warning message."""
        self.logger.warning(message)

    def error(self, message: str):
        """Logs an error message."""
        self.logger.error(message)

    def success(self, message: str, *args: Any, **kwargs: Any):
        """Logs a custom success message."""
        self.logger.log(25, message, *args, **kwargs)


# Initialize the logger instance
# You can give it a specific name relevant to the module or component
logger = StandardLogger(name="WorkflowManagerLogger")
