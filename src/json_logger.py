#!/usr/bin/env python
# coding=utf-8
import logging
import json
import time
import os


class JSONFormatter(logging.Formatter):
    """ JSON formatter """
    def format(self, record):
        """ Format event info to json."""
        obj = {}
        obj["message"] = record.msg
        obj["level"] = record.levelname
        obj["time"] = time.ctime(record.created)
        obj["epoch_time"] = record.created
        if hasattr(record, "custom_logging"):
            for key, value in record.custom_logging.items():
                obj[key] = value
        return json.dumps(obj)


def setup_logger():
    """ Create logging object."""
    logger = logging.getLogger()

    handler = logging.StreamHandler()
    formatter = JSONFormatter()
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    if "DEBUG" in os.environ and os.environ["DEBUG"] == "true":
        logger.setLevel(logging.DEBUG)  # pragma: no cover
    else:
        logger.setLevel(logging.INFO)
        logging.getLogger("boto3").setLevel(logging.WARNING)
        logging.getLogger("botocore").setLevel(logging.WARNING)

    return logger
