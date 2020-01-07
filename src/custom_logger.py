#!/usr/bin/env python
# coding=utf-8
import logging
import json
import time
import os


class CustomAdapter(logging.LoggerAdapter):
    """ Add general items (function name) to the log message """
    def process(self, msg, kwargs):
        function = kwargs.pop('function', self.extra['function'])
        if "extra" in kwargs:
            if "custom_logging" in kwargs["extra"]:
                kwargs["extra"]["custom_logging"]["function"] = function
        return msg, kwargs


class JSONFormatter(logging.Formatter):
    """ JSON formatter """
    def format(self, record):
        """ Format event info to json."""
        string_formatted_time = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(record.created))
        obj = {}
        obj["message"] = record.msg
        obj["level"] = record.levelname
        obj["time"] = f"{string_formatted_time}.{record.msecs:3.0f}Z"
        obj["epoch_time"] = record.created
        if hasattr(record, "custom_logging"):
            for key, value in record.custom_logging.items():
                obj[key] = value
        return json.dumps(obj)


def setup_logger(function):
    """ Create logging object."""
    logger = logging.getLogger(__name__)
    logger.propagate = False  # remove default logger

    handler = logging.StreamHandler()
    formatter = JSONFormatter()
    handler.setFormatter(formatter)

    adapter = CustomAdapter(logger, function)
    logger.addHandler(handler)

    if "DEBUG" in os.environ and os.environ["DEBUG"] == "true":
        logger.setLevel(logging.DEBUG)  # pragma: no cover
    else:
        logger.setLevel(logging.INFO)
        logging.getLogger("boto3").setLevel(logging.WARNING)
        logging.getLogger("botocore").setLevel(logging.WARNING)

    return logger, adapter
