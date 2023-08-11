# -*- coding: utf-8 -*-
from biztest.function.cmdb.cmdb_common_function import get_fee_info_by_period
from biztest.interface.cmdb.cmdb_interface import cmdb_rate_loan_calculate_v6
from biztest.util.easymock.easymock import Easymock
from copy import deepcopy
from biztest.util.tools.tools import *


class JiexinTaikangXinheyuanMock(Easymock):
    def update_route_applycheck_success(self):
        '''
        路由初筛接口
        approvalResult 审批结果 01：准入 02：拒绝
        :return:
        '''
        api = "/xinheyuan/jiexin_taikang_xinheyuan/applyCheck"
        mode = {
                "code": 0,
                "message": "success",
                "data": {
                    "approvalResult": "01",
                    "responseCode": "0000"
                }
            }
        self.update(api, mode)

    # def update_query_bind_card_new_user_01(self):
    #     '''
    #     这个接口一般情况下无用处，返回什么code都不会失败
    #     :return:
    #     '''
    #     api = "/xinheyuan/jiexin_taikang_xinheyuan/queryUserBankList"
    #     mode = {
    #         "code": 0,
    #         "message": "success",
    #         "data": {
    #             "responseCode": "0000"
    #         }
    #     }
    #     self.update(api, mode)

    def update_query_insurestatus_new_user(self):
        '''
        用户从未开过户
        :return:
        '''
        api = "/xinheyuan/jiexin_taikang_xinheyuan/insureStatusQuery"
        mode = {
                "code": 0,
                "message": "success",
                "data": {
                    "responseCode": "E00001",
                    "responseMsg": "未发起投保初筛申请"
                }
            }

        self.update(api, mode)

    def update_query_insure_status_success(self):
        '''
        用户投保成功
        insureStatus投保状态
        SUCCESS:投保成功/
        FAIL:投保失败 ------失败不会更改主表的状态为失败
        IN_PROCESS:保单处理中------继续流程
        NO_AWARD:未投保------继续流程
        '''
        api = "/xinheyuan/jiexin_taikang_xinheyuan/insureStatusQuery"
        mode = {
              "code": 0,
              "message": "success",
              "data": {
                "insureStatus": "SUCCESS",
                "realInsureStatus": "SUCCESS",
                "responseCode": "0000"
              }
            }

        self.update(api, mode)

    def update_query_insure_status_process(self):
        '''
        用户投保成功
        insureStatus投保状态
        SUCCESS:投保成功/
        FAIL:投保失败 ------失败不会更改主表的状态为失败
        IN_PROCESS:保单处理中------继续流程
        NO_AWARD:未投保------继续流程
        '''
        api = "/xinheyuan/jiexin_taikang_xinheyuan/insureStatusQuery"
        mode = {
              "code": 0,
              "message": "success",
              "data": {
                "insureStatus": "IN_PROCESS",
                "realInsureStatus": "IN_PROCESS",
                "responseCode": "0000"
              }
            }

        self.update(api, mode)


    def update_get_bind_card_sms(self):
        '''
        开户获取短信验证码
        :return:
        '''
        api = "/xinheyuan/jiexin_taikang_xinheyuan/getBindBankSMS"
        mode = {
                "code": 0,
                "message": "success",
                "data": {
                      "messageNo": "@id",
                      "responseCode": "0000"
                }}
        self.update(api, mode)



    def update_verify_bind_bank(self):
        '''
        开户协议支付验证
        :return:
        '''
        api = "/xinheyuan/jiexin_taikang_xinheyuan/verifyBindBankSMS"
        mode = {
            "code": 0,
            "message": "success",
            "data": {
                  "responseCode": "0000"
                }}
        self.update(api, mode)


    def update_query_bindbank_result(self):
        '''
        查询开户绑卡结果
        :return:
        '''
        api = "/xinheyuan/jiexin_taikang_xinheyuan/queryBindBankResult"
        mode = '''{
            "code": 0,
            "message": "success",
            "data": {
                  "responseCode": "0000",
                  "responseMsg": "绑卡成功"
                }}'''
        self.update(api, mode)


    def update_insureapply_check(self):
        '''
        投保初筛
        :return:
        '''
        api = "/xinheyuan/jiexin_taikang_xinheyuan/insureApplyCheck"
        mode = {
                "code": 0,
                "message": "success",
                "data": {
                    "responseCode": "0000"
                }
            }
        self.update(api, mode)


    def update_insure_h5url_query_success(self):
        '''
        投保H5页面获取
        status	状态
            SUCCESS: 可投保（会返回h5投保链接 ）
            FAIL: 不可投保（后续不需再调用）
            IN_PROCESS: 处理中（需要稍后重试）
            NO_AWARD: 流程异常（没调用投保初筛，或初筛同步返回失败）
        :return:
        '''
        api = "/xinheyuan/jiexin_taikang_xinheyuan/insureUrlQuery"
        mode = '''{
                    "code": 0,
                    "message": "success",
                    "data": {
                        "insureUrl": "http://ecuat.tk.cn/channel/nprd/trace-xinbaosys-h5/?content=%7B%22appId%22%3A%2220211213919911215315025920%22%2C%22bankCardNo%22%3A%225522458818652610%22%2C%22bankNames%22%3A%22%E6%B2%B3%E5%8C%97%E9%93%B6%E8%A1%8C%22%2C%22callBackUrl%22%3A%22capp%3A%2F%2Fyuxin_h5_insurance_confirm%22%2C%22certNo%22%3A%22350304199504301281%22%2C%22fundInfos%22%3A%5B%7B%22fundCode%22%3A%22WEBANK%22%2C%22fundLoanAmt%22%3A%2210000.00%22%2C%22insureFee%22%3A%2282.63%22%7D%5D%2C%22insureSeriaNo%22%3A%22LXWZ202209130000000364%22%2C%22loanAmt%22%3A%2210000.00%22%2C%22mobileNo%22%3A%2213910000033%22%2C%22name%22%3A%22%E9%98%AE%E7%A7%80%E4%BA%91%22%2C%22sysdata%22%3A%22jiexin%22%7D",
                        "responseCode": "0000",
                        "status": "SUCCESS"
                    }
                }'''
        self.update(api, mode)


    def update_insure_h5url_query_fail(self):
        '''
        投保H5页面获取失败
        :return:
        '''
        api = "/xinheyuan/jiexin_taikang_xinheyuan/insureUrlQuery"
        mode = '''{
                  "code": 0,
                  "message": "mock获取URL失败",
                  "data": {
                    "insureUrl": "",
                    "responseCode": "0000",
                    "status": "FAIL"
                  }
                }
                '''
        self.update(api, mode)

    def update_loanapplynew_success(self):
        api = "/xinheyuan/jiexin_taikang_xinheyuan/creditApply"
        mode = '''{
                    "code": 0,
                    "message": "success",
                    "data": {
                        "responseCode": "0000"
                    }
                }'''
        self.update(api, mode)


    def update_loanapplynew_fail(self):
        api = "/xinheyuan/jiexin_taikang_xinheyuan/creditApply"
        mode = '''{
                 "code": 0,
                 "message": "success",
                 "data": {
                      "responseCode": "9999"
                    }}'''
        self.update(api, mode)


    def update_Loanapplyquery_success(self, totalcredit='20000.00', subexpdate='2036-12-12'):
        api = "/xinheyuan/jiexin_taikang_xinheyuan/getCreditAudit"
        mode = {
                 "code": 0,
                 "message": "success",
                 "data": {
                      "approvalResult": "01",
                        "loadDownMark": "02",
                        "responseCode": "0000",
                        "subExpDate": subexpdate,
                        "totalCredit": totalcredit
                    }}
        self.update(api, mode)


    def update_Loanapplyquery_fail(self):
        api = "/xinheyuan/jiexin_taikang_xinheyuan/getCreditAudit"
        mode = '''{
                 "code": 0,
                 "message": "success",
                 "data": {
                    "approvalResult": "02",
                    "approvalResultCode": "05",
                    "approvalResultDesc": "综合评分不足",
                    "loadDownMark": "02",
                    "rejectDeadline": "2022-12-13",
                    "responseCode": "0000"
                }}'''
        self.update(api, mode)


    def update_loanapplyconfirm_success(self):
        api = "/xinheyuan/jiexin_taikang_xinheyuan/loanApply"
        mode = '''{
                "code": 0,
                "message": "success",
                "data": {
                    "responseCode": "0000"
                }
            }'''
        self.update(api, mode)

    def update_loanapplyconfirm_fail(self):
        api = "/xinheyuan/jiexin_taikang_xinheyuan/loanApply"
        mode = '''{
                "code": 0,
                "message": "success",
                "data": {
                    "responseCode": "9999",
                    "responseMsg": "mock失败"
                }}'''
        self.update(api, mode)


    def update_loanconfirmquery_success(self):
        api = "/xinheyuan/jiexin_taikang_xinheyuan/useLoanQuery"
        mode = '''{
            "code": 0,
            "message": "success",
            "data": {
                    "contractId": "@id",
                    "loanMaturity": "%s",
                    "loanResult": "06",
                    "loanResultDesc": "success",
                    "loanTime": "%s",
                    "responseCode": "0000"
                }}''' % (get_date(month=12, fmt="%Y-%m-%d"), get_date(fmt="%Y-%m-%d %H:%M:%S"))
        self.update(api, mode)


    def update_loanconfirmquery_fail(self):
        api = "/xinheyuan/jiexin_taikang_xinheyuan/useLoanQuery"
        mode = '''{
            "code": 0,
            "message": "success",
            "data": {
                    "contractId": "",
                    "loanResult": "04",
                    "loanResultDesc": "重复进件关闭历史单,此前状态:[5]",
                    "responseCode": "0000"
                }}'''
        self.update(api, mode)


    def update_queryrepayplan_success(self, item_no, asset_info):
        api = "/xinheyuan/jiexin_taikang_xinheyuan/repaymentPlanQuery"
        mode = {
            "code": 0,
            "message": "success",
            "data": {
                  "loanNo": item_no,
                  "pkgList": [],
                  "responseCode": "0000"
                }}
        repayment_plan_tmp = {
                      "guarantorFee": "0.00",
                      "intAmt": "0.00",
                      "noGuarantorFee": "81.25",
                      "noRetAmt": "808.79",
                      "noRetFin": "0.00",
                      "noRetInt": "54.17",
                      "otherFeeName": "风险保障金",
                      "prinAmt": "0.00",
                      "repayIntbDate": "2042-01-25",
                      "repayInteDate": "2042-02-25",
                      "repayOwnbDate": "2042-02-25",
                      "repayOwneDate": "2042-02-25",
                      "repayTerm": "1",
                      "settleFlag": "RUNNING",
                      "termFintFinish": "0.00",
                      "termGuarantorFee": "81.25",
                      "termRetFint": "0.00",
                      "termRetInt": "54.17",
                      "termRetPrin": "808.79",
                      "termStatus": "N",
                      "totalAmt": "944.21"
                    }
        rate_info = cmdb_rate_loan_calculate_v6(asset_info)
        for i in range(asset_info['data']['asset']['period_count']):
            fee_info = get_fee_info_by_period(rate_info, i + 1)
            repayment_plan = deepcopy(repayment_plan_tmp)
            repayment_plan['repayTerm'] = i + 1
            repayment_plan['repayOwnbDate'] = fee_info['date']
            repayment_plan['termRetPrin'] = str(float(fee_info['principal'])/100)
            repayment_plan['termRetInt'] = str(float(fee_info['interest'])/100)
            mode['data']['pkgList'].append(repayment_plan)
        self.update(api, mode)



    def update_contractquery_success(self):
        api = "/xinheyuan/jiexin_taikang_xinheyuan/contractSignedQuery"
        mode = '''{
                "code": 0,
                "message": "success",
                "data": {
                    "contractLists": [
                        {
                            "contractId": "21267334101",
                            "contractName": "个人消费信贷额度合同-捷信",
                            "contractNo": "GRXF.XDED.HT.1.14.pdf",
                            "contractUrl": "http://fastdfs-test.lvxtech.com/group1/M00/28/A6/CgoLiGMhddSAHxRWAAZ_kNTVyn8984.pdf",
                            "urlType": "01"
                        },
                        {
                            "contractId": "21267334101",
                            "contractName": "个人贷款保证保险电子保险单",
                            "contractNo": "JXXJ.GRDK.BZBX.DZBXD.1.39.pdf",
                            "contractUrl": "http://fastdfs-test.lvxtech.com/group1/M00/28/B2/CgoLiGMkHo2AZ9MvAAZDf37GuJ8275.pdf",
                            "urlType": "01"
                        },
                        {
                            "contractId": "21267334101",
                            "contractName": "客户个人授权书-捷信",
                            "contractNo": "KH.GR.SQS.JX.1.27.pdf",
                            "contractUrl": "http://fastdfs-test.lvxtech.com/group1/M00/28/A6/CgoLiGMhddWAQk88AAbAEIVVN-s107.pdf",
                            "urlType": "01"
                        },
                        {
                            "contractId": "21267334101",
                            "contractName": "个人信息处理授权书",
                            "contractNo": "GRXX.CL.SQS.XHY.1.27.pdf",
                            "contractUrl": "http://fastdfs-test.lvxtech.com/group1/M00/28/A6/CgoLiGMhddSAYDyGAANG_wH0gzk528.pdf",
                            "urlType": "01"
                        },
                        {
                            "contractId": "21267334101",
                            "contractName": "代扣服务授权书",
                            "contractNo": "DKFW.SQS.XHY.1.27.pdf",
                            "contractUrl": "http://fastdfs-test.lvxtech.com/group1/M00/28/A6/CgoLiGMhfwOAXerVAAMutOeC9cI261.pdf",
                            "urlType": "01"
                        },
                        {
                            "contractId": "21267334101",
                            "contractName": "个人借款合同-河北银行",
                            "contractNo": "JXXJ.HBYH.GR.KKHT.1.39.pdf",
                            "contractUrl": "http://fastdfs-test.lvxtech.com/group1/M00/28/B2/CgoLiGMkHo2ASg94AAP_crB_FyE668.pdf",
                            "urlType": "01"
                        }
                    ],
                    "responseCode": "0000"
                }
            }
            '''
        self.update(api, mode)





if __name__ == "__main__":
    pass
