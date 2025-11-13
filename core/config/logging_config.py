from pathlib import Path
from logging.handlers import RotatingFileHandler

BASE_DIR = Path(__file__).resolve().parent.parent

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
    },

    "loggers": {
        "": {  # Root logger (all logs)
            "handlers": ["console"],
            "level": "INFO",
        },
        "calculator_api": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "django": {  # Optional: reduce Django’s default verbosity
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
    },
}