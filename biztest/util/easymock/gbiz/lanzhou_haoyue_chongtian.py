# -*- coding: utf-8 -*-
from biztest.function.cmdb.cmdb_common_function import get_fee_info_by_period
from biztest.interface.cmdb.cmdb_interface import cmdb_rate_loan_calculate_v6
from biztest.util.easymock.easymock import Easymock
from biztest.function.gbiz.gbiz_db_function import get_asset_import_data_by_item_no
from biztest.function.gbiz.gbiz_db_function import get_asset_loan_record_by_item_no
from copy import deepcopy
from biztest.util.tools.tools import *


class LanzhouHaoyueChongtianMock(Easymock):

    def update_user_check(self, ifCanPush='1'):
        """
        准入接口
        :return:
        """
        api = "/chongtian/lanzhou_haoyue_chongtian/user/check"
        body = {
            "code": "000000",
            "msg": "成功",
            "data": {
                "ifCanPush": ifCanPush
            }
        }
        self.update(api, body)

    def update_bindCard_check(self, needBinding='Y'):
        """
        绑卡查询接口
        :return:
        """
        api = '/chongtian/lanzhou_haoyue_chongtian/bindCard/check'
        body = {
            "code": "000000",
            "msg": "成功",
            "data": {
                "needBinding": needBinding
            }
        }
        self.update(api, body)

    def update_bindCard_verify(self):
        """
        预绑卡
        :return:
        """
        api = '/chongtian/lanzhou_haoyue_chongtian/bindCard/verify'
        body = {
            "code": "000000",
            "msg": "成功",
            "data": {
                "bindId": "@id",
                "exUserId": "KN_enc_02_4232684671718665216_369",
                "needBinding": "Y",
                "requestId": "20c6019b-b471-4678-9273-4ca3d55c3766"
            }
        }
        self.update(api, body)

    def update_bindCard_confirm(self):
        """
        绑卡确认
        :return:
        """
        api = '/chongtian/lanzhou_haoyue_chongtian/bindCard/confirm'
        body = {
            "code": "000000",
            "msg": "成功",
            "data": {
                "code": "1",
                "msg": "绑卡成功",
                "bindId": "TESTAUTHMOCKPAY2212064304",
                "exUserId": None,
                "requestId": "20c6019b-b471-4678-9273-4ca3d55c3766"
            }
        }
        self.update(api, body)

    def update_user_infoPush(self, code='000000', msg='成功'):
        """
        资料推送
        :return:
        """
        api = '/chongtian/lanzhou_haoyue_chongtian/user/infoPush'
        body = {
                "code": code,
                "msg": msg,
                "data": {
                    "applyFlag": "Y"
                }
            }
        self.update(api, body)

    def update_user_infoPushQuery(self, code='000000', msg='成功', handleStatus='SUC', failMsg=''):
        """
        资料推送查询
        :return:
        """
        api = '/chongtian/lanzhou_haoyue_chongtian/user/infoPushQuery'
        body = {
            "code": code,
            "msg": msg,
            "data": {
                "handleStatus": handleStatus,
                "handleSucTime": get_date(),  # 没什么实际意义
                "failMsg": failMsg
            }
        }
        self.update(api, body)

    def update_loancreditapply(self, code='000000', msg='成功'):
        """
        只是调用一下这个接口（放款试算接口）
        :return:
        """
        api = '/chongtian/lanzhou_haoyue_chongtian/loan/calc'
        body = {
            # 只取了最外层code做判断，其他字段没做处理
            "code": code,
            "msg": msg,
            "data": {
                "agreementList": [],
                "applyNo": None,
                "extUserId": "KN_enc_02_3892252158640785408_212",
                "firstRepayDate": "20220715",
                "lender": None,
                "loanCreditNo": None,
                "loanOrderNo": None,
                "loanRate": 0.36,
                "repayPlanList": [{
                    "repayDate": "20220715",
                    "schdAmt": 1002.64,
                    "schdFee": 90.68,
                    "schdInt": 143.01,
                    "schdPen": None,
                    "schdPrin": 768.95,
                    "termNo": 1,
                    "valueDate": "20220615"
                }
                ],
                "result": None,
                "schdAmt": 12053.41,
                "schdFee": 1088.05,
                "schdInt": 965.36,
                "schdPrin": 10000
            }
        }
        self.update(api, body)



    def update_loan_request(self, item_no, code='000000', msg='成功'):
        """
        借款申请
        :return:
        """
        api = '/chongtian/lanzhou_haoyue_chongtian/loan/request'
        body = {
            "code": code,
            "msg": msg,
            "data": {
                "loanOrderNo": item_no+"_XH",
                "applyNo": "@id",
                "extUserId": "KN_enc_02_4232684671718665216_369",
                "lender": None,
                "loanApplyStatus": "LOAN_APPLY_SUCCESS",
                "remark": None,
                "repayMethod": None
            }
        }
        self.update(api, body)

    def update_loanapply_trial(self, item_no, rate=7.3):
        """
        资方利率查询
        :return:
        """
        api = '/chongtian/lanzhou_haoyue_chongtian/loan/fundLoanRate'
        body = {
                  "code": "000000",
                  "msg": "成功",
                  "data": {
                    "fundCode": "XH",
                    "loanOrderNo": item_no+"_XH",
                    "yearRate": rate
                  }
                }
        self.update(api, body)


    def update_loan_results_query(self, item_no, code='000000', msg='成功', applyStatus='LOAN_PASSED',
                                  applyResult='放款成功'):
        """
        借款结果查询,valuDate以下的参数没有啥用，也没有校验，contractList&repayPlanList都是有值的，只是未使用，此处不mock
        :return:
        """
        api = '/chongtian/lanzhou_haoyue_chongtian/loan/results/query'
        body = {
            "code": code,
            "msg": msg,
            "data": {
                "loanOrderNo": item_no + "_XH",
                "platBillNo": "PLCN" + item_no,
                "applyNo": "@id",
                "applyStatus": applyStatus,
                "refuseCode": None,
                "applyResult": applyResult,
                "issueDate": get_date(),
                "valuDate": get_date(fmt="%Y%m%d"),
                "bankCardNo": "5522453814356910",
                "bankCode": "CCB",
                "contactNo": "PLCN20220727516059668EKHF7P00016",
                "contractList": [],
                "customerChannel": "API-KN",
                "dueDay": 27,
                "endDate": "20230727",
                "extUserId": "KN_enc_02_4041278687604639744_878",
                "lender": None,
                "loanAmount": 8000,
                "loanBal": 8000,
                "loanCardName": "建设银行",
                "loanCardNo": "5522453814356910",
                "loanErrType": None,
                "loanStatus": "LOAN_PASSED",
                "loanTerm": 12,
                "name": "蔡璐",
                "overdueDays": 0,
                "repayPlanList": [],
                "schdAmt": 9080.77,
                "settleTime": None,
                "status": "REPAY",
                "statusTime": 1658817930000,
                "yearRate": 0.24
            }
        }
        self.update(api, body)


    def upate_repayplan_query(self, asset_info, item_no):
        """
        还款计划查询
        :return:
        """
        api = '/chongtian/lanzhou_haoyue_chongtian/repayplan/query'
        rate_info = cmdb_rate_loan_calculate_v6(asset_info)
        bindcardnoencrypt = asset_info['data']['receive_card']['num_encrypt']
        termnum = asset_info['data']['asset']['period_count']
        loanamount = asset_info['data']['asset']['amount']
        body = {
            "code": "000000",
            "msg": "成功",
            "data": {
                "loanOrderNo": item_no + "_XH",
                "bankCardNo": bindcardnoencrypt,
                "bankCode": "CCB",
                "bankName": "建设银行",
                "loanTime": get_date(),
                "loanAmount": loanamount,
                "loanNumber": termnum,
                "paidTerm": 0,
                "currentTerm": 1,
                "repayDate": None,
                "repayTerm": None,
                "repayAmt": 0,
                "repayPrin": 0,
                "repayInteger": None,
                "repayFee": 0,
                "repayPen": 0,
                "overdueDays": 0,
                "status": "BAN_PRE_REPAY",
                "applyNo": "SER202207266606856235",
                "extUserId": "KN_enc_02_4041278687604639744_878",
                "loanBal": 8000,
                "loanStatus": "LOAN_PASSED",
                "repayInt": 0,
                "settleTime": None,
                "statusTime": 1658817930000,
                "yearRate": 0.24,
                "repayPlanList": [],
                "contractList": [
                    # 返回的没意义，这里就不需要mock了
                ]
            }
        }
        repayPlanList = {
                        "canChannelDeduct": False,
                        "canRepayTime": 1670256000000,
                        "dueRepayTime": 1672934400000,
                        "graceDate": 1673020800000,
                        "overdue": "N",
                        "overdueDays": 0,
                        "paidAmt": 0,
                        "paidFee": 0,
                        "paidInt": 0,
                        "paidPen": 0,
                        "paidPrin": 0,
                        "preRepay": None,
                        "realAmt": 944.68,
                        "realFee": 78.03,
                        "realInt": 60.83,
                        "realPen": 0,
                        "realPrin": 805.82,
                        "repayCategory": None,
                        "repayDate": "20230106",
                        "repayTime": None,
                        "schdAmt": 944.68,
                        "schdFee": 78.03,
                        "schdInt": 60.83,
                        "schdLoanServFee": None,
                        "schdPen": 0,
                        "schdPrin": 805.82,
                        "schdTermServFee": None,
                        "settleTime": None,
                        "termNo": 1,
                        "termStatus": "PAYING",
                        "valueDate": "20221206"
                    }
        for i in range(asset_info['data']['asset']['period_count']):
            fee_info = get_fee_info_by_period(rate_info, i + 1)
            repayment_plan = deepcopy(repayPlanList)
            repayment_plan['termNo'] = i + 1
            repayment_plan['schdPrin'] = float(fee_info['principal']) / 100
            repayment_plan['schdInt'] = float(fee_info['interest']) / 100
            repayment_plan['schdFee'] = float(fee_info['consult']) / 100
            repayment_plan['repayDate'] = fee_info['date'].replace("-", "")
            body['data']['repayPlanList'].append(repayment_plan)
        self.update(api, body)

    def update_contract_query(self):
        """
        合同查询下载
        :return:
        """
        api = '/chongtian/lanzhou_haoyue_chongtian/contract/query'
        body = {
                "code": "000000",
                "msg": "成功",
                "data": [
                    {
                        "contractId": "16745",
                        "contractName": "个人信息查询授权协议",
                        "contractPath": "https://ndmicro-bohai.oss-cn-beijing.aliyuncs.com/TMD/SIGN/CREDIT/202207/CON2022072814223757534171-0-20220728142238065644.pdf",
                        "contractType": "BIZ_CREDIT_AUTH",
                        "type": None
                    },
                    {
                        "contractId": "16746",
                        "contractName": "借款须知及风险提示",
                        "contractPath": "https://ndmicro-bohai.oss-cn-beijing.aliyuncs.com/TMD/SIGN/LOAN/202207/CON2022072814224038553491-0-20220728142240341693.pdf",
                        "contractType": "BIZ_LOAN_REQUIREMENTS",
                        "type": None
                    },
                    {
                        "contractId": "16747",
                        "contractName": "委托扣款协议",
                        "contractPath": "https://ndmicro-bohai.oss-cn-beijing.aliyuncs.com/TMD/SIGN/LOAN/202207/CON2022072814224299571193-0-20220728142242369946.pdf",
                        "contractType": "BIZ_WITHHOLD",
                        "type": None
                    },
                    {
                        "contractId": "16748",
                        "contractName": "综合授权书",
                        "contractPath": "https://ndmicro-bohai.oss-cn-beijing.aliyuncs.com/JMX/V1/202207/df0a38dc82ba4cc4a8dd5c18f3d3a6ae-0-20220728142303201958.pdf",
                        "contractType": "PERSONAL_COMPOSITE_AUTH",
                        "type": None
                    },
                    {
                        "contractId": "16749",
                        "contractName": "委托扣款授权书",
                        "contractPath": "https://ndmicro-bohai.oss-cn-beijing.aliyuncs.com/JMX/V1/202207/80491dfc1b0a4add8f165d8556f4a1c8-0-20220728142305914949.pdf",
                        "contractType": "WITHHOLD_AUTH",
                        "type": None
                    },
                    {
                        "contractId": "16750",
                        "contractName": "委托担保协议",
                        "contractPath": "https://ndmicro-bohai.oss-cn-beijing.aliyuncs.com/JMX/V1/202207/8f52505d470f488bbb3b29ad98c466d2-0-20220728142306299804.pdf",
                        "contractType": "ENTRUST_GUARANTEE",
                        "type": None
                    },
                    {
                        "contractId": "16751",
                        "contractName": "借款合同",
                        "contractPath": "https://ndmicro-bohai.oss-cn-beijing.aliyuncs.com/JMX/V1/202207/0267384fe1824c0fa7cf1b9cba0cfaaf-0-20220728142308547742.pdf",
                        "contractType": "LOAN",
                        "type": None
                    },
                    {
                        "contractId": "16752",
                        "contractName": "贷款担保函",
                        "contractPath": "https://ndmicro-bohai.oss-cn-beijing.aliyuncs.com/JMX/CONTRACT/GUARANTEE_PLCN2022072876558603PGR7UNZ11426.pdf",
                        "contractType": "GUARANTEE",
                        "type": None
                    }
                ]
            }
        self.update(api, body)

    def update_guaranteesign_success(self):
        """
        担保方签约申请成功
        :return:
        """
        api = '/hanchen/lanzhou_haoyue_chongtian/sign/tasynstreamsave'
        body = {
                  "code": "0",
                  "msg": "操作成功",
                  "fileId": "@id"
                }
        self.update(api, body)

    def update_guaranteedown_success(self):
        """
        担保合同下载成功
        :return:
        """
        api = '/hanchen/lanzhou_haoyue_chongtian/sign-query'
        body = {
              "code": "0",
              "msg": "操作成功",
              "fileUrl": "https://esignoss.esign.cn/1111563786/aab78995-d388-4a7c-9a60-7686dd21931f/%E7%BA%BF%E4%B8%8A%E6%8B%85%E4%BF%9D%E7%AD%BE%E7%AB%A0.pdf?Expires=1659067939&OSSAccessKeyId=LTAI4G23YViiKnxTC28ygQzF&Signature=B3KG2OG1S3CpfVqoTvuIzeYSd4Q%3D"
            }
        self.update(api, body)

