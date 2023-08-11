# -*- coding: utf-8 -*-
from biztest.function.cmdb.cmdb_common_function import get_fee_info_by_period
from biztest.interface.cmdb.cmdb_interface import cmdb_rate_loan_calculate_v6
from biztest.util.easymock.easymock import Easymock
from biztest.function.gbiz.gbiz_db_function import get_asset_import_data_by_item_no
from biztest.function.gbiz.gbiz_db_function import get_asset_loan_record_by_item_no
from copy import deepcopy
from biztest.util.tools.tools import *


class beiyinDaqinMock(Easymock):

    def update_user_check(self, ifCanPush='1'):
        """
        准入接口
        :return:
        """
        api = "/chongtian/beiyin_daqin/user/check"
        body = {
            "code": "000000",
            "msg": "成功",
            "data": {
                "ifCanPush": ifCanPush
            }
        }
        self.update(api, body)

    def update_bindCard_ceck(self, needBinding='Y'):
        """
        绑卡查询接口
        :return:
        """
        api = '/chongtian/beiyin_daqin/bindCard/check'
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
        api = '/chongtian/beiyin_daqin/bindCard/verify'
        body = {
            "code": "000000",
            "msg": "成功",
            "data": {
                "bindId": "@id",
                "needBinding": "Y"
            }
        }
        self.update(api, body)

    def update_bindCard_confirm(self):
        """
        绑卡确认
        :return:
        """
        api = '/chongtian/beiyin_daqin/bindCard/confirm'
        body = {
            "code": "000000",
            "msg": "成功",
            "data": {
                "code": "1",
                "msg": "绑卡成功",
                "bindId": None
            }
        }
        self.update(api, body)

    def update_user_infoPush(self, code='000000', msg='成功'):
        """
        资料推送
        :return:
        """
        api = '/chongtian/beiyin_daqin/user/infoPush'
        body = {
            "code": code,
            "msg": msg,
            "data": None
        }
        self.update(api, body)

    def update_user_infoPushQuery(self, code='000000', msg='成功', handleStatus='SUC', failMsg=''):
        """
        资料推送查询
        :return:
        """
        api = '/chongtian/beiyin_daqin/user/infoPushQuery'
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

    def update_loan_trial(self, code='000000', msg='成功'):
        """
        放款试算
        :return:
        """
        api = '/chongtian/beiyin_daqin/loan/calc'
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
        api = '/chongtian/beiyin_daqin/loan/request'
        body = {
            "code": code,
            "msg": msg,
            "data": {
                "loanOrderNo": item_no,
                "applyNo": "@id"
            }
        }
        self.update(api, body)

    def update_loan_results_query(self, item_no, code='000000', msg='成功', applyStatus='LOAN_PASSED',
                                  applyResult='放款成功'):
        """
        借款结果查询
        :return:
        """
        api = '/chongtian/beiyin_daqin/loan/results/query'
        body = {
            "code": code,
            "msg": msg,
            "data": {
                "loanOrderNo": item_no + "_BY",
                "platBillNo": "PLCN" + item_no,
                "applyNo": "@id",
                "applyStatus": applyStatus,
                "refuseCode": None,
                "applyResult": applyResult,
                "issueDate": get_date(),
                "valuDate": get_date(fmt="%Y%m%d")
            }
        }
        self.update(api, body)

    def upate_repayplan_query(self, asset_info, item_no):
        """
        还款计划查询
        :return:
        """
        api = '/chongtian/beiyin_daqin/repayplan/query'
        rate_info = cmdb_rate_loan_calculate_v6(asset_info)
        bindcardnoencrypt = asset_info['data']['receive_card']['num_encrypt']
        termnum = asset_info['data']['asset']['period_count']
        loanamount = asset_info['data']['asset']['amount']
        body = {
            "code": "000000",
            "msg": "成功",
            "data": {
                "loanOrderNo": item_no + "_BY",
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
                "repayPlanList": [],
                "contractList": [
                    # 返回的没意义，这里就不需要mock了
                ]
            }
        }
        repayPlanList = {
            "termNo": 1,
            "valueDate": "20220415",
            "repayDate": "20220515",
            "schdAmt": 1021.82,
            "schdPrin": 756.14,
            "schdInt": 175,
            "schdFee": 90.68,
            "realAmt": 1021.82,
            "realPrin": 756.14,
            "realInt": 175,
            "realPen": 0,
            "realFee": 90.68,
            "paidAmt": 0,
            "paidPrin": 0,
            "paidInt": 0,
            "paidFee": 0,
            "paidPen": 0,
            "overdueDays": 0,
            "termStatus": "PAYING",
            "repayCategory": None,
            "overdue": "N"
        }
        for i in range(asset_info['data']['asset']['period_count']):
            fee_info = get_fee_info_by_period(rate_info, i + 1)
            repayment_plan = deepcopy(repayPlanList)
            repayment_plan['termNo'] = i + 1
            repayment_plan['schdPrin'] = float(fee_info['principal']) / 100
            repayment_plan['schdInt'] = float(fee_info['interest']) / 100
            repayment_plan['schdFee'] = float(fee_info['reserve']) / 100 + float(fee_info['consult']) / 100
            repayment_plan['schdAmt'] = repayment_plan['schdPrin'] + repayment_plan['schdInt'] + \
                                        repayment_plan['schdFee']
            repayment_plan['repayDate'] = fee_info['date'].replace("-", "")
            body['data']['repayPlanList'].append(repayment_plan)
        self.update(api, body)

    def updat_contract_query(self):
        """
        合同查询下载
        :return:
        """
        api = '/chongtian/beiyin_daqin/contract/query'
        body = {
    "code": "000000",
    "msg": "成功",
    "data": [
            {
                "contractName": "个人信息查询授权协议",
                "contractId": "5962002",
                "contractPath": "https://ndmicro-yanzhidai-prod.oss-cn-beijing.aliyuncs.com/TMD/SIGN/LOAN/202207/CON2022071406295415921795-0-20220714062954714758.pdf",
                "contractType": "BIZ_CREDIT_AUTH"
            },
            {
                "contractName": "借款须知及风险提示",
                "contractId": "5962003",
                "contractPath": "https://ndmicro-yanzhidai-prod.oss-cn-beijing.aliyuncs.com/TMD/SIGN/LOAN/202207/CON2022071406295415921795-0-20220714062954714758.pdf",
                "contractType": "BIZ_LOAN_REQUIREMENTS"
            },
            {
                "contractName": "个人授权及风险告知书",
                "contractId": "5962272",
                "contractPath": "https://ndmicro-yanzhidai-prod.oss-cn-beijing.aliyuncs.com/TMD/SIGN/LOAN/202207/CON2022071406295415921795-0-20220714062954714758.pdf",
                "contractType": "PERSONAL_COMPOSITE_AUTH"
            },
            {
                "contractName": "个人消费贷款申请书",
                "contractId": "5962279",
                "contractPath": "https://ndmicro-yanzhidai-prod.oss-cn-beijing.aliyuncs.com/TMD/SIGN/LOAN/202207/CON2022071406295415921795-0-20220714062954714758.pdf",
                "contractType": "LOAN"
            },
            {
                "contractName": "咨询服务及委托保证合同 ",
                "contractId": "5962282",
                "contractPath": "https://ndmicro-yanzhidai-prod.oss-cn-beijing.aliyuncs.com/TMD/SIGN/LOAN/202207/CON2022071406295415921795-0-20220714062954714758.pdf",
                "contractType": "GUARANTEE"
            },
            {
                "contractName": "敏感个人信息授权书",
                "contractId": "5962289",
                "contractPath": "https://ndmicro-yanzhidai-prod.oss-cn-beijing.aliyuncs.com/TMD/SIGN/LOAN/202207/CON2022071406295415921795-0-20220714062954714758.pdf",
                "contractType": "PERSONAL_CREDIT_QUERY"
            },
            {
                "contractName": "个人信息对外提供授权书",
                "contractId": "5962294",
                "contractPath": "https://ndmicro-yanzhidai-prod.oss-cn-beijing.aliyuncs.com/TMD/SIGN/LOAN/202207/CON2022071406295415921795-0-20220714062954714758.pdf",
                "contractType": "PERSONAL_INFO_QUERY"
            }
        ]
    }
        self.update(api, body)
