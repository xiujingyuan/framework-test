# -*- coding: utf-8 -*-
import json
import time

import requests

from foundation_test.util.http.http_util import Http


class Easymock(object):

    def __init__(self, user, password, project):
        self.token = ""
        self.project = project
        self.login(user, password)

    def login(self, user, password):
        url = "https://easy-mock.k8s-ingress-nginx.kuainiujinke.com/api/u/login"
        body = {"name": user,
                "password": password}
        header = {"Content-Type": "application/json"}
        resp = Http.http_post(url, body, header)
        self.token = "Bearer " + resp["data"]["token"]
        pass

    def get_api_list(self):
        url = "https://easy-mock.k8s-ingress-nginx.kuainiujinke.com/api/mock?project_id=" + \
              self.project + "&page_size=2000&page_index=1"
        header = {"Content-Type": "application/json",
                  "Authorization": self.token}
        # resp = Http.http_get(url, header)
        resp = requests.get(url, headers=header)
        return json.loads(resp.content)

    def get_api_info_by_api(self, api, method):
        api_list = self.get_api_list()
        api_info = {}
        if method:
            for mock in api_list["data"]["mocks"]:
                if mock["url"] == api and mock['method'] == method:
                    api_info["id"] = mock["_id"]
                    api_info["url"] = mock["url"]
                    api_info["method"] = mock["method"]
                    api_info["mode"] = ""
                    api_info["description"] = mock["description"]
                    break
            if len(api_info) == 0:
                raise Exception("未找到api")
            return api_info
        else:
            for mock in api_list["data"]["mocks"]:
                if mock["url"] == api:
                    api_info["id"] = mock["_id"]
                    api_info["url"] = mock["url"]
                    api_info["method"] = mock["method"]
                    api_info["mode"] = ""
                    api_info["description"] = mock["description"]
                    break
            if len(api_info) == 0:
                raise Exception("未找到api")
            return api_info

    def update(self, api, mode, method=None):
        """
        mode支持传入两种方式，json和str，传入json后内部会自己转为str
        :param api: 
        :param mode:
        :param method
        :return: 
        """
        api_info = self.get_api_info_by_api(api, method)
        url = "https://easy-mock.k8s-ingress-nginx.kuainiujinke.com/api/mock/update"
        header = {"Content-Type": "application/json;charset=UTF-8",
                  "Authorization": self.token}
        if isinstance(mode, str):
            api_info["mode"] = mode
        else:
            # api_info["mode"] = json.dumps(mode).encode('utf-8').decode('unicode_escape')
            api_info["mode"] = json.dumps(mode, ensure_ascii=False)
        # resp = Http.http_post(url, api_info, header)
        resp = requests.request(method='post', url=url, headers=header, json=api_info)
        return json.loads(resp.content)

    def create_project(self, project_id):
        api_list = self.get_api_list()
        for api in api_list["data"]["mocks"]:
            api_info = {"url": api["url"],
                        "method": api["method"],
                        "mode": api["mode"],
                        "description": api["description"],
                        "project_id": project_id}
            url = "https://easy-mock.k8s-ingress-nginx.kuainiujinke.com/api/mock/create"
            header = {"Content-Type": "application/json;charset=UTF-8",
                      "Authorization": self.token}
            Http.http_post(url, api_info, header)


if __name__ == "__main__":
    old_project = "5c221df2c2c04c0020a97fb1"
    new_project = "5de5d515d1784d36471d6041"
    easymock = Easymock('katherinewang', '123456', old_project)
    # params = {"message": "", "code": 2001, "data": ""}
    # easymock.update("/loan", json.dumps(params))
    # easymock.update("/loan", params)
    easymock.create_project(new_project)
