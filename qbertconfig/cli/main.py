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
import openstack
from keystoneauth1.exceptions import MissingRequiredOptions

# local imports
from qbertconfig.Fetcher import Fetcher
from qbertconfig.Kubeconfig import Kubeconfig
from qbertconfig.cli.dispatcher import Dispatcher

LOG = logging.getLogger(__name__)


def main(args=None):
    """
    Main CLI Entrypoint
    https://docs.openstack.org/openstacksdk/latest/user/config/configuration.html
    """

    parser = argparse.ArgumentParser(description='Manages Kubeconfig files')
    parser.add_argument('-k', '--kubeconfig',
                        dest='kubeconfig', help='Path to Kubeconfig file')

    # Positional Arguments
    parser.add_argument('operation', nargs='?', default='help')
    parser.add_argument('--name', dest='name', help='Cluster Name')
    parser.add_argument('--uuid', dest='uuid', help='Cluster UUID')

    # Register OpenStack argparse arguments
    cloud_config = openstack.config.OpenStackConfig()
    cloud_config.register_argparse_arguments(parser, sys.argv)

    args = parser.parse_args()

    # Try to get a cloud from OpenStack config
    cloud = None
    try:
        cloud = cloud_config.get_one_cloud(argparse=args)
    except MissingRequiredOptions as ex:
        # We may not need this, don't fail
        LOG.warn("Unable to validate openstack credentials."
                 "Bad things may happen soon... Check this error out: \n" + ex.message)
        sys.exit(1)

    qc = Fetcher(kubeconfig=Kubeconfig(kcfg_path=args.kubeconfig), os_cloud=cloud)
    dis = Dispatcher(qc)

    try:
        dis.do(args.operation, args)
    except AttributeError:
        # User specified an operation which doesn't correspond to a method in Dispatcher
        parser.print_usage()
    except Exception as e:
        LOG.error(e)
