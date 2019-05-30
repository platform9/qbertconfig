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
import sys
from contextlib import contextmanager

from qbertconfig.tests.base import QcTestCase
import tests.samples as samples
import tests.samples.qbertclient as qbertclient_samples
from qbertconfig.qbertclient import QbertClient

from qbertconfig.cli.operation.list_clusters import ListClusters

LOG = logging.getLogger(__name__)

PYTHON2 = False
if sys.version_info[0] == 2:
    PYTHON2 = True

# python2 compat
if PYTHON2:
    from io import BytesIO as StringIO
    from mock import patch, MagicMock
else:
    from io import StringIO
    from unittest.mock import patch, MagicMock


@contextmanager
def captured_output():
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err


class OperationFetchTest(QcTestCase):
    @patch('qbertconfig.qbertclient.QbertClient.__init__')
    def test_listclusters(self, mock_qbertclient_init):
        """
        Listing Clusters should print a list of clusters to stdout
        """
        # Mock the QbertClient's init to do nothing
        mock_qbertclient_init.return_value = None

        # Mock the functions we use from QbertClient
        qc = QbertClient()
        qc.list_clusters = MagicMock(return_value=qbertclient_samples.LIST_CLUSTERS_DEFAULT)

        # pretend we're parsing args via argparse
        args = samples.DEFAULT_PARSED_ARGS

        lister = ListClusters(qbertclient=qc, args=args)
        with captured_output() as (out, err):
            lister.run()

        output = out.getvalue().strip()
        self.assertEqual(output, "Clusters in this region:\n"
                                 "bareos (5f69a5da-2780-4a30-8663-3c76f154dd67)\n"
                                 "openstack-cluster (69b9a7b2-1508-4e33-9bac-5a9232cc7f26)")
