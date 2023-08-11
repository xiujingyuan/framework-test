#!/usr/bin/python
# -*- coding: UTF-8 -*-
from biztest.util.http.http_util import Http as http
import common.global_const as gc

dmp_conf = {
    "china": {
        "base_url": "http://yfrule.kuainiujinke.com",
        "workspace": "ws_loan_test",
        "project_name": "资方路由{}".format(gc.ENV),
        "project_id": "route",
        "third_api_no": "e6a4b2221b49496b9c7a022ec80dd732",
        "grouter_callback_url": "{}/factor/query".format(gc.GROUTER_URL)
    }
}


class DMP:
    third_api_update_url = "/api/third/api/update"
    package_publish_url = "/api/package/doPublish"

    header = {
        "x-app-key": "fe6a4a13c0af87f6b837f51e035de68d2c45cb5c",
        "x-request-way": "client",
        "Content-Type": "application/json"
    }

    def __init__(self, base_url, workspace):
        self.base_url = base_url
        self.workspace = workspace

    def update_third_api_url(self, api_no, api_url):
        body = {
            "workspaceCode": self.workspace,
            "apiName": "资方特征数据收集",
            "apiType": "http",
            "enable": True,
            "httpAction": {
                "apiContent": "资方特征收集",
                "apiUrl": api_url,
                "apiUse": "feature",
                "requestType": "2",
                "headerParams": [],
                "bodyParams": [
                    {
                        "paramEN": "businessId",
                        "paramCN": "null",
                        "desc": "路由请求标识",
                        "paramGetMethodName": "getFromRequest",
                        "paramType": "String",
                        "inputVal": "null",
                        "valueKey": "businessId",
                        "defaultValue": "",
                        "id": "businessId",
                        "value": "{\"paramGetMethodName\":\"getFromRequest\",\"paramType\":\"String\",\"inputVal\":\"null\",\"defaultValue\":\"\",\"valueKey\":\"businessId\"}",
                        "val": "来源于请求参数(参数类型:String)(映射键:businessId)(默认值:)"
                    },
                    {
                        "paramEN": "channelName",
                        "paramCN": "null",
                        "desc": "资方编码",
                        "paramGetMethodName": "getFromFacts",
                        "paramType": "String",
                        "inputVal": "null",
                        "valueKey": "facts.channelName",
                        "defaultValue": "",
                        "id": "channelName",
                        "value": "{\"paramGetMethodName\":\"getFromFacts\",\"paramType\":\"String\",\"inputVal\":\"null\",\"defaultValue\":\"\",\"valueKey\":\"facts.channelName\"}",
                        "val": "来源于事实对象(参数类型:String)(映射键:facts.channelName)(默认值:)"
                    },
                    {
                        "paramEN": "featureNames",
                        "paramCN": "null",
                        "desc": "特征名称",
                        "paramGetMethodName": "getDynamicParam",
                        "paramType": "String",
                        "inputVal": "null",
                        "valueKey": "featureNames",
                        "defaultValue": "",
                        "id": "featureNames",
                        "value": "{\"paramGetMethodName\":\"getDynamicParam\",\"paramType\":\"String\",\"inputVal\":\"null\",\"defaultValue\":\"\",\"valueKey\":\"featureNames\"}",
                        "val": "来源于变量选择(参数类型:String)(映射键:featureNames)(默认值:)"
                    },
                    {
                        "paramEN": "version",
                        "paramCN": "null",
                        "desc": "规则引擎版本",
                        "paramGetMethodName": "getDynamicParam",
                        "paramType": "String",
                        "inputVal": "null",
                        "valueKey": "version",
                        "defaultValue": "",
                        "id": "version",
                        "value": "{\"paramGetMethodName\":\"getDynamicParam\",\"paramType\":\"String\",\"inputVal\":\"null\",\"defaultValue\":\"\",\"valueKey\":\"version\"}",
                        "val": "来源于变量选择(参数类型:String)(映射键:version)(默认值:)"
                    }
                ]
            },
            "apiNo": api_no
        }
        http.http_post(self.base_url+self.third_api_update_url, body, self.header)

    def publish_package(self, project_id="route", project_name="资方路由"):
        body = {
            "workspaceCode": self.workspace,
            "refreshKnowledgeParams": [
                {
                    "fileId": project_id,
                    "projectName": project_name
                }
            ],
            "clientNames": [
                "localhost"
            ],
            "projectName": project_name,
            "remark": "1",
            "taskId": "taskId1624348011945"
        }
        http.http_post(self.base_url + self.package_publish_url, body, self.header)


def publish_dmp_package():
    """
    修改特征收集api并发布知识包
    :return:
    """
    dmp = DMP(dmp_conf[gc.COUNTRY]["base_url"], dmp_conf[gc.COUNTRY]["workspace"])
    dmp.update_third_api_url(dmp_conf[gc.COUNTRY]["third_api_no"], dmp_conf[gc.COUNTRY]["grouter_callback_url"])
    dmp.publish_package(dmp_conf[gc.COUNTRY]["project_id"], dmp_conf[gc.COUNTRY]["project_name"])


if __name__ == '__main__':
    gc.init_env(9, "china", "dev")
    publish_dmp_package()
