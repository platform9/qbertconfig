# Qbertconfig

Fetches kubeconfig from qbert API

Although the [`kubectl config`](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#config) command is used to manage kubeconfigs, we have no way to pull a kubeconfig from Platform9 Managed Kubernetes' Qbert API. This aims to solve that problem by downloading and merging clusters' kubeconfigs with existing kubeconfig files.

## Prerequisites

- Python 2.7+
- Python Openstack Clients [[Documentation](http://docs.platform9.com/support/tutorial-getting-started-with-the-openstack-command-line/)]
- Openstack Credentials to a Platform9 Managed Kubernetes cloud [[Documentation](https://docs.openstack.org/os-client-config/latest/user/configuration.html)]

## Installation

It's strongly recommended to use a python virtualenv

```bash
pip install qbertconfig
```

## Usage

```bash
qc [-h] [-k KUBECONFIG] fetch [--name cluster_name] [--uuid cluster_uuid]
```

_Note: The client also supports all `--os` cli flags provided by os-client-config_

## Testing

Yes, really, there are tests

```bash
pip install -r requirements.txt
nosetests -v -d tests/
```

## How it works

Here is the basic structure of a Kubeconfig:

```yaml
apiVersion: v1
kind: Config
preferences: {}
current-context: default
clusters: []
contexts: []
users: []
```

Each of cluster, context, or user, has a `name` associated with it. This is the unique identifier for each object, and each context uses these names to tie it all together.

Each of these sections can be managed with the `kubectl config` command. [[Documentation](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#config)]

This utility will fetch a fresh kubeconfig from the Qbert API, and merge it's details into the specified kubeconfig.

With the fresh kubeconfig, the following sections are renamed to resolve common collisions when managing many PMK clouds.

- `user` is renamed to `fqdn-username` to align with unique keystone environments
- `context` is renamed to the `cluster_name`
- `cluster` is renamed to the `cluster_uuid`
