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

import os

from setuptools import setup, find_packages

def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as fn:
        return fn.read()

setup(
    name='qbertconfig',
    version='0.1.0',
    description='Fetches kubeconfigs from qbert API',
    long_description=read('README.md'),
    url='https://github.com/platform9-incubator/qbertconfig',
    author='Graham Rounds',
    author_email='graham@platform9.com',
    license='Apache License 2.0',
    classifiers=[
        'Environment :: Platform9',
        'Intended Audience :: Platform9 Managed Kubernetes Operators',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7'
    ],
    keywords='Kubeconfig Qbert Platform9 PMK',
    packages=find_packages(exclude=['*.tests', 'tests.*', 'tests', '*.tests.*']),
    install_requires=[
        'keystoneauth1',
        'os_client_config==1.29.0'
    ],
    python_requies='>2.7',
    entry_points={
        'console_scripts': [
            'qc=qbertconfig.cli.main:main'
        ],
    }
)
