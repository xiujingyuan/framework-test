#!/usr/bin/python
# -*- coding: UTF-8 -*-
gbiz_mock = "gbiz_auto_test"
global_gbiz_mock = "global_gbiz_auto_test"
rbiz_mock = "rbiz_auto_test"
global_rbiz_mock = "global_rbiz_auto_test"
global_payment_mock = "global_payment_auto_test"
global_payment_easy_mock = "global_payment_auto_test"
global_payment_easy_mock_phl = "global_payment_test_phl"
base_url = "https://easy-mock.k8s-ingress-nginx.kuainiujinke.com"
account = {
    "user": "carltonliu",
    "password": "lx19891115"
}

mock_project = {
    "gbiz_auto_test": {
        "name": "gbiz",
        "id": "5f9bfaf562081c0020d7f5a7",
        "base_url": base_url,
        "user": account['user'],
        "password": account['password']
    },
    "global_gbiz_auto_test": {
        "name": "nbfc",
        "id": "5e465f0ed53ef1165b982496",
        "base_url": base_url,
        "user": account['user'],
        "password": account['password']
    },
    "rbiz_auto_test": {
        "name": "rbiz_auto_test",
        "id": "5de5d515d1784d36471d6041",
        "base_url": base_url,
        "user": account['user'],
        "password": account['password']
    },
    "contract": {
        "name": "contract",
        "id": "6007a8b11242fa00160534bb",
        "base_url": base_url,
        "user": account['user'],
        "password": account['password']
    },
    "global_rbiz_auto_test": {
        "name": "global_rbiz_auto_test",
        "id": "5e46037fd53ef1165b98246e",
        "base_url": base_url,
        "user": account['user'],
        "password": account['password']
    },
    "global_payment_auto_test": {
        "name": "global_payment_auto_test",
        "id": "5b9a3ddd3a0f7700206522eb",
        "base_url": base_url,
        "user": account['user'],
        "password": account['password']
    },
    "global_payment_test_phl": {
        "name": "global_payment_test_phl",
        "id": "5e9807281718270057767a3e",
        "base_url": base_url,
        "user": account['user'],
        "password": account['password']
    },
    "dcs_auto_test": {
        "name": "dcs",
        "id": "5bd800c7b820c00016b21ddb",
        "base_url": base_url,
        "user": account['user'],
        "password": account['password']
    },
    "old_dcs_auto_test": {
        "name": "dcs",
        "id": "5caeea78c2c04c0020a98498",
        "base_url": base_url,
        "user": account['user'],
        "password": account['password']
    }
}
