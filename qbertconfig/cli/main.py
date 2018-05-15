#!/usr/bin/env python

import sys
import argparse
import logging
import os_client_config
from keystoneauth1.exceptions import MissingRequiredOptions

# local imports
from qbertconfig.Kubeconfig import Kubeconfig
from dispatcher import Dispatcher

LOG = logging.getLogger(__name__)

def main(args=None):
    """ Main CLI Entrypoint """

    parser = argparse.ArgumentParser(description='Manages Kubeconfig files')
    parser.add_argument('-k', '--kubeconfig',
                        dest='kubeconfig', help='Path to Kubeconfig file')

    # Positional Arguments
    parser.add_argument('operation', nargs='?', default='help')
    parser.add_argument('targets', nargs='+', default='clusters')

    # Register os_client_config argparse arguments
    cloud_config = os_client_config.OpenStackConfig()
    cloud_config.register_argparse_arguments(parser, sys.argv)

    args = parser.parse_args()

    ## Try to get a cloud from os_client_config
    cloud = None
    try:
        cloud = cloud_config.get_one_cloud(argparse=args)
    except MissingRequiredOptions as ex:
        # We may not need this, don't fail
        LOG.warn("Unable to validate openstack credentials. Bad things may happen soon... Check this error out: \n" + ex.message)

    kcfg = Kubeconfig(cli_arg=args.kubeconfig)

    dis = Dispatcher(cloud, kcfg)
    dis.do(args.operation, args.targets)

    # If the kubeconfig does not exist, or it exists but the desired context is not found
    # Require that a cloud is specified
    # Else - gather the kubeconfig from qbert
    kcfg.fetch(cloud, cluster_name='DevOps Services')
    kcfg.save()

    print("Hello World!")