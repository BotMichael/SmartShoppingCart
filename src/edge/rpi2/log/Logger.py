import os
import logging
from logging import handlers

_log_dir = ""
# if(not os.path.exists(_log_dir)):
#     os.mkdir(_log_dir)

_log_file = "log/"
_log_file_error = _log_file + "Error.log"
_log_file_cloud = _log_file + "Cloud.log"
_log_file_fog = _log_file + "Fog.log"
_log_file_edge = _log_file + "Edge_?.log"
_log_file_model = _log_file+ "Model_?.log"

_level = logging.INFO
_when = 'D'
_backupCount = 5
_fmt = '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'


def _get_logger(filename: str):
    logger = logging.getLogger(filename)
    format_str = logging.Formatter(_fmt)
    logger.setLevel(_level)

    # Print to the console
    sh = logging.StreamHandler() 
    sh.setFormatter(format_str)
    logger.addHandler(sh)

    # Print to the file
    th = handlers.TimedRotatingFileHandler(filename = filename, when = _when, backupCount = _backupCount, encoding = 'utf-8') 
    th.setFormatter(format_str)
    logger.addHandler(th)

    return (logger, sh, th)


class ErrorLogger:
    def __init__(self):
        self.logger, self.sh, self.th = _get_logger(_log_file_error)
        self.logger.removeHandler(self.sh)


class CloudLogger:
    def __init__(self):
        self.logger, self.sh, self.th = _get_logger(_log_file_cloud)


class FogLogger:
    def __init__(self):
        self.logger, self.sh, self.th = _get_logger(_log_file_fog)


class EdgeLogger:
    def __init__(self, device_id: str):
        self.logger, self.sh, self.th = _get_logger(_log_file_edge.replace("?", device_id))
        self.logger.removeHandler(self.sh)


class ModelLogger:
    def __init__(self, model_id: str):
        self.logger, self.sh, self.th = _get_logger(_log_file_model.replace("?", model_id))
