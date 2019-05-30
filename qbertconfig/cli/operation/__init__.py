# Copyright 2019 Platform9 Systems, Inc.

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

LOG = logging.getLogger(__name__)


class Operation(object):
    """ A standard qbertconfig Operation
    """

    def __init__(self, qbertclient=None):
        """ Initialize a QbertClient session

        Args:
            qbertclient: An initialized qbertconfig.qbertclient object
        """
        # initialize the connection
        self.connection = qbertclient

    def run(self):
        """ Performs an operation """
        pass
