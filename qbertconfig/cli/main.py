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
from importlib import import_module

# local imports
from qbertconfig.qbertclient import QbertClient

LOG = logging.getLogger(__name__)


def get_module(classname):
    """ Dynamically import module based on classname """
    module_parts = classname.split('.')
    class_name = module_parts.pop()
    m = import_module('.'.join(module_parts))
    return getattr(m, class_name, None)


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
    parser.add_argument('-c', '--encode-creds', dest='use_creds', action='store_true',
                        help='Use OpenStack credentials instead of keystone token')

    # Register OpenStack argparse arguments
    cloud_config = openstack.config.OpenStackConfig()
    cloud_config.register_argparse_arguments(parser, sys.argv)

    args = parser.parse_args()

    # Initialize a QbertClient
    # Skip this step for operations that do not require a QbertClient
    qbertclient = None
    if args.operation != 'help':
        qbertclient = QbertClient(parsed_args=args)

    # Mapping of args.operation to qbertconfig.cli.operation
    op_map = {
        'fetch': 'qbertconfig.cli.operation.fetch.Fetch',
        'help': 'qbertconfig.cli.operation.help.Help',
        'list-clusters': 'qbertconfig.cli.operation.list_clusters.ListClusters',
        'list-cluster': 'qbertconfig.cli.operation.list_clusters.ListClusters'
    }

    try:
        # find operation in mapping
        op_module = get_module(op_map[args.operation])
        operation = op_module(qbertclient=qbertclient, args=args)
        operation.run()
    except KeyError:
        # Operation not found in mapping
        # Display help text
        op_map['help']().run()
    except Exception as ex:
        LOG.error("An unexpected error occurred")
        LOG.exception(ex)
        sys.exit(1)


if __name__ == "__main__":
    main()
    sys.exit(0)
