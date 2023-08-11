# -*- coding: utf-8 -*-
import json

from requests import HTTPError
from tenacity import retry, stop_after_attempt, wait_fixed
from biztest.util.log.log_util import LogUtil
import requests
import time


class Http(object):
    @classmethod
    @retry(stop=stop_after_attempt(5), wait=wait_fixed(2))
    def http_post(cls, url, req_data, headers=None, cookies=None):
        start = time.time()
        if headers is None:
            headers = {"Content-Type": "application/json", "Connection": "close",
                       "X-CALLBACK-TOKEN": "rZiLiUtn3rlqBU8a0PyZv5FyiCVcFObUmLu32noi5I6Exbd2"}
        resp = None
        try:
            if 'application/json' in str(headers).lower():
                resp = requests.post(url=url, json=req_data, headers=headers, cookies=cookies, timeout=150)
            elif 'application/x-www-form-urlencoded' in str(headers).lower():
                resp = requests.post(url=url, data=req_data, headers=headers, cookies=cookies, timeout=150)
        except Exception as e:
            LogUtil.log_info("http request error: %s" % e)
            resp = None
        if int(resp.status_code) not in (200, 201):
            LogUtil.log_info("请求报错，url:%s 返回的http_code:%s异常，返回body:%s，请检查" %
                             (url, resp.status_code, resp.content.decode('utf-8')))
            raise HTTPError
        try:
            resp_content = json.loads(resp.content)
        except Exception as e:
            print(e)
            resp_content = resp.content
        log_info = {"url": url,
                    "method": "post",
                    "request": req_data,
                    "response": resp_content,
                    "time": round(time.time() - start, 2)}
        LogUtil.log_info(log_info)
        return resp_content

    @classmethod
    @retry(stop=stop_after_attempt(5), wait=wait_fixed(2))
    def http_get(cls, url, headers=None, cookies=None, params=None):
        start = time.time()
        if headers is None:
            headers = {"Content-Type": "application/json", "Connection": "close"}
        try:
            resp = requests.get(url, params=params, headers=headers, cookies=cookies, timeout=150)
        except Exception as e:
            LogUtil.log_info("http request error: %s" % e)
            resp = None
        if int(resp.status_code) not in (200, 201):
            LogUtil.log_info("请求报错，url:%s 返回的http_code:%s异常，返回body:%s，请检查" %
                             (url, resp.status_code, resp.content.decode('utf-8')))
            raise HTTPError
        try:
            resp_content = json.loads(resp.content)
        except Exception as e:
            print(e)
            resp_content = resp.content
        log_info = {"url": url,
                    "method": "get",
                    "request": None,
                    "params": str(params),
                    "response": resp_content,
                    "time": round(time.time() - start, 2)}
        LogUtil.log_info(log_info)
        return resp_content

    @classmethod
    @retry(stop=stop_after_attempt(5), wait=wait_fixed(2))
    def http_put(cls, url, req_data, headers):
        start = time.time()
        if headers is None:
            headers = {"Content-Type": "application/json"}
        try:
            if 'application/json' in str(headers).lower():
                resp = requests.put(url=url, json=req_data, headers=headers, timeout=150)
            else:
                resp = requests.put(url=url, data=req_data, headers=headers, timeout=150)
        except Exception as e:
            LogUtil.log_info("http request error: %s" % e)
            resp = None
        if int(resp.status_code) not in (200, 201):
            LogUtil.log_info("请求报错，url:%s 返回的http_code:%s异常，返回body:%s，请检查" %
                             (url, resp.status_code, resp.content.decode('utf-8')))
            raise HTTPError
        log_info = {"url": url,
                    "method": "put",
                    "request": req_data,
                    "response": json.loads(resp.content),
                    "time": round(time.time() - start, 2)}
        LogUtil.log_info(log_info)
        return json.loads(resp.content)

    @classmethod
    @retry(stop=stop_after_attempt(5), wait=wait_fixed(2))
    def http_delete(cls, url, headers=None):
        start = time.time()
        if headers is None:
            headers = {"Content-Type": "application/json"}
        try:
            resp = requests.delete(url=url, headers=headers, timeout=150)
        except Exception as e:
            LogUtil.log_info("http request error: %s" % e)
            resp = None
        if int(resp.status_code) not in (200, 201):
            LogUtil.log_info("请求报错，url:%s 返回的http_code:%s异常，返回body:%s，请检查" %
                             (url, resp.status_code, resp.content.decode('utf-8')))
            raise HTTPError
        log_info = {"url": url,
                    "method": "delete",
                    "response": json.loads(resp.content),
                    "time": round(time.time() - start, 2)}
        LogUtil.log_info(log_info)
        return json.loads(resp.content)
