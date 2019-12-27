" Zoolite demo app"
# import logging
import json_logger

# Setup logging
LOGGER = json_logger.setup_logger()


def handler(event, _):
    """ main handler """
    try:
        if event["simulation"] == "error":
            LOGGER.error("Function failed")
        if event["simulation"] == "info":
            LOGGER.info("Function started")
    except KeyError as err:
        LOGGER.error("Missing 'simulation' key in event")
        raise Exception("Missing 'simulation' key")
