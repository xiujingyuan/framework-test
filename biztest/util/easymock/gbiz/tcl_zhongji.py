# -*- coding: utf-8 -*-
from biztest.function.cmdb.cmdb_common_function import get_fee_info_by_period
from biztest.interface.cmdb.cmdb_interface import cmdb_rate_loan_calculate_v6
from biztest.util.easymock.easymock import Easymock
from copy import deepcopy
from biztest.util.tools.tools import *
import hashlib
import calendar;
import time;


class TclZhongjiMock(Easymock):

    def get_hashmdt(self, item):
        md5 = hashlib.md5()
        md5.update(item.encode('utf-8'))
        str_md5 = md5.hexdigest()
        return str_md5

    def update_creditapply(self, itemNo, retCode='000000', status='01'):
        api = "/tcl/tcl_zhongji/S010001C"
        mode = {
            "code": 0,
            "message": "success",
            "data": {
                "header": {
                    "retCode": retCode,
                    "retMsg": "成功",
                    "reqNo": "e2c8f11a90b64670bf53954dd02cad13"
                },
                "data": {
                    "message": None,
                    "status": status,
                    "applyNo": self.get_hashmdt('C' + str(itemNo)),
                    "step": None,
                    "success": True
                }
            }
        }
        self.update(api, mode)

    def update_creditapply_query(self, itemno, retCode='000000', status='01'):
        api = "/tcl/tcl_zhongji/S010001Q"
        mode = {"code": 0,
                "message": "success",
                "data": {
                    "header": {
                        "retCode": retCode,
                        "retMsg": "成功",
                        "reqNo": "f5c2b1d8926a4f1e96c7e5b3f1e8dd59"
                    },
                    "data": {
                        "status": status,
                        "url": None,
                        "applyNo": self.get_hashmdt('C' + str(itemno)),
                        "sendResult": None,
                        "contractNo": None,
                        "failReason": None,
                        "step": None,
                        "creditAmt": None
                    }
                }}
        self.update(api, mode)

    def update_no_order(self):
        api = '/tcl/tcl_zhongji/S010001Q'
        body = {"code": 0,
                "message": "success",
                "data": {
                    "header": {
                        "retCode": "100002",
                        "retMsg": "未查询到相关授信数据",
                        "reqNo": "6bae361c7e29433fb835d8cbaf2b23b0"
                    },
                    "data": {}
                }}
        self.update(api, body)

    def update_loan_apply(self, itemno, retCode='000000', status=3):
        api = "/tcl/tcl_zhongji/S012007C"
        mode = {"code": 0,
                "message": "success",
                "data": {
                    "header": {
                        "retCode": retCode,
                        "retMsg": "成功",
                        "reqNo": "9438215bc9d14f649d82e828ea89fcea"
                    },
                    "data": {
                        # "putoutNo": "5282e9c87b1345cfa7bcc9a53721d5bd",
                        "putoutNo": self.get_hashmdt(itemno),
                        "status": status,
                        "errMsg": None,
                        "fileId": None
                    }
                }}
        self.update(api, mode)

    def update_loan_query(self, itemno, asset_info, retCode='000000', status=1):
        api = "/tcl/tcl_zhongji/S012002Q"
        rate_info = cmdb_rate_loan_calculate_v6(asset_info)
        ts = calendar.timegm(time.gmtime())
        mode = {"code": 0,
                "message": "success",
                "data": {
                    "header": {
                        "retCode": retCode,
                        "retMsg": "成功",
                        "reqNo": "ea9a8753ff7044718424d189a49e31bc"
                    },
                    "data": {
                        "applyNo": self.get_hashmdt('C' + str(itemno)),
                        "putoutNo": self.get_hashmdt(itemno),
                        "duebillNo": "TG" + itemno,
                        "status": status,
                        "errMsg": None,
                        "payoutTime": ts,
                        "repayPlanList": []
                    }
                }}
        repayPlanList = {
            "term": 1,
            "repayBeginDate": "2036-07-12",
            "repayEndDate": "2036-07-12",
            "repayAmount": "1004.33",
            "termAmt": "833.33",
            "termInt": "101.39",
            "termFee": "0.00",
            "vouchFee": "5.83",
            "serviceFee": "63.78",
            "platInt": "0.00"
        }
        for i in range(asset_info['data']['asset']['period_count']):
            fee_info = get_fee_info_by_period(rate_info, i + 1)
            repayment_plan = deepcopy(repayPlanList)
            repayment_plan['term'] = i + 1
            repayment_plan['termAmt'] = float(fee_info['principal']) / 100
            repayment_plan['termInt'] = float(fee_info['interest']) / 100
            repayment_plan['vouchFee'] = float(fee_info['reserve']) / 100
            repayment_plan['serviceFee'] = float(fee_info['consult']) / 100
            repayment_plan['repayEndDate'] = fee_info['date']
            mode['data']['data']['repayPlanList'].append(repayment_plan)
        self.update(api, mode)

    def update_loan_no_order(self):
        api = '/tcl/tcl_zhongji/S012002Q'
        body = {"code": 0,
                "message": "success",
                "data": {
                    "header": {
                        "retCode": "100002",
                        "retMsg": "进件号759b52e1ac864d349ba3568a8a5c1891不存在放款信息",
                        "reqNo": "0d5583d0a45f4faaa17749a92352e915"
                    },
                    "data": {}
                }}
        self.update(api, body)

    def update_contract_down(self):
        api = '/tcl/tcl_zhongji/S010008Q'
        body = {"code": 0,
                "message": "success",
                "data": {
                    "header": {
                        "retCode": "000000",
                        "retMsg": "成功",
                        "reqNo": "a892e3fce81442bb8a7ac13fc4d116ad"
                    },
                    "data": {
                        "contractList": [
                            {
                                "contractType": "11",
                                "contractUrl": "https://openapi.bestsign.info/openapi/v2/contract/download/?developerId=1978861263916106337&rtick=16855891247770&signType=rsa&sign=Vb6rmU9uUrx%2BNRCu9WwiPbp0LJwvWfewhXmkVvh1cguJeNNR9MEK3VB0W%2BJqTmwCWQrWAtpaXnJmuzdhKgVwPUPmOUG7UZvUOf0%2FjpvoKUrRMFmLADDXXH1pPUgqbp0%2BHobX7AnKQ4fxbDKbZIHuyyElSuDL%2B0T44amR6xGpTo0%3D&contractId=168552617901000001"
                            },
                            {
                                "contractType": "02",
                                "contractUrl": "https://openapi.bestsign.info/openapi/v2/contract/download/?developerId=1978861263916106337&rtick=16855891247810&signType=rsa&sign=FbmRrS%2BagGYyIxKFLSQvSF8V18fKnmhWeWDasHgOMz1ti8U32hP8ROJf8U4rbQWPUnTXMsRllxVdlMxIZoTAUzTxNWlkhp0VD9RCSvsNt5KE35op%2F2J8vXo6n5WM%2B0T1teKx6Pm6pMhKZazaZmFX8QAz2WkjuYdMI6YCfMLKtyQ%3D&contractId=168552617901000006"
                            },
                            {
                                "contractType": "12",
                                "contractUrl": "https://openapi.bestsign.info/openapi/v2/contract/download/?developerId=1978861263916106337&rtick=16855891247870&signType=rsa&sign=nBmD%2BHjT1zL0HisM0CCTS%2F8U6T%2FlffwNgMkRd7vylZur2LzAqdvmn3j%2FyLKcfiso9eUJIB6lptw%2FivYiP5%2FO46h5fAaA2lfcQtAqYt6SOz%2FqvuhXkq2uMBpIwqz%2FugrMMPa3%2Fa27X9tq3XYVZFf%2BEQgw7KaVTMT3u8tpcNDVQys%3D&contractId=168552617901000002"
                            },
                            {
                                "contractType": "01",
                                "contractUrl": "https://openapi.bestsign.info/openapi/v2/contract/download/?developerId=1978861263916106337&rtick=16855891247920&signType=rsa&sign=VgFqhSK2su1TJ9GcjwbfVltiGJOl%2FytspZwROBpjqT1a9W96xC64i0OOTLnh%2FT6AKnFUkEu1%2BFdJJ1jwbL8IUXWrpTnjIXKsc4z7AZkSh62RD5SFE2ZMCB5Yaoc0F8DW9T8FIHjuf40w0azQWlLX8YQMOxHfyKSyGkrtKb6dK1k%3D&contractId=168552617901000005"
                            },
                            {
                                "contractType": "14",
                                "contractUrl": "https://openapi.bestsign.info/openapi/v2/contract/download/?developerId=1978861263916106337&rtick=16855891247980&signType=rsa&sign=V7BvyxzCgOvjl8TMhXcm0G5avEX%2FB2oxkXV%2BldT33mpukmi5qUw2C94xjc9nI1%2BfYvs5VnqJB%2FW3dtMuJ4pImU5XvoRW7BsHoHDn71BNxdxmMUQBOUafOlbQf4UchLZX%2BaOAm1nvJkKNTUw5WcglrvYA8i7adpfTm2SNH2Tt%2FSI%3D&contractId=168552617901000007"
                            },
                            {
                                "contractType": "03",
                                "contractUrl": "https://openapi.bestsign.info/openapi/v2/contract/download/?developerId=1978861263916106337&rtick=16855891248040&signType=rsa&sign=iUE6C%2BionlrFbQYbZHIm3dV4a0aJfRwfN57sV99bc%2FofcSKuwSxek260Y1b2Oa%2Bl%2FmhfGIUR9f3f3lPl%2Bzh64gQGwNDkkTeR4vq4RO7fnhZjCkC5XRYHD9Up%2Fxuiv3DOrkca8mtzJELgJ83mxalCjb7tHkQGSqMXQgcaYdBvi44%3D&contractId=168552617901000003"
                            }
                        ]
                    }
                }}
        self.update(api, body)

    def update_contract_push(self):
        api = '/tcl/tcl_zhongji/S010009C'
        body = {"code": 0,
                "message": "success",
                "data": {
                    "header": {
                        "retCode": "000000",
                        "retMsg": "成功",
                        "reqNo": "8653c88ab74945f4a470fd1f57870c3f"
                    },
                    "data": {}
                }}
        self.update(api, body)
