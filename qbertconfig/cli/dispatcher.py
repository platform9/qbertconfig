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

LOG = logging.getLogger(__name__)


class Dispatcher(object):

    def __init__(self, cloud, kubeconfig):
        self.cloud = cloud
        self.kubeconfig = kubeconfig

    def do(self, operation, targets):
        # TODO: input sanitization
        return getattr(self, operation)(targets)

    def fetch(self, args):
        cluster_name = args.name if args.name else None
        cluster_uuid = args.uuid if args.uuid else None
        self.kubeconfig.fetch(self.cloud, cluster_name=cluster_name, cluster_uuid=cluster_uuid)
        self.kubeconfig.save()
