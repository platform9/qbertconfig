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

import base64
import json
import logging
import sys

from qbertconfig.cli.operation import Operation
from qbertconfig.kubeconfig import Kubeconfig

PYTHON2 = False
if sys.version_info[0] == 2:
    PYTHON2 = True

LOG = logging.getLogger(__name__)


class Fetch(Operation):
    def __init__(self, qbertclient=None, args=None):
        self.cluster_name = args.name if args.name else None
        self.cluster_uuid = args.uuid if args.uuid else None
        self.use_creds = args.use_creds

        kcfg_path = args.kubeconfig if args.kubeconfig else ""
        self.kubeconfig = Kubeconfig(kcfg_path=kcfg_path)

        if PYTHON2:
            super(Fetch, self).__init__(qbertclient)
        else:
            super().__init__(qbertclient)
        pass

    def run(self):
        """ Using the qbert API, download a kubeconfig file for the specified cluster

        Returns:
            qbertconfig.Kubeconfig object
        """

        LOG.debug("Cluster: '%s' (%s)", self.cluster_name, self.cluster_uuid)

        cluster = self.connection.find_cluster(self.cluster_uuid, self.cluster_name)
        credentials = self.connection.get_credentials()
        cloud_fqdn = self.connection.get_cloud_fqdn()

        bearer_token = ""
        if self.use_creds:
            bearer_token = self.connection.get_keystone_token()
        else:
            credential_string = json.dumps(credentials)
            if PYTHON2:
                bearer_token = base64.b64encode(bytes(credential_string))
            else:
                bearer_token = base64.b64encode(bytes(credential_string, 'utf-8'))
            # base64.b4encode gives us a bytes, convert back to string
            bearer_token = bearer_token.decode('utf-8')

        raw_kubeconfig = self.connection.get_kubeconfig(cluster)
        # Replace the token placeholder with a real "token"
        raw_kubeconfig['users'][0]['user']['token'] = bearer_token

        # Organize the kubeconfig for merging
        new_kubeconfig = Kubeconfig(kcfg=raw_kubeconfig)
        new_kubeconfig.organize_kubeconfig(cluster, cloud_fqdn, credentials['username'])

        # Merge and return the kubeconfigs
        self.kubeconfig.merge_kubeconfigs(new_kubeconfig)
        self.kubeconfig.save()
        print("Successfully fetched kubeconfig for cluster %s (%s)" % (cluster['name'], cluster['uuid']))
        return self.kubeconfig
