# -*- coding: utf-8 -*-
import json
import time
import requests

from biztest.util.tools.tools import parse_resp_body
from biztest.util.http.http_util import Http


class Nacos(object):
    def __init__(self, domain, username="nacos", password="bizadmin0504"):
        self.username = username
        self.password = password

        self.domain = domain
        self.cookies = None
        self.authorization = None

        self.content = None
        self.type = type

        self.login()

    def login(self):
        url = "https://{0}/nacos/v1/auth/login".format(self.domain)
        req_body = {
            "username": self.username,
            "password": self.password,
            "namespaceId": ""
        }
        resp = parse_resp_body(
            requests.request(method='post', url=url,
                             headers={"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"},
                             data=req_body))
        response_headers = resp["headers"]
        self.authorization = response_headers["Authorization"]
        self.cookies = resp["cookies"]

    def get_configs_id(self, tenant, data_id):
        url = "https://%s/nacos/v1/cs/configs?search=accurate&dataId=%s&group=&appName=&config_tags=" \
              "&pageNo=1&pageSize=10&tenant=%s&namespaceId=%s" % (self.domain, data_id, tenant, tenant)
        resp = parse_resp_body(
            requests.request(method='get', url=url,
                             headers={"Authorization": self.authorization},
                             cookies=self.cookies))
        configs_id = resp["content"]["pageItems"][0]["id"]
        return configs_id
        # resp = Http.http_get(url, headers={"Authorization": self.authorization}, cookies=self.cookies)
        # configs_id = resp["pageItems"][0]["id"]
        # return configs_id

    def update_configs(self, tenant, data_id, content, group="KV", types="json"):
        configs_id = self.get_configs_id(tenant, data_id)
        url = "https://%s/nacos/v1/cs/configs" % self.domain
        if types == "json":
            content = json.dumps(content, ensure_ascii=False)
        req_body = {
            "dataId": data_id,
            "group": group,
            "content": content,
            "appName": None,
            "desc": None,
            "config_tags": None,
            "tenant": tenant,
            "createTime": "1581592882000",
            "modifyTime": "1581592882000",
            "createUser": None,
            "createIp": "118.242.27.98",
            "use": None,
            "effect": None,
            "schema": None,
            "configTags": None,
            "md5": "be65d4de7d98e9877adbfd2416069e05",
            "id": configs_id,
            "type": types,
        }
        Http.http_post(url, req_body,
                       headers={"content-type": "application/x-www-form-urlencoded",
                                "Authorization": self.authorization},
                       cookies=self.cookies)
        time.sleep(0.5)

    def get_configs(self, tenant, data_id):
        url = "https://{0}/nacos/v1/cs/configs?search=accurate&dataId={1}&group=&appName=&config_tags=" \
              "&pageNo=1&pageSize=10&tenant={2}&namespaceId={2}".format(self.domain, data_id, tenant)
        resp = parse_resp_body(
            requests.request(method='get', url=url,
                             headers={"Authorization": self.authorization},
                             cookies=self.cookies))
        # configs_content = resp["content"]
        configs_content = resp["content"]["pageItems"][0]["content"]
        return configs_content

    def get_config(self, tenant, group, data_id):
        url = "https://{0}/nacos/v1/cs/configs".format(self.domain)
        headers = {"Authorization": self.authorization}
        params = {
            "dataId": data_id,
            "group": group,
            "namespaceId": tenant,
            "tenant": tenant,
            "show": "all"
        }
        resp = requests.get(url, params=params, headers=headers, cookies=self.cookies)
        return resp.json()

    def incremental_update_config(self, tenant, data_id, group, **kwargs):
        config = self.get_config(tenant, group, data_id)
        if config['type'] == "json":
            content = json.loads(config['content'])
            for key, value in kwargs.items():
                content[key] = value
        else:
            # TODO:其他类型增量更新config
            content = config['content']
        self.update_configs(tenant, data_id, content, group)


if __name__ == "__main__":
    nacos = Nacos("nacos.k8s-ingress-nginx.kuainiujinke.com")
    nacos.update_configs("grant%s" % 2, "gbiz_mq_config", {"available": False})
