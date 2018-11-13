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

from ._version import get_versions

# Log to stdout
root_logger = logging.getLogger('')

log_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

console_handler = logging.StreamHandler()
console_handler.setFormatter(log_format)

root_logger.addHandler(console_handler)
root_logger.setLevel(logging.INFO)

# To supress keystone discovery warnings
keystone_logger = logging.getLogger('keystoneauth')
keystone_logger.setLevel(logging.ERROR)

# Added by versioneer
__version__ = get_versions()['version']
del get_versions
