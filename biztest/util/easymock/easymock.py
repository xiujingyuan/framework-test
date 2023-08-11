# -*- coding: utf-8 -*-
import json
import re
import requests
from tenacity import retry, wait_fixed, stop_after_attempt

from biztest.util.http.http_util import Http
from biztest.util.log.log_util import LogUtil
from biztest.config.easymock.easymock_config import *


class Easymock(object):

    def __init__(self, project, check_req=True, return_req=False):
        """
        :param project: 项目名，easymock_config.mock_project的key
        :param check_req: bool，是否检查_req请求数据
        :param return_req:  bool，是否返回_req请求数据，返回到"origin_req"
        """
        self.token = ""
        self.project = project
        self.project_id = mock_project[project]['id']
        self.project_name = mock_project[project]['name']
        self.path_prefix = '/mock/{}/{}'.format(self.project_id, self.project_name)
        self.url = '{}{}'.format(mock_project[project]['base_url'], self.path_prefix)
        self.login(mock_project[project]['user'], mock_project[project]['password'])
        self.check_req = check_req
        self.return_req = return_req
        LogUtil.log_info("Easymock.__init__()...")

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
              self.project_id + "&page_size=2000&page_index=1"
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

    @retry(stop=stop_after_attempt(5), wait=wait_fixed(2))
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
        if self.return_req:
            api_info["mode"] = self.append_origin_req(api_info["mode"])
        resp = requests.request(method='post', url=url, headers=header, json=api_info)
        return json.loads(resp.content)

    @retry(stop=stop_after_attempt(5), wait=wait_fixed(2))
    def update_by_api_id(self, api_id, api, mode, method="post"):
        api_list = self.get_api_list()
        api_info = {}
        for mock in api_list["data"]["mocks"]:
            if mock["_id"] == api_id and mock['method'] == method:
                api_info["id"] = api_id
                api_info["url"] = api
                api_info["method"] = mock["method"]
                api_info["mode"] = ""
                api_info["description"] = mock["description"]
                break
        if len(api_info) == 0:
            raise Exception("未找到api")

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
            api_info = {"url": "" + api["url"],
                        "method": api["method"],
                        "mode": api["mode"],
                        "description": api["description"],
                        "project_id": project_id}
            url = "https://easy-mock.k8s-ingress-nginx.kuainiujinke.com/api/mock/create"
            header = {"Content-Type": "application/json;charset=UTF-8",
                      "Authorization": self.token}
            Http.http_post(url, api_info, header)

    def append_origin_req(self, data):
        """
        把最后一个'}'替换成追加了_req数据的串
        :param data:
        :return:
        """
        req_data = ', "origin_req":{' \
                   '"_req.url":function({_req}){return _req.url},' \
                   '"_req.path":function({_req}){return _req.path},' \
                   '"_req.body":function({_req}){return _req.body},' \
                   '"_req.query":function({_req}){return _req.query}' \
                   '}}'
        replace_reg = re.compile("\\}$")
        data = replace_reg.sub(req_data, data)
        return data

    @staticmethod
    def get_str_by_type(key):
        if type(key) == str:
            ret_key = '"%s"' % key
        else:
            ret_key = key
        return ret_key

    def get_mock_result_with_check(self, origin_data, check_point_dict):
        """
        带检查点的mock结果
        :param origin_data: 正常的响应数据
        :param check_point_dict: 检查点
         - GET请求，推荐检查 path + query；
         - POST请求，推荐检查 path + body；
        eg.
        {
            "path": "/mock/5f9bfaf562081c0020d7f5a7/gbiz/tongrongmiyang/tongrongmiyang/loanApply",
            "body": {
                "loanOrder.termNo": 6,
                "loanOrder.account": "4000.00"
            },
            "query": {
                "loanOrder.termNo": 6,
                "loanOrder.account": "4000.00"
            }
        }
        :return: 需要检查请求参数时，返回带检查点的响应式mock结果；无需检查请求参数时，返回原始数据
        """
        # 需要检查_req参数，组装function
        if self.check_req:
            demo = """function({_req}) {
                    if (%s) {
                      return %s
                    } else {
                      return "REQ_CHECK_FAILED: %s"
                    }
                  }"""
            if_condition = "true"
            fail_message = ""
            for k, v in check_point_dict.items():
                if type(v) == str:
                    if_condition += " && _req.%s === %s" % (k, self.get_str_by_type(v))
                    fail_message += "%s: expect[%s], actual[\" + %s + \"]; " % (k, v, "_req.%s" % (k))
                elif type(v) == dict:
                    for key, value in v.items():
                        if_condition += " && _req.%s.%s === %s" % (k, key, self.get_str_by_type(value))
                        fail_message += "%s.%s: expect[%s], actual[\" + %s + \"]; " % (
                            k, key, value, "_req.%s.%s" % (k, key))
            result = demo % (
                if_condition, origin_data if isinstance(origin_data, int) else self.get_str_by_type(origin_data),
                fail_message)
            return result
        # 不需要检查_req，返回原始数据
        else:
            return self.get_str_by_type(origin_data)


if __name__ == "__main__":
    # old_project = "5caeea78c2c04c0020a98498"
    new_project = "5bd800c7b820c00016b21ddb"
    easymock = Easymock("old_dcs_auto_test")
    check_point = {
        "path": "/mock/5f9bfaf562081c0020d7f5a7/gbiz/tongrongmiyang/tongrongmiyang/loanApply",
        "body": {
            "loanOrder.termNo": 6,
            "loanOrder.account": "4000.00"
        },
        "query": {
            "loanOrder.termNo": 6,
            "loanOrder.account": "4000.00"
        }
    }
    mock_result = easymock.get_mock_result_with_check(200, check_point)
    print(mock_result)
    params = {"message": "", "code": 2001, "data": ""}
    easymock.update("/loan", json.dumps(params))
    easymock.update("/loan", params)
    easymock.create_project(new_project)
