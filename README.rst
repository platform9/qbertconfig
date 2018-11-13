Qbertconfig
===========

Fetches kubeconfig from qbert API

Although the `kubectl config`_ command is used to manage
kubeconfigs, we have no way to pull a kubeconfig from Platform9 Managed
Kubernetes’ Qbert API. This aims to solve that problem by downloading
and merging clusters’ kubeconfigs with existing kubeconfig files.

Installation
------------

It’s strongly recommended to use a python virtualenv

.. code:: bash

   pip install qbertconfig

Usage
-----

.. code:: bash

   qc [-h] [-k KUBECONFIG] fetch [--name cluster_name] [--uuid cluster_uuid]

*Note:* The client also supports all ``--os`` cli flags provided by
os-client-config

Testing
-------

Yes, really, there are tests

.. code:: bash

   pip install -r requirements.txt
   nosetests -v -d tests/

How it works
------------

Here is the basic structure of a Kubeconfig:

.. code:: yaml

   apiVersion: v1
   kind: Config
   preferences: {}
   current-context: default
   clusters: []
   contexts: []
   users: []

Each of cluster, context, or user, has a ``name`` associated with it.
This is the unique identifier for each object, and each context uses
these names to tie it all together.

Each of these sections can be managed with the ``kubectl config``
command. [`Documentation`_]

This utility will fetch a fresh kubeconfig from the Qbert API, and merge
it’s details into the specified kubeconfig.

With the fresh kubeconfig, the following sections are renamed to resolve
common collisions when managing many PMK clouds.

-  ``user`` is renamed to ``fqdn-username`` to align with unique
   keystone environments
-  ``context`` is renamed to the ``cluster_name``
-  ``cluster`` is renamed to the ``cluster_uuid``

.. _kubectl config: https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#config
.. _Documentation: https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#config