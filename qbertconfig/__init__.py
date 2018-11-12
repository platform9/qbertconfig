# Copyright 2018 Platform9 Systems, Inc.

# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy
# of the License at

#   http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import logging
import os

from ._version import get_versions

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


__version__ = get_versions()['version']
del get_versions
