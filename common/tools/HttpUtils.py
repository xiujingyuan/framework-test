# -*- coding: utf-8 -*-
# @Time    : 公元18-11-27 上午9:34
# @Author  : 张廷利
# @Site    :
# @File    : HttpUtils.py
# @Software: IntelliJ IDEA

import json
import requests
import allure
from common.tools.BaseUtils import BaseUtils
from framework.dao.FrameworkDAO import FrameworkDAO

class HttpUtils(object):

    def __init__(self):
        self.fdao = FrameworkDAO()



    def http_post(self,url,req_data,mock_flag="N",case_id=None,headers=None):
        '''
            迁移的老版本的对api 访问功能方法
        :param url:
        :param req_data:
        :param headers:
        :return:
        '''
        # 如果是mock ，直接获取表中预留的mock 做为http 返回。
        if mock_flag =="Y":
            return self.http_mock_response(case_id)

        else:
            headers = BaseUtils.transfer_string_to_dict(headers)
            if 'application/x-www-form-urlencoded' in str(headers) \
                    or 'form-data' in str(headers):
                #该Content-Type下post参数data需接受字典类型
                if req_data is not None and req_data!="":
                    req_data = eval(req_data.replace("false", "0").replace("true", "1"))
            else:
                req_data = BaseUtils.transfer_dict_to_string(req_data)
            if 'application/json' in str(headers).lower():
                data = BaseUtils.transfer_string_to_dict(req_data)
                rsp = requests.post(url=url, json=data, headers=headers, timeout=150)
            elif 'multipart/form-data' in str(headers).lower():
                for key in headers:
                    if key.lower() == "content-type":
                        headers[key] += ";boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW"
                        break


                payload = """------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data;"""
                for index, item in enumerate(req_data):
                    req_data_value = req_data[item] if isinstance(req_data[item], str) else req_data[item]
                    # print(item, req_data_value, type(req_data_value))
                    if index == len(req_data) - 1:

                        payload += """  name=\"{0}\"\r\n\r\n {1}\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--""".format(item,req_data_value )
                    else:
                        payload += """  name=\"{0}\"\n\n{1}\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; """.format(item, req_data_value)
                print(payload, type(payload))
                rsp = requests.post(url, headers=headers, data=payload)

            else:
                rsp = requests.post(url=url, data=req_data, headers=headers, timeout=150)

            if rsp is not None:
                rsp_result = rsp.content
            else:
                rsp_result = None
            return rsp_result

    def http_get(self,url,mock_flag="N",case_id=None,headers=None):
        '''
            迁移老版本API访问封装。
        :param url:
        :return:
        '''
        # 如果是mock ，直接获取表中预留的mock 做为http 返回。
        if mock_flag =="Y":
            return self.http_mock_response(case_id)

        else:
            headers = BaseUtils.transfer_string_to_dict(headers)
            rsp = requests.get(url,headers=headers)
            return rsp.content


    def http_put(self,url,req_data,headers,mock_flag="N",case_id=None):
        '''
            迁移的老版本的对api 访问功能方法
        :param url:
        :param req_data:
        :param headers:
        :return:
        '''
        # 如果是mock ，直接获取表中预留的mock 做为http 返回。
        if mock_flag =="Y":
            return self.http_mock_response(case_id)

        else:
            headers = BaseUtils.transfer_string_to_dict(headers)
            if 'application/x-www-form-urlencoded' in str(headers) \
                    or 'form-data' in str(headers):
                #该Content-Type下post参数data需接受字典类型
                if req_data is not None and req_data!="":
                    req_data = eval(req_data)
            else:
                req_data = BaseUtils.transfer_dict_to_string(req_data)
            if 'application/json' in str(headers).lower():
                data = BaseUtils.transfer_string_to_dict(req_data)
                rsp = requests.put(url=url, json=data, headers=headers, timeout=150)
            else:
                rsp = requests.put(url=url, data=req_data, headers=headers, timeout=150)
            if rsp is not None:
                rsp_result = rsp.content
            else:
                rsp_result = None
            return rsp_result

    def http_delete(self,url,req_data,headers,mock_flag="N",case_id=None):
        '''
            迁移的老版本的对api 访问功能方法
        :param url:
        :param req_data:
        :param headers:
        :return:
        '''
        # 如果是mock ，直接获取表中预留的mock 做为http 返回。
        if  mock_flag =="Y":
            return self.http_mock_response(case_id)

        else:
            headers = BaseUtils.transfer_string_to_dict(headers)
            if 'application/x-www-form-urlencoded' in str(headers) \
                    or 'form-data' in str(headers):
                #该Content-Type下post参数data需接受字典类型
                if req_data is not None and req_data!="":
                    req_data = eval(req_data)
            else:
                req_data = BaseUtils.transfer_dict_to_string(req_data)
            if 'application/json' in str(headers).lower():
                data = BaseUtils.transfer_string_to_dict(req_data)
                rsp = requests.delete(url=url, json=data, headers=headers, timeout=150)
            else:
                rsp = requests.delete(url=url, data=req_data, headers=headers, timeout=150)
            if rsp is not None:
                rsp_result = rsp.content
            else:
                rsp_result = None
            return rsp_result








    def http_request(self,url,req_data,method,headers,mock_flag="N",case_id=0):
        result = None
        if method is not None and method.upper() == 'POST':
            result = self.http_post(url,req_data,mock_flag,case_id,headers)
        elif method is not None and method.upper() == 'GET':
            result = self.http_get(url,mock_flag,case_id,headers)
        elif method is not None and method.upper() =="PUT":
            result = self.http_put(url,req_data,headers,mock_flag,case_id)
        elif method is not None and method.upper() =="DELETE":
            result = self.http_delete(url,req_data,headers,mock_flag,case_id)
        else:
            result = self.http_post(url,req_data,mock_flag,case_id,headers)
        return result



    def http_mock_response(self,case_id):
        response = self.fdao.get_case_mock_response(case_id)
        if response is not None:
            return response.mock_response





