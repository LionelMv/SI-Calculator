import os
from pathlib import Path
from logging.handlers import RotatingFileHandler

BASE_DIR = Path(__file__).resolve().parent.parent

LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,

    "formatters": {
        "verbose": {
            "format": "[{asctime}] {levelname} {name} ({module}:{lineno}) - {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname}: {message}",
            "style": "{",
        },
    },

    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_DIR / "calculator_app.log",
            "maxBytes": 5 * 1024 * 1024,  # 5 MB per log file
            "backupCount": 5,  # Keep 5 backups
            "formatter": "verbose",
            "encoding": "utf8",
        },
    },

    "loggers": {
        "": {  # Root logger (all logs)
            "handlers": ["console", "file"],
            "level": "INFO",
        },
        "calculator_api": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False,
        },
        "django": {  # Optional: reduce Django’s default verbosity
            "handlers": ["console", "file"],
            "level": "WARNING",
            "propagate": False,
        },
    },
}
