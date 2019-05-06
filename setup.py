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
import versioneer
from setuptools import setup, find_packages


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as fn:
        return fn.read()


setup(
    name='qbertconfig',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description='Fetches kubeconfigs from qbert API',
    long_description=read('README.rst'),
    url='https://github.com/platform9/qbertconfig',
    author='Graham Rounds',
    author_email='graham@platform9.com',
    license='Apache License 2.0',
    classifiers=[
        'Environment :: OpenStack',
        'Intended Audience :: System Administrators',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3'
    ],
    keywords='Kubeconfig Qbert Platform9 PMK',
    packages=find_packages(exclude=['*.tests', 'tests.*', 'tests', '*.tests.*']),
    install_requires=[
        'keystoneauth1==3.11.1',
        'openstacksdk==0.19.0'
    ],
    python_requires='>=2.7, >=3.4',
    entry_points={
        'console_scripts': [
            'qc=qbertconfig.cli.main:main'
        ],
    }
)
