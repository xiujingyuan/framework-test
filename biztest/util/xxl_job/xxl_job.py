# -*- coding: utf-8 -*-
import json

import requests

from biztest.config.rbiz.url_config import xxl_job_url, global_xxl_job_new_url, global_taiguo_xxl_job_url, \
    global_yindu_xxl_job_url, \
    xxl_job_url_k8s, global_phl_xxl_job_url
from biztest.util.tools.tools import parse_resp_body


class XxlJob:

    def __init__(self, job_group, executor_handler, user_name="admin", password="MTIzNDU2", xxl_job_type="xxl_job"):
        self.user_name = user_name
        self.password = password
        self.cookie = None
        self.job_group = int(job_group)
        self.executorHandler = executor_handler
        self.base_url = None
        self.type = xxl_job_type
        self.get_url()
        self.login()

    def get_url(self):
        if self.type == 'xxl_job':
            self.base_url = xxl_job_url
        elif self.type == "xxl_job_k8s":
            self.base_url = xxl_job_url_k8s
        elif self.type == "global_yindu_xxl_job":
            self.base_url = global_yindu_xxl_job_url
        elif self.type == "global_taiguo_xxl_job":
            self.base_url = global_taiguo_xxl_job_url
        elif self.type == "global_phl_xxl_job":
            self.base_url = global_phl_xxl_job_url
        elif self.type == "global_xxl_job_new":
            self.base_url = global_xxl_job_new_url

    def login(self):
        url = self.base_url + "/login"
        req_body = {
            "userName": self.user_name,
            "password": self.password
        }
        resp = parse_resp_body(
            requests.request(method='post', url=url, headers={"content-type": "application/x-www-form-urlencoded"},
                             data=req_body))
        self.cookie = resp["cookies"]

    def get_page_list(self):
        url = self.base_url + "/jobinfo/pageList"
        req_body = {
            "jobDesc": "",
            "jobGroup": self.job_group,
            "executorHandler": "",
            "jobAuthor": "",
            "jobParam": "",
            "shCommand": "",
            "systemName": "",
            "triggerStatus": -1,
            "start": 0,
            "length": 200
        }
        resp = parse_resp_body(
            requests.request(method='post', url=url, headers={"content-type": "application/x-www-form-urlencoded"},
                             data=req_body, cookies=self.cookie))
        return resp

    def get_job_info(self):
        page_list = self.get_page_list()['content']['data']
        job_info = None
        for page in page_list:
            if page["executorHandler"] == self.executorHandler:
                job_info = page
                break
        return job_info

    def trigger_job(self, executor_param=None):
        url = self.base_url + "/jobinfo/trigger"
        job_info = self.get_job_info()
        if job_info is None:
            raise Exception("没有查询到对应的executorHandler")
        if executor_param is not None and len(executor_param) > 0:
            if isinstance(executor_param, str):
                job_info["executorParam"] = executor_param
            else:
                job_info["executorParam"] = json.dumps(executor_param, ensure_ascii=False)
        req_body = {
            "id": job_info["id"],
            "executorParam": job_info["executorParam"]
        }
        resp = parse_resp_body(
            requests.request(method='post', url=url, headers={"content-type": "application/x-www-form-urlencoded"},
                             data=req_body, cookies=self.cookie))
        if resp['content']["code"] != 200:
            raise Exception("触发job失败")

    def update_job(self, executor_param):
        url = self.base_url + "/jobinfo/update"
        job_info = self.get_job_info()
        if job_info is None:
            raise Exception("没有查询到对应的executorHandler")
        if isinstance(executor_param, str):
            job_info["executorParam"] = executor_param
        else:
            job_info["executorParam"] = json.dumps(executor_param, ensure_ascii=False)

        if self.type == "xxl_job" or self.type == "global_yindu_xxl_job":
            update_job_info = {"id": job_info["id"],
                               "jobCron": job_info["jobCron"],
                               "jobDesc": job_info["jobDesc"],
                               "author": job_info["author"],
                               "notification": job_info["notification"],
                               "executorRouteStrategy": job_info["executorRouteStrategy"],
                               "executorHandler": job_info["executorHandler"],
                               "executorParam": job_info["executorParam"],
                               "executorBlockStrategy": job_info["executorBlockStrategy"],
                               "executorFailStrategy": job_info["executorFailStrategy"],
                               "sliceTotal": job_info["sliceTotal"],
                               "systemName": job_info["systemName"]}
            resp = parse_resp_body(
                requests.request(method='post', url=url, headers={"content-type": "application/json"},
                                 json=update_job_info, cookies=self.cookie))
            print("a")
        else:
            update_job_info = {
                "id": job_info["id"],
                "jobCron": job_info["jobCron"],
                "cronGen_display": job_info["jobCron"],
                "jobDesc": job_info["jobDesc"],
                "jobGroup": job_info["jobGroup"],
                "author": job_info["author"],
                "alarmEmail": job_info["alarmEmail"],
                "executorRouteStrategy": job_info["executorRouteStrategy"],
                "executorHandler": job_info["executorHandler"],
                "executorParam": job_info["executorParam"],
                "executorBlockStrategy": job_info["executorBlockStrategy"],
                "executorFailRetryCount": job_info["executorFailRetryCount"],
                "executorTimeout": job_info["executorTimeout"],
                "sliceTotal": job_info["sliceTotal"]}
            resp = parse_resp_body(
                requests.request(method='post', url=url, headers={"content-type": "application/x-www-form-urlencoded"},
                                 data=update_job_info, cookies=self.cookie))
            print("b")
        if resp['content']["code"] != 200:
            raise Exception("更新job失败")

    def trigger_job_for_id(self, job_id, job_param):
        url = self.base_url + "/jobinfo/trigger"
        req_body = {
            "id": job_id,
            "executorParam": job_param
        }
        resp = parse_resp_body(
            requests.request(method='post', url=url, headers={"content-type": "application/x-www-form-urlencoded"},
                             data=req_body, cookies=self.cookie))
        if resp['content']["code"] != 200:
            raise Exception("触发job失败")

    # def get_jobs_by_group(self):
    #     url = self.base_url["get_jobs_by_group"]
    #     req_body = {
    #         "jobGroup": self.job_group
    #     }
    #     resp = parse_resp_body(
    #         requests.request(method='post', url=url, headers={"content-type": "application/x-www-form-urlencoded"},
    #                          data=req_body, cookies=self.cookie))
    #     return resp
    #
    #
    # def get_job_id_by_group_id(self):
    #     jobs_list = self.get_jobs_by_group()['content']['content']
    #     job_id = 0
    #     job_param = ""
    #     for job in jobs_list:
    #         if job["executorHandler"] == self.executorHandler:
    #             job_id = job["id"]
    #             job_param = job["executorParam"]
    #             break
    #     return job_id, job_param
    #
    #
    # def trigger_job_global(self):
    #     url = self.base_url["trigger"]
    #     id, job_param = self.get_job_id_by_group_id()
    #     if id == 0:
    #         raise Exception("没有查询到对应的executorHandler")
    #     req_body = {
    #         "id": id,
    #         "executorParam": job_param
    #     }
    #     resp = parse_resp_body(
    #         requests.request(method='post', url=url, headers={"content-type": "application/x-www-form-urlencoded"},
    #                          data=req_body, cookies=self.cookie))
    #     if resp['content']["code"] != 200:
    #         raise Exception("触发job失败")


if __name__ == '__main__':
    xxl_job = XxlJob(54, "refreshLateFeeV1", xxl_job_type="xxl_job")
    xxl_job.trigger_job()
    xxl_job = XxlJob(2, "withholdAutoV1", xxl_job_type="global_yindu_xxl_job")
    xxl_job.trigger_job()
    xxl_job.update_job("xxx")
    xxl_job = XxlJob(2, "withholdAutoV1", password="123456", xxl_job_type="global_xxl_job_new")
    xxl_job.trigger_job("xxxx")
    xxl_job.update_job("xxxx")
