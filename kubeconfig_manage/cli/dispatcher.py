#!/usr/bin/env python

import logging
import sys

import kubeconfig_manage.Kubeconfig as Kubeconfig

LOG = logging.getLogger(__name__)

""" Dispatcher performs operations we care about """

class Dispatcher(object):

    def __init__(self, cloud, kubeconfig):
        self.cloud = cloud
        self.kubeconfig = kubeconfig

    def do(self, operation, targets):
        # TODO: input sanitization
        return getattr(self, operation)(targets)

    def get(self, items):
        for item in items:
            if item not in Kubeconfig.KUBECONFIG_REPEATABLES:
                LOG.error("Unknown item: %s", item)
            else:
                for k, v in self.kubeconfig.kubeconfig.iteritems():
                    if k == item:
                        return v
