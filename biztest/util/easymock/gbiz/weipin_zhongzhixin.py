# -*- coding: utf-8 -*-
from biztest.function.cmdb.cmdb_common_function import get_fee_info_by_period
from biztest.function.gbiz.gbiz_db_function import get_asset_event
from biztest.interface.cmdb.cmdb_interface import cmdb_rate_loan_calculate_v6
from biztest.util.easymock.easymock import Easymock
from copy import deepcopy
from biztest.util.tools.tools import *



class WeipinZhongweiMock(Easymock):

    def __init__(self, project, check_req=True, return_req=False):
        super(WeipinZhongweiMock, self).__init__(project, check_req=check_req, return_req=return_req)
        self.idnum = None

    def set_idno(self, four_element):
        id_number_encrypt = four_element['data']['id_number_encrypt']
        self.idnum = decrypt_data(id_number_encrypt)

    def update_open_register(self, status='S'):
        '''
        用户注册
        :return:
        '''
        api = "/weipin/weipin_zhongzhixin/customer/openRegister"
        body = {
            "code": 0,
            "message": "success",
            "data": {
                "body": {
                    "respCode": "000000",
                    "respMessage": "渠道处理成功",
                    "status": status,
                    "tenantId": "888",
                    "userId": self.idnum  # 根据身份证生成
                },
                "header": {
                    "channel": "10010000028",
                    "code": "000000",
                    "message": "访问成功",
                    "seqNo": "5656a9e098424d0480ce145f05b51e00",
                    "timeStamp": "20230221102535093"
                }
            }
        }
        # {
        #     "code": 0,
        #     "message": "success",
        #     "data": {
        #         "body": {
        #             "respCode": "101021",
        #             "respMessage": "证件号码格式不正确",
        #             "status": "F",
        #             "tenantId": "888"
        #         },
        #         "header": {
        #             "channel": "10010000028",
        #             "code": "000000",
        #             "message": "访问成功",
        #             "seqNo": "8a243f8795cf4c00b240b61f04d32ebe",
        #             "timeStamp": "20230222164806370"
        #         }
        #     }
        # }

        self.update(api, body)


    def update_bind_bank_card_apply(self):
        '''
        预绑卡
        :return:
        '''
        api = '/weipin/weipin_zhongzhixin/customer/bindBankCardApply'
        body = {
            "code": 0,
            "message": "success",
            "data": {
                "body": {
                    "productId": "1201001030020",
                    "respCode": "000000",
                    "respMessage": "请求成功",
                    "status": "01",
                    "tenantId": "888",
                    "userId": self.idnum
                },
                "header": {
                    "channel": "10010000028",
                    "code": "000000",
                    "message": "访问成功",
                    "seqNo": "a7ac342463d34d44977ae014a9d0ee34",
                    "timeStamp": "20230221104450999"
                }
            }
        }
        self.update(api, body)

    def update_bind_bank_card_msg_verify(self):
        '''
        绑卡
        :return:
        '''
        api = '/weipin/weipin_zhongzhixin/customer/bindBankCardMsgVerify'
        body = {
            "code": 0,
            "message": "success",
            "data": {
                "body": {
                    "productId": "1201001030020",
                    "respCode": "000000",
                    "respMessage": "请求成功",
                    "status": "01",
                    "tenantId": "888",
                    "userId": self.idnum
                },
                "header": {
                    "channel": "10010000028",
                    "code": "000000",
                    "message": "访问成功",
                    "seqNo": "eae5532fa1834d68b7b9fb683b619348",
                    "timeStamp": "20230221104504728"
                }
            }
        }
        self.update(api, body)

    def update_upload_img(self, item_no, respCode='000000', respMessage='成功'):
        '''
        影像上传
        :return:
        '''
        api = '/weipin/weipin_zhongzhixin/customer/uploadImg'
        body = {
            "code": 0,
            "message": "success",
            "data": {
                "body": {
                    "creditApplyNo": item_no,
                    "respCode": respCode,
                    "respMessage": respMessage,
                    "tenantId": "888"
                },
                "header": {
                    "channel": "10010000028",
                    "code": "000000",
                    "message": "访问成功",
                    "seqNo": "51478e95c64f452bac0311efc783a3ad",
                    "timeStamp": "20230221104554262"
                }
            }
        }
        self.update(api, body)

    def update_open_account(self, item_no, respCode='000000', respMessage='渠道处理成功', status='S'):
        '''
        授信申请
        :return:
        '''
        api = '/weipin/weipin_zhongzhixin/credit/openAccount'
        body = {
            "code": 0,
            "message": "success",
            "data": {
                "body": {
                    "creditAppNo": item_no,
                    "respCode": respCode,
                    "respMessage": respMessage,
                    "status": status,
                    "tenantId": "888",
                    "userId": self.idnum
                },
                "header": {
                    "channel": "10010000028",
                    "code": "000000",
                    "message": "访问成功",
                    "seqNo": "fadf3314ee0b43b1933cffcae78a7692",
                    "timeStamp": "20230221104620427"
                }
            }
        }
        self.update(api, body)

    def update_query_credit_result(self, item_no, respCode='000000', respMessage='渠道处理成功', status='S'):
        '''
        授信申请查询
        :return:
        '''
        api = '/weipin/weipin_zhongzhixin/customer/queryCreditResult'
        body = {
            "code": 0,
            "message": "success",
            "data": {
                "body": {
                    "creditAppNo": item_no,
                    "creditLimit": 5000000,
                    "creditRate": 0.12,
                    "productId": "1201001030020",
                    "respCode": respCode,
                    "respMessage": respMessage,
                    "status": status,
                    "tenantId": "888",
                    "userId": self.idnum
                },
                "header": {
                    "channel": "10010000028",
                    "code": "000000",
                    "message": "访问成功",
                    "seqNo": "0803b5c784ad470aaaff8e28967cfe66",
                    "timeStamp": "20230221110600859"
                }
            }
        }
        self.update(api, body)

    def update_loan_apply(self, item_no, respCode='000000', respMessage='成功', status='S'):
        '''
        借款申请
        :return:
        '''
        api = '/weipin/weipin_zhongzhixin/loanService/loanApply'
        body = {
            "code": 0,
            "message": "success",
            "data": {
                "body": {
                    "contractNumber": item_no,  # 和我方无交互
                    "creditAppNo": item_no,
                    "loanAmount": "1000.0",
                    "loanId": item_no,
                    "productId": "1201001030020",
                    "respCode": respCode,
                    "respMessage": respMessage,
                    "status": status,
                    "tenantId": "888",
                    "tenor": "12",
                    "userId": self.idnum
                },
                "header": {
                    "channel": "10010000028",
                    "code": "000000",
                    "message": "访问成功",
                    "seqNo": "83a73e6e3b014235bd28dd66ce9c5b2f",
                    "timeStamp": "20230221110605486"
                }
            }
        }
        self.update(api, body)

    def update_loan_apply_result_query(self, item_no, respCode='000000', respMessage='成功', disbursementStatus='00',
                                       failreason=''):
        '''
        借款申请查询
        :return:
        '''
        api = '/weipin/weipin_zhongzhixin/loanService/loanApplyResultQuery'
        body = {
            "code": 0,
            "message": "success",
            "data": {
                "body": {
                    "completeTime": get_date(fmt="%Y%m%d%H%M%S"),
                    "creditAppNo": item_no,
                    "disbursementStatus": disbursementStatus,
                    "failreason": failreason,
                    "loanId": "8884120230221110704176651483746",  # 和我方无交互
                    "paymentPlanList": [],
                    "productId": "1201001030020",
                    "respCode": respCode,
                    "respMessage": respMessage,
                    "tenantId": "888",
                    "userId": self.idnum
                },
                "header": {
                    "channel": "10010000028",
                    "code": "000000",
                    "message": "访问成功",
                    "seqNo": "c44a421121a94dd495a12b44ee0b1b5a",
                    "timeStamp": "20230221111126204"
                }
            }
        }
        self.update(api, body)

    def update_repayplan_query(self, item_no, asset_info):
        '''
        还款计划查询
        :return:
        '''
        api = '/weipin/weipin_zhongzhixin/repayment/repaymentPlanQuery'
        rate_info = cmdb_rate_loan_calculate_v6(asset_info)
        body = {
            "code": 0,
            "message": "success",
            "data": {
                "body": {
                    "creditAppNo": item_no,
                    "loanId": "8884120230221110704176651483746",  # 和我发方无交互
                    "planList": [],
                    "productId": "1201001030020",
                    "respCode": "000000",
                    "respMessage": "访问成功",
                    "tenantId": "888",
                    "userId": self.idnum
                },
                "header": {
                    "channel": "10010000028",
                    "code": "000000",
                    "message": "访问成功",
                    "seqNo": "b653b3160f8e455591320342b0fba6cf",
                    "timeStamp": "20230221111603879"
                }
            }
        }
        planList = {
            "compoundAmount": 0,
            "delqDays": 0,
            "exemptAmount": 0,
            "feeAmount": 0,
            "interestAmount": 10,
            "payableCompoundInterest": 0,
            "payableFee": 0,
            "payableInterest": 10,
            "payablePenaltyInterest": 0,
            "payablePrincipal": 78.85,
            "paymentCompoundInterest": 0,
            "paymentDueDate": "20260707",
            "paymentFee": 0,
            "paymentFlag": "1",
            "paymentInterest": 0,
            "paymentPenaltyInterest": 0,
            "paymentPrincipal": 0,
            "penaltyIntAmount": 0,
            "principalAmount": 78.85,
            "tenor": 1,
            "totalAmount": 88.85,
            "waivedAmount": 0
        }
        for i in range(asset_info['data']['asset']['period_count']):
            fee_info = get_fee_info_by_period(rate_info, i + 1)
            repayment_plan = deepcopy(planList)
            repayment_plan['tenor'] = i + 1
            repayment_plan['payablePrincipal'] = float(fee_info['principal']) / 100
            repayment_plan['payableInterest'] = float(fee_info['interest']) / 100
            repayment_plan['totalAmount'] = repayment_plan['payablePrincipal'] + repayment_plan['payableInterest']
            repayment_plan['paymentDueDate'] = fee_info['date'].replace("-", "")
            body['data']['body']['planList'].append(repayment_plan)
        self.update(api, body)

    def update_contract_download(self, item_no):
        '''
        协议下载
        :return:
        '''
        api = '/weipin/weipin_zhongzhixin/contract/download'
        body = {
            "code": 0,
            "message": "成功",
            "data": {
                "respCode": "000000",
                "respMessage": "成功",
                "creditAppNo": item_no,
                "userId": "16530278743892430040",
                "contractList": [{
                    "contractType": "0007",
                    # 文件base64编码
                    "contractFile": "JVBER"
                },
                    {
                        "contractType": "0003",
                        "contractFile": "JVBER"
                    },
                    {
                        "contractType": "0002",
                        "contractFile": "JVBER"
                    },
                    {
                        "contractType": "0006",
                        "contractFile": "JVBER"
                    }
                ]
            }
        }
        self.update(api, body)

    def update_realtime_apply(self, item_no):
        '''
        担保合同签约
        :return:
        '''
        api = '/zhongzhixin/weipin_zhongzhixin/sign/realtime/apply'
        body = {
            "code": 0,
            "message": "成功",
            "data": {
                "fileId": "XNAB" + item_no,
                "status": "200",
                "reqNo": "9067d5db31ac4b318e096ca279f9ba9d",
                "msg": "成功"
            }
        }
        self.update(api, body)

    def update_realtime_query(self, item_no):
        '''
        担保合同下载
        :return:
        '''
        api = '/zhongzhixin/weipin_zhongzhixin/sign/realtime/query'
        body = {
            "code": 0,
            "message": "成功",
            "data": {
                "fileId": "XNAB" + item_no,
                "status": "200",
                "msg": "成功",
                "fileBase64": "JVB"
            }
        }
        self.update(api, body)
