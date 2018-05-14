#!/usr/bin/env python

from setuptools import setup

setup(
    name='kubeconfig_manage',
    description='Kubeconfig Manegement Tool',
    author='Platform9',
    classifiers=[
        'Environment :: Platform9',
        'Intended Audience :: Kubernetes Operators',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7'
    ],
    packages=['kubeconfig_manage'],
    entry_points={
        'console_scripts': [
            'kcm=kubeconfig_manage.cli:main'
        ],
    }
)
