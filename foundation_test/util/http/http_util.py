# -*- coding: utf-8 -*-
import json

from requests import HTTPError

from foundation_test.util.log.log_util import LogUtil
import requests


class Http(object):
    @classmethod
    def http_post(cls, url, req_data, headers=None, cookies=None):
        if headers is None:
            headers = {"Content-Type": "application/json", "Connection": "close"}
        resp = None
        try:
            if 'application/json' in str(headers).lower():
                resp = requests.post(url=url, json=req_data, headers=headers, cookies=cookies, timeout=150)
                print(url, json.dumps(req_data), resp.content)
            elif 'application/x-www-form-urlencoded' in str(headers).lower():
                resp = requests.post(url=url, data=req_data, headers=headers, cookies=cookies, timeout=150)
                print(resp)
        except Exception as e:
            LogUtil.log_error("http request error: %s" % e)
            resp = None
        if int(resp.status_code) not in (200, 201):
            LogUtil.log_info("请求报错，url:%s 返回的http_code:%s异常，返回body:%s，请检查" %
                             (url, resp.status_code, resp.content.decode('utf-8')))
            raise HTTPError
        try:
            resp_content = json.loads(resp.text)
        except Exception as e:
            print(e)
            resp_content = resp.text
        log_info = {"url": url,
                    "method": "post",
                    "request": req_data,
                    "response": resp_content
                    }
        LogUtil.log_debug(log_info)
        return resp_content

    @classmethod
    def http_get(cls, url, headers=None, cookies=None):
        if headers is None:
            headers = {"Content-Type": "application/json", "Connection": "close"}
        try:
            resp = requests.get(url, headers=headers, cookies=cookies, timeout=500)
        except Exception as e:
            LogUtil.log_error("http request error: %s" % e)
            resp = None
        if int(resp.status_code) not in (200, 201):
            LogUtil.log_info("请求报错，url:%s 返回的http_code:%s异常，返回body:%s，请检查" %
                             (url, resp.status_code, resp.content.decode('utf-8')))
            raise HTTPError
        try:
            resp_content = json.loads(resp.text)
        except Exception as e:
            print(e)
            resp_content = resp.text
        log_info = {"url": url,
                    "method": "get",
                    "request": None,
                    "response": resp_content
                    }
        LogUtil.log_debug(log_info)
        return resp_content

    @classmethod
    def http_put(cls, url, req_data, headers):
        if headers is None:
            headers = {"Content-Type": "application/json"}
        try:
            if 'application/json' in str(headers).lower():
                resp = requests.put(url=url, json=req_data, headers=headers, timeout=150)
            else:
                resp = requests.put(url=url, data=req_data, headers=headers, timeout=150)
        except Exception as e:
            LogUtil.log_error("http request error: %s" % e)
            resp = None
        try:
            resp_content = json.loads(resp.text)
        except Exception as e:
            print(e)
            resp_content = resp.text
        log_info = {"url": url,
                    "method": "put",
                    "request": req_data,
                    "response": resp_content
                    }
        LogUtil.log_debug(log_info)
        return resp_content
