import logging

import yaml

CONFIG_PATH = "app/logging/logging.yaml"


def configure_logging():
    with open(CONFIG_PATH) as f:
        logging_config = yaml.safe_load(f)
        logging.config.dictConfig(logging_config)
