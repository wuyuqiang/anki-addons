import os
import sys
import logging
import logging.handlers

ADDON = os.path.dirname(os.path.abspath(__file__)).decode(sys.getfilesystemencoding())

LOG_DIR = os.path.join(ADDON, 'log')
if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)

LOG = os.path.join(LOG_DIR, 'addon.log')

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


handler = logging.handlers.RotatingFileHandler(LOG,maxBytes=1024 * 1024 * 16, backupCount=10)
handler.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s")
handler.setFormatter(formatter)


def getLogger(loggerName):
    logger = logging.getLogger(loggerName)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    return logger
