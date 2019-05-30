Qbertconfig
===========

.. image:: https://travis-ci.org/platform9/qbertconfig.svg?branch=master
    :target: https://travis-ci.org/platform9/qbertconfig

Fetches kubeconfig from qbert API

`kubectl config`_ can be used used to manage kubeconfig files. However, 
gathering a kubeconfig file for a Platform9 Managed Kubernetes cluster is 
a manual process today. This aims to solve that problem by downloading
and merging clusters’ kubeconfigs with existing kubeconfig files.

Installation
------------

It’s strongly recommended to use a python virtualenv

.. code:: bash

   pip install qbertconfig

Usage
-----

.. code:: bash

   qc [-h] [-k KUBECONFIG] <operation> [--name cluster_name] [--uuid cluster_uuid] [-c]

**Supported Operations**

- **fetch** - get a kubeconfig for a PMK cluster
- **help** - show this message
- **list-clusters** - list available PMK clusters in the target Platform9 Managed Cloud

**Providing Credentials**

Qbertconfig uses the `Openstack SDK`_ to perform authentication against a
Platform9 Cloud. Credentials can be provided in either a ``clouds.yaml`` file,
environment variables, or by using the ``--os`` command-line arguments. For more
information, please refer to the `official documentation`_

**Example**

.. code:: bash

    source ~/openstack.rc
    qc fetch --name dev-cluster -k dev-cluster.kcfg.yml
    export KUBECONFIG=$(pwd)/dev-cluster.kcfg.yml
    kubeconfig get nodes --context dev-cluster
    kubeconfig get pods -n foo

For more information on openstack rc files and how to generate them, see
`Installing Openstack CLI Clients`_.

Testing
-------

Running Tests

.. code:: bash

   pip install -r requirements.txt
   nosetests -v -d tests/

Linting

.. code:: bash

   flake8 --exclude versioneer.py

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
.. _Openstack SDK: https://docs.openstack.org/openstacksdk/latest/
.. _official documentation: https://docs.openstack.org/os-client-config/latest/user/configuration.html
.. _Installing Openstack CLI Clients: https://docs.platform9.com/support/getting-started-with-the-openstack-command-line/