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

import base64
import logging
import json
import sys
from yaml import safe_load

# Python2 Compatability
if sys.version_info[0] == 2:
    from urlparse import urlparse
else:
    from urllib.parse import urlparse

LOG = logging.getLogger(__name__)


class QbertClient(object):
    """ A (limited) client for the qbert API """

    def __init__(self, os_cloud):
        """
        Args:
            os_cloud: an openstack.config.CloudConfig object
        """
        self.cloud = os_cloud
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
        url = self._build_url('/clusters')
        response = self.client.get(url)
        cluster_list = response.json()

        return cluster_list

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
        body = response.text
        LOG.debug('Received kubeconfig from Qbert API')

        # Hash credentials and store with kubeconfig
        credentials = {
            "username": self.client.session.auth._username,
            "password": self.client.session.auth._password
        }
        credential_string = json.dumps(credentials)
        bearer_token = base64.b64encode(bytes(credential_string, 'utf-8'))
        # base64.b4encode gives us a bytes, convert back to string
        bearer_token = bearer_token.decode('utf-8')
        raw_kubeconfig = body.replace("__INSERT_BEARER_TOKEN_HERE__", bearer_token)

        kubeconfig = safe_load(raw_kubeconfig)

        # change cluster name to cluster UUID
        kubeconfig['clusters'][0]['name'] = cluster['uuid']
        kubeconfig['contexts'][0]['context']['cluster'] = cluster['uuid']
        # change context name to cluster name
        kubeconfig['contexts'][0]['name'] = cluster['name']
        # change user to fqdn-username
        cloud_fqdn = urlparse(self.cloud.config['auth']['auth_url']).netloc
        cloud_username = self.cloud.config['auth']['username']
        new_user_name = '{}-{}'.format(cloud_fqdn, cloud_username)
        LOG.debug('Renaming user from %s to %s', kubeconfig['users'][0]['name'], new_user_name)
        kubeconfig['users'][0]['name'] = new_user_name
        kubeconfig['contexts'][0]['context']['user'] = new_user_name

        return kubeconfig

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
