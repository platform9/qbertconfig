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
import urlparse
from yaml import safe_load

LOG = logging.getLogger(__name__)


class QbertClient(object):
    """ A (limited) client for the qbert API """

    def __init__(self, os_cloud):
        self.cloud = os_cloud
        if not self.cloud:
            raise CloudNotFoundException

        self.client = self.cloud.get_session_client('qbert', version=2)

    def list_clusters(self):
        response = self.client.get('/clusters')
        cluster_list = response.json()

        return cluster_list

    def get_kubeconfig(self, cluster):
        """ Download a kubeconfig file for the specified cluster

        Args:
            cluster: cluster dictionary as returned by qbert API

        Returns:
            dictionary representation of a yaml kubeconfig file
        """
        LOG.info("Getting kubeconfig for cluster '%s' (%s)", cluster['name'], cluster['uuid'])
        response = self.client.get('/kubeconfig/{}'.format(cluster['uuid']))
        body = response.text
        LOG.debug('Received kubeconfig from Qbert API')

        # Hash credentials and store with kubeconfig
        credentials = {
            "username": self.client.session.auth._username,
            "password": self.client.session.auth._password
        }
        credential_string = json.dumps(credentials)
        bearer_token = base64.b64encode(credential_string)
        raw_kubeconfig = body.replace("__INSERT_BEARER_TOKEN_HERE__", bearer_token)

        kubeconfig = safe_load(raw_kubeconfig)

        # change cluster name to cluster UUID
        kubeconfig['clusters'][0]['name'] = cluster['uuid']
        kubeconfig['contexts'][0]['context']['cluster'] = cluster['uuid']
        # change context name to cluster name
        kubeconfig['contexts'][0]['name'] = cluster['name']
        # change user to fqdn-username
        cloud_fqdn = urlparse.urlparse(self.cloud.config['auth']['auth_url']).netloc
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
            cluster_uuids = ''
            for c in clusters:
                cluster_uuids += '{uuid}: {name}\n'.format(uuid=c['uuid'], name=c['name'])
            LOG.info('Clusters in list: \n%s' % cluster_uuids)
            raise ClusterNotFoundException(search_val)
        else:
            cluster = cluster_found[0]

        return cluster


class CloudNotFoundException(Exception):
    """ Unable to get an Openstack Cloud """
    def __init__(self):
        super(CloudNotFoundException, self).__init__(
            ("No cloud was specified"))


class ClusterNotFoundException(Exception):
    """ Unable to find qbert cluster """
    def __init__(self, cluster):
        super(ClusterNotFoundException, self).__init__(
            ("Unable to find qbert cluster %s" % cluster))
        self.cluster = cluster
