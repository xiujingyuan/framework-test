# -*- coding: utf-8 -*-
import json
import os

import requests

from biztest.config.rbiz.url_config import xxl_job_url, global_xxl_job_new_url, global_taiguo_xxl_job_url, \
    global_yindu_xxl_job_url, \
    xxl_job_url_k8s, XXL_JOB_DICT
from biztest.util.tools.tools import parse_resp_body

HEADERS = {"content-type": "application/x-www-form-urlencoded"}
HEADERS_JSON = {"content-type": "application/json"}


class XxlJobNew(object):

    def __init__(self, xxl_job_type):
        self.user_name = XXL_JOB_DICT[xxl_job_type]['username']
        self.password = XXL_JOB_DICT[xxl_job_type]['password']
        self.cookie = None
        self.base_url = XXL_JOB_DICT[xxl_job_type]['url']
        self.type = xxl_job_type
        self.login_url = os.path.join(self.base_url, 'login')
        self.page_list_url = os.path.join(self.base_url, 'jobinfo/pageList')
        self.trigger_url = os.path.join(self.base_url, 'jobinfo/trigger')
        self.update_url = os.path.join(self.base_url, 'jobinfo/update')

    def login(self):
        req_body = {
            "userName": self.user_name,
            "password": self.password
        }
        resp = parse_resp_body(
            requests.request(method='post', url=self.login_url, headers=HEADERS, data=req_body))
        self.cookie = resp["cookies"]

    def get_page_list(self, job_group):
        req_body = {
            "jobDesc": "",
            "jobGroup": job_group,
            "executorHandler": "",
            "jobAuthor": "",
            "jobParam": "",
            "shCommand": "",
            "systemName": "",
            "triggerStatus": -1,
            "start": 0,
            "length": 200
        }
        resp = parse_resp_body(requests.request(method='post', url=self.page_list_url, headers=HEADERS, data=req_body,
                                                cookies=self.cookie))
        return resp

    def get_job_info(self, job_group, executor_handler):
        page_list = self.get_page_list(job_group)['content']['data']
        for page in page_list:
            if page["executorHandler"] == executor_handler:
                return page
        return None

    def trigger_job(self, job_group, executor_handler, executor_param=None):
        self.login()
        job_info = self.get_job_info(job_group, executor_handler)
        if job_info is None:
            raise Exception("没有查询到对应的executorHandler")
        if executor_param is not None and executor_param:
            job_info["executorParam"] = executor_param if isinstance(executor_param, str) \
                else json.dumps(executor_param, ensure_ascii=False)
        req_body = {
            "id": job_info["id"],
            "executorParam": job_info["executorParam"]
        }
        resp = parse_resp_body(
            requests.request(method='post', url=self.trigger_url, headers=HEADERS, data=req_body, cookies=self.cookie))
        if resp['content']["code"] != 200:
            raise Exception("触发job失败")

    def update_job(self, job_group, executor_handler, executor_param):
        self.login()
        job_info = self.get_job_info(job_group, executor_handler)
        if job_info is None:
            raise Exception("没有查询到对应的executorHandler")
        job_info["executorParam"] = executor_param if isinstance(executor_param, str) else \
            json.dumps(executor_param, ensure_ascii=False)
        update_job_info, header = self.get_job_info_dict(job_info)
        resp = parse_resp_body(requests.request(method='post', url=self.update_url, headers=header,
                                                data=update_job_info, cookies=self.cookie))
        if resp['content']["code"] != 200:
            raise Exception("更新job失败")

    def get_job_info_dict(self, job_info):
        update_job_info, header = {
            "id": job_info["id"],
            "jobCron": job_info["jobCron"],
            "jobDesc": job_info["jobDesc"],
            "author": job_info["author"],
            "executorRouteStrategy": job_info["executorRouteStrategy"],
            "executorHandler": job_info["executorHandler"],
            "executorParam": job_info["executorParam"],
            "executorBlockStrategy": job_info["executorBlockStrategy"],
            "sliceTotal": job_info["sliceTotal"]
        }, HEADERS
        if self.type in ('xxl_job', 'global_yindu_xxl_job'):
            update_job_info["notification"] = job_info["notification"]
            update_job_info["executorFailStrategy"] = job_info["executorFailStrategy"]
            update_job_info["systemName"] = job_info["systemName"]
            header = HEADERS_JSON
        else:
            update_job_info["cronGen_display"] = job_info["jobCron"]
            update_job_info["jobGroup"] = job_info["jobGroup"]
            update_job_info["alarmEmail"] = job_info["alarmEmail"]
            update_job_info["executorFailRetryCount"] = job_info["executorFailRetryCount"]
            update_job_info["executorTimeout"] = job_info["executorTimeout"]
        return update_job_info, header

    def trigger_job_for_id(self, job_id, job_param):
        self.login()
        req_body = {
            "id": job_id,
            "executorParam": job_param
        }
        resp = parse_resp_body(requests.request(method='post', url=self.trigger_url, headers=HEADERS,
                                                data=req_body, cookies=self.cookie))
        if resp['content']["code"] != 200:
            raise Exception("触发job失败")


if __name__ == '__main__':
    pass
