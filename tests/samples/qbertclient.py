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

import tests.samples.clusters as cluster_samples
import tests.samples.kubeconfigs as kubeconfig_samples

# QbertClient.get_credentials(..)
GET_CREDENTIALS_DEFAULT = {
    "username": "azurediamond",
    "password": "hunter2"
}

# QbertClient.get_keystone_token(..)
GET_KEYSTONE_TOKEN_DEFAULT = "thisisakeystonetoken-lolnotreally"

# QbertClient.get_kubeconfig(..)
GET_KUBECONFIG_DEFAULT = kubeconfig_samples.API_UNEDITED_KUBECONFIG

# QbertClient.get_cloud_fqdn(..)
GET_CLOUD_FQDN_DEFAULT = "my-cloud.platform9.net"

# QbertClient.find_cluster(..)
FIND_CLUSTER_DEFAULT = cluster_samples.BAREOS_CLUSTER
