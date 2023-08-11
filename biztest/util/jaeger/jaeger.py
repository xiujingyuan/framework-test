#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests
from biztest.util.log.log_util import LogUtil
from tenacity import retry, wait_fixed, stop_after_attempt
import common.global_const as gc


class Jaeger():
    def __init__(self, service):
        self.service = service
        self.base_url = gc.JAEGER_URL

    @retry(stop=stop_after_attempt(10), wait=wait_fixed(3))
    def get_request_log(self, order_no, operation, child_operation_lt):
        """
        从jaeger获取请求日志
        :param order_no: 资产编号
        :param operation: 业务节点
        :param child_operation_lt: 子业务节点list
        :return: 请求日志json：
        {
            '子业务节点1': {
                'http_status_code': 200,
                'http_path': '',
                'http_url': '',
                'http_method': ''
                'feign_request': '',
                'feign_response': ''
            },
            ...
        }
        """
        ret_data_dt = {}
        uri = "/api/traces"
        params = {
            "service": self.service,
            "operation": operation,
            "tags": "{\"orderNo\": \"%s\"}" % order_no,
            "limit": 20,
            "lookback": "1h",
        }
        resp = requests.get(self.base_url + uri, params=params).json()
        LogUtil.log_info("jaeger log: %s" % resp)
        spans = resp['data'][0]['spans']
        filtered_spans = [x for x in spans if x['operationName'] in child_operation_lt]
        for span in filtered_spans:
            req_dt = {}
            for tag in span['tags']:
                req_dt[tag['key'].replace('.', '_')] = tag['value']
            for log in span['logs']:
                req_dt[log['fields'][0]['key'].replace('.', '_')] = log['fields'][0]['value']
            ret_data_dt[span['operationName']] = req_dt
        LogUtil.log_info("filtered jaeger log: %s" % ret_data_dt)
        return ret_data_dt


if __name__ == '__main__':
    jaeger = Jaeger('gbiz2')
    item_no = '20201615199893138638'
    req = jaeger.get_request_log(item_no, 'LoanApplyNew', ['/mock/5f9bfaf562081c0020d7f5a7/gbiz/tongrongmiyang/tongrongmiyang/loanApply'])
    print(item_no, 'LoanApplyNew', req)
    req = jaeger.get_request_log(item_no, 'LoanApplyQuery', ['/mock/5f9bfaf562081c0020d7f5a7/gbiz/tongrongmiyang/tongrongmiyang/loanApplyQuery'])
    print(item_no, 'LoanApplyQuery', req)
    req = jaeger.get_request_log(item_no, 'PaymentWithdraw',
                                 ['//mock/5f9bfaf562081c0020d7f5a7/gbiz/withdraw/balance',
                                  '//mock/5f9bfaf562081c0020d7f5a7/gbiz/withdraw/autoWithdraw'])
    print(item_no, 'PaymentWithdraw', req)
    req = jaeger.get_request_log(item_no, 'PaymentWithdraw', ['/mock/5f9bfaf562081c0020d7f5a7/gbiz/withdraw/autoWithdraw'])
    print(item_no, 'PaymentWithdraw', req)
