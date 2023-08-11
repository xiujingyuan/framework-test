# -*- coding: utf-8 -*-
from biztest.function.cmdb.cmdb_common_function import get_fee_info_by_period
from biztest.function.gbiz.gbiz_db_function import get_asset_loan_record_by_item_no
from biztest.interface.cmdb.cmdb_interface import cmdb_rate_loan_calculate_v6
from biztest.util.easymock.easymock import Easymock
from copy import deepcopy

from biztest.util.tools.tools import get_date


class LanhaiZhongbaoPuanMock(Easymock):

    def update_query_credit_balance_list(self, availableCreditAmount=10000, status='10', endTime='2025-07-25 00:00:00'):
        '''
        额度查询
        :return:
        '''
        api = '/puan/lanhai_zhongbao_puan/credit/queryCreditBalanceList'
        body = {
            "code": 0,
            "message": "success",
            "data": {
                "resCode": "0",
                "resDesc": "成功",
                "body": [
                    {
                        "availableCreditAmount": availableCreditAmount,
                        "certificateKind": "110001",
                        "productId": "XKDPAZB",
                        "monthRate": 0.0068,
                        "usedAmount": 0,
                        "mobileNo": "13376071726",
                        "userName": "安丽娟",
                        "certificateNo": "141122198508100347",
                        "userId": "000UC020000464200",
                        "productName": "小康贷-普安资本",
                        "applyId": "000CA202307250000029002",
                        "freezeAmount": 0,
                        "creditKind": "1",
                        "rate": 0.083,
                        "creditTerm": 360,
                        "startTime": "2023-07-25 00:00:00",
                        "endTime": endTime,
                        "creditAmount": 3000,
                        "creditTermUnit": "3",
                        "creditLimitId": "000CCLI202307250000028006",
                        "status": status
                    }
                ]
            }
        }

        self.update(api, body)

    def update_credit_apply(self, itemno, resCode='0'):
        """
        进件，授信申请接口-
        credit_status 授信状态
                P 授信中
                S 授信成功
                F 授信拒绝
        """
        api = "/puan/lanhai_zhongbao_puan/credit/apply"
        body = '''{
            "code": 0,
            "message": "success",
            "data": {
                "resCode": "%s",
                "resDesc": "成功",
                "body": {
                    "creditSeq": "KN%s",
                    "outApplyId": function({_req}) {return _req.body.outApplyId}
                }
            }
        }''' % (resCode, itemno)
        self.update(api, body)

    def update_credit_query(self, itemno, status='03', availableAmount=20000, creditEndDate='2036-12-12'):
        """
        授信查询接口
        credit_status 授信状态
                P-授信中
                S-授信成功
                F-授信拒绝
        """
        api = "/puan/lanhai_zhongbao_puan/credit/query"
        body = '''{
            "code": 0,
            "message": "success",
            "data": {
                "resCode": "0",
                "resDesc": "成功",
                "body": {
                    "creditSeq": function({_req}) {return _req.body.creditSeq},
                    "outApplyId": function({_req}) {return _req.body.outApplyId},
                    "rate": 0.083,
                    "contractNo": "000CCLI%s",
                    "creditAmount": 10000,
                    "userId": "@id",
                    "bankCreditSeq": "%s",
                    "status": "%s"
                }
            }
        }''' % (itemno, itemno, status)
        self.update(api, body)

    def update_credit_query_notorder(self):
        """
        授信查询接口
        """
        api = "/puan/lanhai_zhongbao_puan/credit/query"
        body = {
            "code": 0,
            "message": "success",
            "data": {
                "resCode": "0",
                "resDesc": "成功",
                "body": {
                    "rejectReason": "授信信息不存在",
                    "rejectCode": "120000003",
                    "status": "04"
                }
            }
        }
        self.update(api, body)

    def update_trial(self, itemno, asset_info):
        '''
        试算
        :return:
        '''
        rate_info = cmdb_rate_loan_calculate_v6(asset_info)
        api = '/puan/lanhai_zhongbao_puan/loan/trial'
        body = {
            "code": 0,
            "message": "success",
            "data": {
                "resCode": "0",
                "resDesc": "成功",
                "body": {
                    "creditSeq": "KN" + itemno,
                    "discountFee": "0",
                    "repayPrincipal": "10000.00",
                    "discountInterest": "0",
                    "repayAmount": "10449.70",
                    "repayFee": "0",
                    "repayDate": "20230924",
                    "leftRepayInterest": "449.70",
                    "repayInterest": "449.70",
                    "leftRepayPrincipal": "10000.00",
                    "paymentList": []
                }
            }
        }

        paymentList = {
            "prcpAmt": 807.96,
            "psRemPrcp": 807.96,
            "dueDt": "20231024",
            "psFeeAmt": 0,
            "instmAmt": 870.81,
            "perdNo": 1,
            "normAmt": 62.85
        }
        for i in range(asset_info['data']['asset']['period_count']):
            fee_info = get_fee_info_by_period(rate_info, i + 1)
            repayment_plan = deepcopy(paymentList)
            repayment_plan['perdNo'] = i + 1
            repayment_plan['prcpAmt'] = float(fee_info['principal']) / 100
            repayment_plan['normAmt'] = float(fee_info['interest']) / 100
            repayment_plan['dueDt'] = fee_info['date'].replace('-', '')
            repayment_plan['psRemPrcp'] = float(fee_info['interest']) / 100
            repayment_plan['instmAmt'] = float(fee_info['interest']) / 100
            body['data']['body']['paymentList'].append(repayment_plan)
        self.update(api, body)

    def update_loan_apply(self, itemno, status='1'):
        """
        放款申请
        """
        api = "/puan/lanhai_zhongbao_puan/loan/apply"
        body = {
            "code": 0,
            "message": "success",
            "data": {
                "resCode": "0",
                "resDesc": "成功",
                "body": {
                    "bankLoanSeq": "",
                    "loanNo": "",
                    "loanActvTime": "2023-08-24 18:06:43",
                    "errCode": "null",
                    "loanSeq": "LOANKN" + itemno,
                    "loanAmount": 13000,
                    "status": status
                }
            }
        }
        self.update(api, body)

    def update_loan_query(self, itemno, status='2'):
        """
        放款查询
        loan_status 借款状态
            P-处理中
            S-成功
            F-失败
        """
        api = '/puan/lanhai_zhongbao_puan/loan/query'
        date = get_date(fmt="%Y-%m-%d %H:%M:%S")
        body = {
            "code": 0,
            "message": "success",
            "data": {
                "resCode": "0",
                "resDesc": "成功",
                "body": {
                    "bankLoanSeq": "000CLA202307250000028009",
                    "loanNo": "@id",
                    "loanActvTime": date,
                    "errCode": "null",
                    "loanSeq": "LOAnKN" + itemno,
                    "loanAmount": 10000,
                    "status": status
                }
            }
        }
        self.update(api, body)

    def update_loan_query_notorder(self):
        """
        授信查询接口
        """
        api = '/puan/lanhai_zhongbao_puan/loan/query'
        body = {
            "code": 0,
            "message": "success",
            "data": {
                "resCode": "0",
                "resDesc": "成功",
                "body": {
                    "rejectReason": "放款信息不存在",
                    "rejectCode": "120000003",
                    "status": "4"
                }
            }
        }
        self.update(api, body)

    def update_repayment_plan_query(self, itemno, asset_info):
        """
        还款计划查询
        """
        rate_info = cmdb_rate_loan_calculate_v6(asset_info)
        api = '/puan/lanhai_zhongbao_puan/repaymentPlan/query'
        loanNo = get_asset_loan_record_by_item_no(itemno)[0]['asset_loan_record_due_bill_no']
        body = {
            "code": 0,
            "message": "success",
            "data": {
                "resCode": "0",
                "resDesc": "成功",
                "body": {
                    "loanNo": loanNo,
                    "dataList": [],
                    "loanStatus": "1"
                }
            }
        }
        dataList = {
            "oweInterest": 88.83,
            "oweTermFee": 0,
            "period": "1",
            "dueCapital": 1043.22,
            "oweCompoundInterest": 0,
            "overDays": 0,
            "overFeeTotal": 0,
            "perFeeTotal": 0,
            "owePrincipal": 1043.22,
            "derateInterest": 0,
            "oweOverdueFee": 0,
            "repayDate": "2023-09-24",
            "derateTermFee": 0,
            "dueInterest": 88.83,
            "repayCompoundInterest": 0,
            "status": "1"
        }
        for i in range(asset_info['data']['asset']['period_count']):
            fee_info = get_fee_info_by_period(rate_info, i + 1)
            repayment_plan = deepcopy(dataList)
            repayment_plan['period'] = i + 1
            repayment_plan['dueCapital'] = float(fee_info['principal']) / 100
            repayment_plan['owePrincipal'] = float(fee_info['principal']) / 100
            repayment_plan['dueInterest'] = float(fee_info['interest']) / 100
            repayment_plan['oweInterest'] = float(fee_info['interest']) / 100
            repayment_plan['repayDate'] = fee_info['date']
            body['data']['body']['dataList'].append(repayment_plan)
        self.update(api, body)


def update_file_download(self):
    """
    合同下载
    """
    api = '/puan/lanhai_zhongbao_puan/file/contract/download'
    body = {
        "code": "0",
        "message": "Success",
        "data": {
            "status": "S",
            "busiDate": "20230315",
            "fileId": "ff80808186772b680186e4d93f3739f4 CFS20230315183803073",
            "billType": "e-con",
            "base64": "JVBERi0xLjYKJeLjz9MKMjA2"
        }
    }
    self.update(api, body)
