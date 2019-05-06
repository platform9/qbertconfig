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
import openstack
from keystoneauth1.exceptions import MissingRequiredOptions

# Local imports
from qbertconfig.QbertClient import QbertClient
from qbertconfig.Kubeconfig import Kubeconfig

LOG = logging.getLogger(__name__)


class Fetcher(object):
    """ Fetches a Kubeconfig from Qbert """
    def __init__(self, kubeconfig=None, os_config=None, os_cloud=None):
        """ From a defined OpenStack Cloud, initialize QbertClient

        If cloud_name is not specified, the default values 'envvars' and 'defaults' will be used.
        The cloud 'envvars' will be preferred to 'defaults' if found.

        Args:
            kubeconfig: qbertconfig.Kubeconfig object
            os_config: an openstack.config.cloud_config.CloudConfig object
            os_cloud: an openstack.config.cloud_region.CloudRegion object
        Returns:
            An initialized qbertconfig.QbertClient object
        """
        self.kubeconfig = kubeconfig
        self.os_config = os_config
        self.os_cloud = os_cloud

        if not self.kubeconfig:
            self.kubeconfig = Kubeconfig()

        self.qbert_session = self._initialize_qbert_client(os_config, os_cloud)

    def _initialize_qbert_client(self, os_config=None, os_cloud=None):
        """ From a defined OpenStack Cloud, initialize QbertClient

        If cloud_name is not specified, the default values 'envvars' and 'defaults' will be used.
        The cloud 'envvars' will be preferred to 'defaults' if found.

        Args:
            os_config: an openstack.config.cloud_config.CloudConfig object

        Returns;
            An initialized qbertconfig.QbertClient object
        """
        if os_cloud:
            self.os_cloud = os_cloud
            return QbertClient(os_cloud=self.os_cloud)

        # Cloud not provided, so see if we need to create config and then get cloud
        if not os_config:
            # this will decide whether to use env vars, or a clouds.yaml
            self.os_config = openstack.config.OpenStackConfig()

        # Now use config to get a cloud
        try:
            self.os_cloud = self.os_config.get_one_cloud()
        except MissingRequiredOptions as e:
            # If this fails, it means no other credentials were provided another way
            LOG.error("Unable to validate openstack credentials. Check this error out: \n" + e.message)
            LOG.error("Check to ensure your OpenStack credentials are in clouds.yaml"
                      " or available as environment variables")
            raise e
        return QbertClient(os_cloud=self.os_cloud)

    def save(self):
        """ Saves the current kubeconfig to file """
        self.kubeconfig.save()

    def fetch(self, cluster_name=None, cluster_uuid=None):
        """
        Using the qbert API, download a kubeconfig file for the specified cluster

        Args:
            cluster_name: name of the qbert cluster
            cluster_uuid: ID of the qbert cluster

        Returns:
            KubeConfig object
        """
        LOG.debug("Cluster: '%s' (%s)", cluster_name, cluster_uuid)
        cluster = self.qbert_session.find_cluster(cluster_uuid, cluster_name)
        new_kubeconfig = Kubeconfig(kcfg=self.qbert_session.get_kubeconfig(cluster))
        self.kubeconfig.merge_kubeconfigs(new_kubeconfig)
        return self.kubeconfig
