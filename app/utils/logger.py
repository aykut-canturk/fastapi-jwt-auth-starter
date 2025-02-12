import os
import logging
from contextvars import ContextVar
from app.config import settings

correlation_id_var = ContextVar("correlation_id", default="unknown")


def set_correlation_id(correlation_id):
    correlation_id_var.set(correlation_id)


def get_correlation_id():
    return correlation_id_var.get()


class CorrelationIDFilter(logging.Filter):
    def filter(self, record):
        record.correlation_id = correlation_id_var.get()
        return True


def get_logger(name):
    application_logger = logging.getLogger(name)
    application_logger.setLevel(settings.log_level)

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - [%(correlation_id)s] - %(message)s"
    )

    correlation_id_filter = CorrelationIDFilter()
    application_logger.addFilter(correlation_id_filter)

    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    application_logger.addHandler(ch)

    # Create logs directory if it does not exist
    if not os.path.exists("./logs"):
        os.makedirs("./logs")
    fh = logging.FileHandler("./logs/application.log")
    fh.setFormatter(formatter)
    application_logger.addHandler(fh)

    return application_logger


logger = get_logger(__name__)


def log_info(message):
    logger.info(message)


def log_debug(message):
    logger.debug(message)


def log_error(message):
    logger.error(message)


def log_warning(message):
    logger.warning(message)


def log_critical(message):
    logger.critical(message)


def log_exception(message):
    logger.exception(message)
