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
import sys
import base64
import json

from qbertconfig.tests.base import QcTestCase
import tests.samples as samples
import tests.samples.qbertclient as qbertclient_samples
from qbertconfig.cli.operation.fetch import Fetch
from qbertconfig.kubeconfig import Kubeconfig
from qbertconfig.qbertclient import QbertClient

PYTHON2 = False
if sys.version_info[0] == 2:
    PYTHON2 = True

if PYTHON2:
    from mock import patch, MagicMock
else:
    from unittest.mock import patch, MagicMock

LOG = logging.getLogger(__name__)


class OperationFetchTest(QcTestCase):
    @patch('qbertconfig.qbertclient.QbertClient.__init__')
    def test_fetch_save(self, mock_qbertclient_init):
        """
        Fetching a kubeconfig should save it to the filesystem and return the Kubeconfig object
        """
        # Mock the QbertClient's init to do nothing
        mock_qbertclient_init.return_value = None

        # Mock the functions we use from QbertClient
        qc = QbertClient()
        qc.find_cluster = MagicMock(return_value=qbertclient_samples.FIND_CLUSTER_DEFAULT)
        qc.get_credentials = MagicMock(return_value=qbertclient_samples.GET_CREDENTIALS_DEFAULT)
        qc.get_cloud_fqdn = MagicMock(return_value=qbertclient_samples.GET_CLOUD_FQDN_DEFAULT)
        qc.get_keystone_token = MagicMock(return_value=qbertclient_samples.GET_KEYSTONE_TOKEN_DEFAULT)
        qc.get_kubeconfig = MagicMock(return_value=qbertclient_samples.GET_KUBECONFIG_DEFAULT)

        # pretend we're parsing args via argparse
        args = samples.DEFAULT_PARSED_ARGS

        fetcher = Fetch(qbertclient=qc, args=args)
        fetched_kubeconfig = fetcher.run()
        self.assertIsInstance(fetched_kubeconfig, Kubeconfig)

        # check the filesystem for the kubeconfig file
        fromfile_kubeconfig = Kubeconfig(kcfg_path=args.kubeconfig)
        self.assertEquals(fetched_kubeconfig, fromfile_kubeconfig)

    @patch('qbertconfig.qbertclient.QbertClient.__init__')
    def test_fetch_encode_creds(self, mock_qbertclient_init):
        """
        Specifying the -c or --encode-creds flag should use base64-encoded credentials instead of a keystone token
        """

        # Mock the QbertClient's init to do nothing
        mock_qbertclient_init.return_value = None

        # Mock the functions we use from QbertClient
        qc = QbertClient()
        qc.find_cluster = MagicMock(return_value=qbertclient_samples.FIND_CLUSTER_DEFAULT)
        qc.get_credentials = MagicMock(return_value=qbertclient_samples.GET_CREDENTIALS_DEFAULT)
        qc.get_cloud_fqdn = MagicMock(return_value=qbertclient_samples.GET_CLOUD_FQDN_DEFAULT)
        qc.get_keystone_token = MagicMock(return_value=qbertclient_samples.GET_KEYSTONE_TOKEN_DEFAULT)
        qc.get_kubeconfig = MagicMock(return_value=qbertclient_samples.GET_KUBECONFIG_DEFAULT)

        # generate a kubeconfig without encoding credentials (with a keystone token)
        default_args = samples.DEFAULT_PARSED_ARGS
        default_fetcher = Fetch(qbertclient=qc, args=default_args)
        token_kubeconfig = default_fetcher.run()
        # check that this kubeconfig is using a keystone token
        self.assertEquals(token_kubeconfig.kubeconfig['users'][0]['user']['token'],
                          qbertclient_samples.GET_KEYSTONE_TOKEN_DEFAULT)

        # generate a kubeconfig with encoded credentials
        creds_args = samples.ENCODE_CREDS_ARGS
        creds_fetcher = Fetch(qbertclient=qc, args=creds_args)
        creds_kubeconfig = creds_fetcher.run()
        # check that the kubeconfig has a bearer token with encoded credentials
        encoded_creds = creds_kubeconfig.kubeconfig['users'][0]['user']['token']
        decoded_creds = base64.b64decode(encoded_creds).decode('utf-8')
        kubeconfig_creds = json.loads(decoded_creds)
        self.assertEquals(kubeconfig_creds, qbertclient_samples.GET_CREDENTIALS_DEFAULT)
