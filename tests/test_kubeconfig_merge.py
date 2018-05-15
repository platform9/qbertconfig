#!/usr/bin/env python

import logging

from qbertconfig.Kubeconfig import Kubeconfig
from qbertconfig.tests.base import QcTestCase
import tests.samples.kubeconfigs as samples

LOG = logging.getLogger(__name__)

class KubeconfigMergeTest(QcTestCase):
    def test_adding_duplicate(self):
        """
        Adding a kubeconfig that exists should not change the object
        """
        initial_kubeconfig = self.kubeconfig
        incoming_kubeconfig = Kubeconfig(kcfg=samples.BASE_TEST_KUBECONFIG)

        initial_kubeconfig.merge_kubeconfigs(incoming_kubeconfig)
        self.assertEqual(initial_kubeconfig, Kubeconfig(kcfg=samples.BASE_TEST_KUBECONFIG))

    def test_adding_partial_match(self):
        """
        Adding a kubeconfig with some matching entities should append new ones and update others
        """
        initial_kubeconfig = self.kubeconfig
        incoming_kubeconfig = Kubeconfig(kcfg=samples.PARTIAL_UNIQUE_KUBECONFIG)

        initial_kubeconfig.merge_kubeconfigs(incoming_kubeconfig)
        self.assertEqual(initial_kubeconfig, Kubeconfig(kcfg=samples.BASE_TEST_KUBECONFIG))
