# Copyright 2018 Platform9 Systems, Inc.

import logging
import os

# Configure Logging to log both to file and to stdout
LOG_DIR = '.'
try:
    LOG_DIR = os.environ['LOG_DIR']
except KeyError:
    print("LOG_DIR is not specified as an environment variable. Logging to current dir.")

root_logger = logging.getLogger('')

log_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

console_handler = logging.StreamHandler()
console_handler.setFormatter(log_format)
if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)
file_handler = logging.FileHandler(os.path.join(LOG_DIR, 'qbertconfig.log'))
file_handler.setFormatter(log_format)

root_logger.addHandler(console_handler)
root_logger.addHandler(file_handler)

root_logger.setLevel(logging.INFO)
