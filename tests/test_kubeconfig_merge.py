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

import logging

from qbertconfig.kubeconfig import Kubeconfig
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
