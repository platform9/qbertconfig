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

from qbertconfig.cli.operation import Operation


class Help(Operation):
    def __init__(self, *args, **kwargs):
        # override the __init__ method to remove dependency on qbertconfig.qbertclient.QbertClient
        pass

    def run(self):
        print("""QbertConfig

Fetches kubeconfig from qbert API

Usage: qc [-h] [-k KUBECONFIG] <operation> [--name cluster_name] [--uuid cluster_uuid] [-c]

Specifying your credentials: Qbertconfig uses the same authentication methods as OpenstackSDK
and other Openstack clients. For more info, please follow this guide:
https://docs.openstack.org/os-client-config/latest/user/configuration.html

Supported Operations:
fetch - get a kubeconfig for a PMK cluster
help - show this message
list-clusters - list all clusters in the PMK Cloud project""")
