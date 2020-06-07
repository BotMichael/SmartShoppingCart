import os
import logging
from logging import handlers


_log_file_edge_dir = "src/edge/rpi2/"
_log_file_error = "log/Error.log"
_log_file_edge = "log/Edge_?.log"
_log_file_model = "log/Model_?.log"

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

class EdgeLogger:
    def __init__(self, device_id: str):
        self.logger, self.sh, self.th = _get_logger(_log_file_edge.replace("?", device_id))
        self.logger.removeHandler(self.sh)
        self.error_logger, self.error_sh, self.error_th = _get_logger( _log_file_error)
        self.error_logger.removeHandler(self.error_sh)


class ModelLogger:
    def __init__(self, model_id: str):
        self.logger, self.sh, self.th = _get_logger(_log_file_model.replace("?", model_id))
        self.error_logger, self.error_sh, self.error_th = _get_logger( _log_file_error)
        self.error_logger.removeHandler(self.error_sh)
