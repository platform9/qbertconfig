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
from qbertconfig.cli.operation import Operation
from qbertconfig.kubeconfig import Kubeconfig

PYTHON2 = False
if sys.version_info[0] == 2:
    PYTHON2 = True

LOG = logging.getLogger(__name__)


class ListClusters(Operation):
    def __init__(self, qbertclient=None, args=None):
        self.cluster_name = args.name if args.name else None
        self.cluster_uuid = args.uuid if args.uuid else None

        kcfg_path = args.kubeconfig if args.kubeconfig else ""
        self.kubeconfig = Kubeconfig(kcfg_path=kcfg_path)

        if PYTHON2:
            super(ListClusters, self).__init__(qbertclient)
        else:
            super().__init__(qbertclient)
        pass

    def run(self):
        """ Using the qbert API, list all clusters in the current project """

        LOG.debug("Cluster: '%s' (%s)", self.cluster_name, self.cluster_uuid)
        clusters = self.connection.list_clusters()
        msg = ''
        cluster_uuids = ''
        for c in clusters:
            cluster_uuids += '{name} ({uuid})\n'.format(uuid=c['uuid'], name=c['name'])
        msg += "\n\nClusters in this region:\n{}".format(cluster_uuids)
        print(msg)
