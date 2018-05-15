#!/usr/bin/env python

from setuptools import setup

setup(
    name='qbertconfig',
    description='Fetches kubeconfigs from qbert API',
    author='Platform9',
    classifiers=[
        'Environment :: Platform9',
        'Intended Audience :: Platform9 Managed Kubernetes Operators',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7'
    ],
    packages=['qbertconfig'],
    entry_points={
        'console_scripts': [
            'qc=qbertconfig.cli.main:main'
        ],
    }
)
