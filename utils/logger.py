"""Logger setup for application debugging and audit logs."""

import logging
import os

LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "logs")
os.makedirs(LOG_DIR, exist_ok=True)


def get_logger(name: str) -> logging.Logger:
    """
    Returns a configured logger for the given module name.
    Logs to both console and logs/app.log file.
    """
    logger = logging.getLogger(name)

    if logger.handlers:
        # Prevent adding duplicate handlers on repeated imports
        return logger

    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        fmt="[%(asctime)s] %(levelname)s in %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    # File handler
    file_handler = logging.FileHandler(os.path.join(LOG_DIR, "app.log"))
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
