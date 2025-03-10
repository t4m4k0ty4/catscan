import logging
from pathlib import Path

import yaml

CONFIG_PATH = Path("app/logging/")

if not CONFIG_PATH.exists():
    CONFIG_PATH.mkdir(parents=True)


def configure_logging():
    with open(CONFIG_PATH / "logging.yaml") as f:
        logging_config = yaml.safe_load(f)
        logging.config.dictConfig(logging_config)
