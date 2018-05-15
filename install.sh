#!/usr/bin/env bash

# This script will install kubeconfig-manage into the current virtualenv

# Install newton python-openstackclient
pip install --upgrade \
--requirement https://raw.githubusercontent.com/platform9/support-locker/master/openstack-clients/requirements.txt \
--constraint http://raw.githubusercontent.com/openstack/requirements/stable/newton/upper-constraints.txt
# Patch openstackclient - not really required, but not a bad idea
pip install --upgrade git+https://github.com/openstack/python-openstackclient.git@newton-eol

# Install prerequisites
pip install -r requirements.txt

# Build self and install into current python environment
python setup.py develop
