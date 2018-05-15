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
    def __init__(self, cli_arg=None):
        self.kubeconfig_path = self.determine_location(cli_arg)
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

    def determine_location(self, cli_arg):
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
            pass # :its_fine:

        if cli_arg:
            kubeconfig_path = cli_arg
        elif kubeconfig_env:
            kubeconfig_path = kubeconfig_env
        else:
            kubeconfig_path = DEFAULT_KUBECONFIG

        # Check if file exists
        if not os.path.isfile(kubeconfig_path):
            LOG.info('No Kubeconfig at specified location. Using default location %s' % DEFAULT_KUBECONFIG)
            kubeconfig_path = DEFAULT_KUBECONFIG

        # Clean it up
        kubeconfig_path = os.path.expanduser(kubeconfig_path)
        kubeconfig_path = os.path.expandvars(kubeconfig_path)

        return kubeconfig_path

    def load(self):
        """ Loads the current kubeconfig from file
        """
        if not os.path.isfile(self.kubeconfig_path):
            # File may not be created yet
            self.kubeconfig = {}
        else:
            self.kubeconfig = safe_load(self.kubeconfig_path)

    def save(self):
        """ Saves the current kubeconfig to file
        """
        kcfg_dir = os.path.dirname(self.kubeconfig_path)
        LOG.error('saving to %s' % kcfg_dir)
        if not os.path.exists(kcfg_dir):
            os.makedirs(kcfg_dir)

        # File has not be created yet
        with open(self.kubeconfig_path, "w+") as kcfg_f:
            kcfg_f.write(safe_dump(self.kubeconfig))

