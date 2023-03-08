import sys
import os
import logging.config
from src.api import app

ROOT_DIR = sys.path[0]
LOGGING_CONF_PATH = os.path.join(ROOT_DIR, 'logging.conf')

logging.config.fileConfig(LOGGING_CONF_PATH)

if __name__ == '__main__':
  app.run(host='0.0.0.0')