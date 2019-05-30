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
from yaml import safe_load
from openstack.config import OpenStackConfig
from keystoneauth1.exceptions import MissingRequiredOptions

# Python2 Compatability
if sys.version_info[0] == 2:
    from urlparse import urlparse
else:
    from urllib.parse import urlparse

LOG = logging.getLogger(__name__)


class QbertClient(object):
    """ A (limited) client for the qbert API """

    def __init__(self, parsed_args=None):
        """ Initializes a QbertClient object

        Args:
            parsed_args: optional CLI arguments parsed via argparse's parse_args()
        """

        # Determine the cloud from env vars, CLI args, and/or clouds.yaml
        self.cloud = None
        try:
            cloud_config = OpenStackConfig()
            self.cloud = cloud_config.get_one_cloud(argparse=parsed_args)
        except MissingRequiredOptions as ex:
            # Don't fail, we can try via other methods
            LOG.error("Unable to validate openstack credentials.\n"
                      "You must specify your credentials in environment variables, clouds.yaml, or via CLI Arguments.\n"
                      "For more information, see this help article: "
                      "https://docs.openstack.org/python-openstackclient/pike/cli/man/openstack.html#manpage")
            raise ex

        self.client = self.cloud.get_session_client('qbert')

    def _build_url(self, url):
        """ Construct a URL for qbert

        Detect latest Qbert version available in the qbert catalog
        Handle the behavior differences in various qbert API versions
        """
        major, minor = self.client.get_api_major_version()

        # in qbert v2 and above, project_id for the cluster is required in the uri
        if major >= 2:
            url = '/{project_id}/{url}'.format(**{
                'project_id': self.client.get_project_id(),
                'url': url
            })

        return url

    def list_clusters(self):
        """ List all clusters in the target PMK Cloud

        Returns:
            Dictionary list as returned from Qbert API
        """
        url = self._build_url('/clusters')
        response = self.client.get(url)
        cluster_list = response.json()

        return cluster_list

    def get_keystone_token(self):
        """ Retrieves a keystone token """
        return self.client.session.get_token()

    def get_credentials(self):
        """ Retrieves credentials currently being used to authenticate against qbert """
        return {
            "username": self.client.session.auth._username,
            "password": self.client.session.auth._password
        }

    def get_cloud_fqdn(self):
        """ Returns the current fqdn for the connected PMK cloud """
        return urlparse(self.cloud.config['auth']['auth_url']).netloc

    def get_kubeconfig(self, cluster):
        """ Download a kubeconfig file for the specified cluster

        Args:
            cluster: cluster dictionary as returned by qbert API

        Returns:
            dictionary representation of a yaml kubeconfig file
        """
        url = self._build_url('/kubeconfig/' + cluster['uuid'])
        LOG.info("Getting kubeconfig for cluster '%s' (%s)", cluster['name'], cluster['uuid'])
        response = self.client.get(url)
        LOG.debug('Received kubeconfig from Qbert API')
        return safe_load(response.text)

    def find_cluster(self, cluster_uuid=None, cluster_name=None):
        """ Searches the list of clusters for a cluster by name OR uuid

        Args:
            cluster_uuid: qbert UUID of the cluster
            cluster_name: common name of the cluster

        Returns:
            dictionary of the cluster as returned by the qbert API
        """
        cluster = None
        if not cluster_name and not cluster_uuid:
            raise Exception('You must specify at least one of cluster name, id')

        # prefer searching by uuid
        search_key = 'name' if not cluster_uuid else 'uuid'
        search_val = cluster_name if not cluster_uuid else cluster_uuid

        clusters = self.list_clusters()
        cluster_found = [c for c in clusters if c[search_key] == search_val]
        if not cluster_found:
            raise ClusterNotFoundException(search_val, clusters)
        else:
            cluster = cluster_found[0]

        return cluster


class ClusterNotFoundException(Exception):
    """ Unable to find qbert cluster """
    def __init__(self, cluster, clusters=[]):
        msg = "Unable to find PMK cluster {}".format(cluster)
        if clusters:
            cluster_uuids = ''
            for c in clusters:
                cluster_uuids += '{name} ({uuid})\n'.format(uuid=c['uuid'], name=c['name'])
            msg += "\n\nClusters in this region:\n{}".format(cluster_uuids)
        super(ClusterNotFoundException, self).__init__(msg)
        self.cluster = cluster
