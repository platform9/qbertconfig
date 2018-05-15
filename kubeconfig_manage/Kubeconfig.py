#!/usr/bin/env python
import os
import logging

from yaml import safe_load, safe_dump

# Local imports
from QbertClient import QbertClient

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)

DEFAULT_KUBECONFIG='~/.kube/config'

class Kubeconfig(object):
    """ High level class to describe operations on kubeconfigs """
    def __init__(self, kubeconfig=None):
        self.kubeconfig_path = kubeconfig
        self.kubeconfig = None

    def fetch(self, cloud, cluster_name=None, cluster_uuid=None):
        """ Using the qbert API, download a kubeconfig file for the specified cluster

        Args:
            cluster_name: name of the qbert cluster
            cluster_uuid: ID of the qbert cluster

        Returns:
            The profile name of the kubeconfig added
        """
        LOG.debug("Cluster: '%s' (%s)", cluster_name, cluster_uuid)

        qbert = QbertClient(cloud)
        cluster = qbert.find_cluster(cluster_uuid, cluster_name)
        self.kubeconfig = qbert.get_kubeconfig(cluster)

    def identify_kubeconfig(self):
        """ Identifies which kubeconfig is currently to be used.

        This will load the kubeconfig from the following locations in this precedence order:
        - specified in '--kubeconfig' flag
        - specified in $KUBECONFIG environment variable
        - home directory location ~/.kube/config

        Returns:
            The identified kubeconfig file to use
        """

        kubeconfig_path = None

        # see if we can get the environment variable
        kubeconfig_env = None
        try:
            kubeconfig_env = os.environ['KUBECONFIG']
        except KeyError:
            # :its_fine:
            pass

        if self.kubeconfig_path:
            kubeconfig_path = self.kubeconfig_path
        elif kubeconfig_env:
            kubeconfig_path = kubeconfig_env
        else:
            kubeconfig_path = DEFAULT_KUBECONFIG

        # Check if file exists
        if not os.path.isfile(kubeconfig_path):
            LOG.warn('No Kubeconfig at specified location. Will write to %s' % DEFAULT_KUBECONFIG)
            kubeconfig_path = DEFAULT_KUBECONFIG

        return kubeconfig_path

    def load(self):
        """ Loads the current kubeconfig from file
        """
        kubeconfig_path = self.identify_kubeconfig()

        if not os.path.isfile(kubeconfig_path):
            # File may not be created yet
            self.kubeconfig = {}
        else:
            self.kubeconfig = safe_load(kubeconfig_path)
