#!/usr/bin/env python

""" Example Kubeconfigs """

BASE_TEST_KUBECONFIG = {
    'apiVersion': 'v1',
    'kind': 'Config',
    'preferences': {},
    'current-context': 'test-case-context',
    'clusters': [
        {
            'cluster': {
                'certificate-authority-data': 'certificate-is-wut',
                'server': 'https://test-case-cluster'
            },
            'name': 'test-case-cluster'
        }
    ],
    'contexts': [
        {
            'context': {
                'cluster': 'test-case-cluster',
                'namespace': 'default',
                'user': 'azurediamond'
            },
            'name': 'test-case-context'
        }
    ],
    'users': [
        {
            'user': {
                # azurediamond / hunter2
                'token': 'eyJ1c2VybmFtZSI6ICJhenVyZWRpYW1vbmQiLCAicGFzc3dvcmQiOiAiaHVudGVyMiJ9'
            },
            'name': 'azurediamond'
        }
    ]
}

UNIQUE_KUBECONFIG = {
    'apiVersion': 'v1',
    'kind': 'Config',
    'preferences': {},
    'current-context': 'test-case-context',
    'clusters': [
        {
            'cluster': {
                'certificate-authority-data': 'certificate-is-wut',
                'server': 'https://test-case-cluster'
            },
            'name': 'unique-cluster'
        }
    ],
    'contexts': [
        {
            'context': {
                'cluster': 'unique-cluster',
                'namespace': 'default',
                'user': 'foobar'
            },
            'name': 'unique'
        }
    ],
    'users': [
        {
            'user': {
                # foo / bar
                'token': 'eyJ1c2VybmFtZSI6ICJmb28iLCAicGFzc3dvcmQiOiAiYmFyIn0='
            },
            'name': 'foobar'
        }
    ]
}

PARTIAL_UNIQUE_KUBECONFIG = {
    'apiVersion': 'v1',
    'kind': 'Config',
    'preferences': {},
    'current-context': 'test-case-context',
    'clusters': [
        {
            'cluster': {
                'certificate-authority-data': 'who-was-phone',
                'server': 'https://clusterapocalypse'
            },
            'name': 'clusterapocalypse'
        }
    ],
    'contexts': [
        {
            'context': {
                'cluster': 'clusterapocalypse',
                'namespace': 'default',
                'user': BASE_TEST_KUBECONFIG['users'][0]['name']
            },
            'name': 'partial-unique'
        }
    ],
    'users': BASE_TEST_KUBECONFIG['users']
}

MANGLED_PROPERTIES_KUBECONFIG = {
    'apiVersion': 'v2',
    'kind': 'QbertConfig',
    'preferences': { 'foo': 'bar' },
    'current-context': 'fhqwhgads',
    'clusters': BASE_TEST_KUBECONFIG['clusters'],
    'contexts': BASE_TEST_KUBECONFIG['contexts'],
    'users': BASE_TEST_KUBECONFIG['users']
}