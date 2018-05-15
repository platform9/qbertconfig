#!/usr/bin/env python
import os
import logging

from yaml import safe_load, safe_dump

# Local imports
from QbertClient import QbertClient

LOG = logging.getLogger(__name__)

DEFAULT_KUBECONFIG='~/.kube/config'
# the piece of kubeconfig we care about
KUBECONFIG_REPEATABLES = ['clusters', 'users', 'contexts']

class Kubeconfig(object):
    """ High level class to describe operations on kubeconfigs """
    def __init__(self, kcfg_path=None, kcfg_yaml=None, kcfg=None):
        self.kubeconfig_path = self.determine_location(kcfg_path)
        if kcfg:
            # User provided us with the kubeconfig
            LOG.debug('Using user provided Kubeconfig')
            self.kubeconfig = kcfg
        else:
            # Attempt to load from yaml or file
            existing_kubeconfig = self.read()

            # load the kubeconfig from string
            if kcfg_yaml:
                loaded_kcfg = safe_load(kcfg_yaml)
                if existing_kubeconfig != {}:
                    LOG.warn('kubeconfig already exists at %s. It will be overwritten', self.kubeconfig_path)
                LOG.debug('Using provided yaml as kubeconfig')
                self.kubeconfig = loaded_kcfg
            else:
                LOG.debug('Using kubeconfig as loaded from file')
                self.kubeconfig = existing_kubeconfig

    def __eq__(self, other):
        # TODO: This only checks that the NAMES are the same. This doesn't catch when the content is
        #       different but the names are the same.
        if isinstance(other, self.__class__):
            # check that both objects have the same clusters, contexts, & users
            for item in KUBECONFIG_REPEATABLES:
                names = [c['name'] for c in self.kubeconfig[item]]
                incoming_names = [c['name'] for c in other.kubeconfig[item]]
                if set(names) != set(incoming_names):
                    return False
            return True
        else:
            return False

    def read(self):
        """ Loads the current kubeconfig from file
        """
        if not os.path.isfile(self.kubeconfig_path):
            LOG.debug('Kubeconfig not found at %s', self.kubeconfig_path)
            return {}
        else:
            with open(self.kubeconfig_path) as kcfg_f:
                LOG.debug('Reading kubeconfig at %s', self.kubeconfig_path)
                return safe_load(kcfg_f)

    def save(self):
        """ Saves the current kubeconfig to file
        """
        kcfg_dir = os.path.dirname(self.kubeconfig_path)
        LOG.debug('saving to %s' % kcfg_dir)
        if not os.path.exists(kcfg_dir):
            os.makedirs(kcfg_dir)

        # File has not be created yet
        with open(self.kubeconfig_path, "w+") as kcfg_f:
            kcfg_f.write(safe_dump(self.kubeconfig))

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
        new_kubeconfig = Kubeconfig(kcfg=qbert.get_kubeconfig(cluster))
        self.kubeconfig = self.merge_kubeconfigs(new_kubeconfig)

    def determine_location(self, kcfg_path=None):
        """ Identifies which kubeconfig is currently to be used.

        This will load the kubeconfig from the following locations in this precedence order:
        - specified in '--kubeconfig' flag
        - specified in $KUBECONFIG environment variable
        - home directory location ~/.kube/config

        Returns:
            The identified kubeconfig file to use
        """
        kubeconfig_env = None
        try:
            kubeconfig_env = os.environ['KUBECONFIG']
        except KeyError:
            pass # :its_fine:

        # Determine
        kubeconfig_path = None
        if kcfg_path:
            kubeconfig_path = kcfg_path
        elif kubeconfig_env:
            kubeconfig_path = kubeconfig_env
        else:
            kubeconfig_path = DEFAULT_KUBECONFIG

        # Clean it up
        kubeconfig_path = os.path.expanduser(kubeconfig_path)
        kubeconfig_path = os.path.expandvars(kubeconfig_path)

        return kubeconfig_path

    def merge_kubeconfigs(self, new_kubeconfig):
        """ Soft merges two kubeconfig files.
        If name matches for cluster, context, or user the new_kubeconfig will be preferred

        Args:
            new_kubeconfig: A Kubeconfig object to merge into this one

        Returns:
            The merged kubeconfig dictionary
        """

        LOG.debug('Current kubeconfig:\n%s', self.kubeconfig)
        LOG.debug('Incoming kubeconfig:\n%s', new_kubeconfig.kubeconfig)
        if self.kubeconfig == {}:
            LOG.debug('Source is empty, no merging required')
            # it's a fresh kubeconfig! no need to merge anything
            self.kubeconfig = new_kubeconfig
            return self.kubeconfig

        result = self.kubeconfig
        for category in KUBECONFIG_REPEATABLES:
            incoming_list = new_kubeconfig.kubeconfig[category]

            # merge based on the key 'name'
            for inc in incoming_list:
                merged = False
                for index, item in enumerate(result[category]):
                    if item['name'] == inc['name']:
                        LOG.debug('Item %s found in %s. Overwriting', inc['name'], category)
                        result[category][index] = inc
                        merged = True
                if not merged:
                    LOG.debug('Item %s not found in %s. Appending', inc['name'], category)
                    result[category].append(inc)
        LOG.debug('After merge:\n%s', result)
        self.kubeconfig = result

        return self.kubeconfig
