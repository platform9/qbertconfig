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
    parser.add_argument('--name', dest='name', help='Cluster Name')
    parser.add_argument('--uuid', dest='uuid', help='Cluster UUID')

    # Register os_client_config argparse arguments
    cloud_config = os_client_config.OpenStackConfig()
    cloud_config.register_argparse_arguments(parser, sys.argv)

    args = parser.parse_args()

    # Try to get a cloud from os_client_config
    cloud = None
    try:
        cloud = cloud_config.get_one_cloud(argparse=args)
    except MissingRequiredOptions as ex:
        # We may not need this, don't fail
        LOG.warn("Unable to validate openstack credentials. Bad things may happen soon... "
                 "Check this error out: \n" + ex.message)

    kcfg = Kubeconfig(kcfg_path=args.kubeconfig)
    dis = Dispatcher(cloud, kcfg)
    dis.do(args.operation, args)
