#!/usr/bin/env python

import logging
import sys

import qbertconfig.Kubeconfig as Kubeconfig

LOG = logging.getLogger(__name__)

""" Dispatcher performs operations we care about """

class Dispatcher(object):

    def __init__(self, cloud, kubeconfig):
        self.cloud = cloud
        self.kubeconfig = kubeconfig

    def do(self, operation, targets):
        # TODO: input sanitization
        return getattr(self, operation)(targets)

    def fetch(self, args):
        cluster_name = args.name if args.name else None
        cluster_uuid = args.uuid if args.uuid else None
        self.kubeconfig.fetch(self.cloud, cluster_name=cluster_name, cluster_uuid=cluster_uuid)
        self.kubeconfig.save()
