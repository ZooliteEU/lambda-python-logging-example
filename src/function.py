" Zoolite demo app"
# import logging
# import json_logger
import os
import custom_logger

# Setup logging
FUNCTION_NAME = {"function": os.getenv("AWS_LAMBDA_FUNCTION_NAME")}
LOGGER, ADAPTER = custom_logger.setup_logger(FUNCTION_NAME)
# LOGGER = json_logger.setup_logger()
# LOGGER = logging.getLogger(__name__)
# LOGGER.setLevel(logging.INFO)

def handler(event, _):
    """ main handler """
    extra_logging = {"custom_logging": {"something": "we want to log"}}
    try:
        if event["simulation"] == "error":
            ADAPTER.error("Function failed", extra=extra_logging)
        if event["simulation"] == "info":
            LOGGER.info("Function started")
    except KeyError as err:
        LOGGER.error("Missing 'simulation' key in event")
        raise Exception("Missing 'simulation' key")
