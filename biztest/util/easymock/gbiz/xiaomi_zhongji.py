from biztest.function.cmdb.cmdb_common_function import get_fee_info_by_period
from biztest.interface.cmdb.cmdb_interface import cmdb_rate_loan_calculate_v6
from biztest.util.easymock.easymock import Easymock
from copy import deepcopy
from biztest.util.tools.tools import get_date
from biztest.function.gbiz.gbiz_db_function import get_asset_loan_record_by_item_no

class XiaomiZhongjiMock(Easymock):

    def update_loan_pre_apply(self, code="000000", message="成功", limitState ="3", remainLimit="0", creditLimit="0",
                              endDate="" , startDate="", credNo=""):
        """
        额度信息查询接口
        limitState	额度状态
            0	正常(已激活)
            1	冻结
            2	失效
            3	未签约激活
            非0状态都需要走授信流程
        备注limitState=0时，想要成功则：
            startDate 必须小于等于进件当日
            endDate 必须大于进件当日
            remainLimit必须大于等于借款金额
            creditLimit不校验
        """
        api = "/xiaomi/xiaomi_zhongji/02B176"
        body = '''{
                "code": "%s",
                "message": "%s",
                "data": {
                    "limitState": "%s",
                    "endDate": "%s",  // 状态非0的时候为空字符串
                    "remainLimit": "%s",  // 状态非0的时候为0
                    "creditLimit": "%s",  // 状态非0的时候为0
                    "startDate": "%s",  // 状态非0的时候为空字符串
                    "credNo": "%s",  // 这个值会存入事件表中，成功之时不可为空
                }
            }''' % (code, message, limitState, endDate, remainLimit, creditLimit, startDate, credNo)
        self.update(api, body)

    def update_loan_apply(self, item_no, code="000000", result="W", message="成功"):
        """
        授信申请接口
        result	交易处理状态
            S	成功
            F	失败
            W	处理中
        """
        api = "/xiaomi/xiaomi_zhongji/02B172"
        body = {
                "code": code,
                "message": message,
                "data": {
                    "result": result,
                    "serialNo": "CA"+item_no
                }
            }
        self.update(api, body)

    def update_loan_apply_query(self, asset_info,  code="000000", result="S", message="成功"):
        """
        授信结果查询接口
        result	交易处理状态
            S	成功
            F	失败
            W	处理中
        """
        api = "/xiaomi/xiaomi_zhongji/02B173"
        body = {
                "code": code,
                "message": message,
                "data": {
                    "result": result,
                    "creditRateType": "D",
                    "creditRate": "0.00066660",
                    "credNo": "L@id",  # 这个值会存入事件表中，成功之时不可为空
                    "capitalCreditAmt": asset_info['data']['asset']['amount']
                }
            }
        self.update(api, body)

    def update_loan_apply_query_fail(self):
        api = "/xiaomi/xiaomi_zhongji/02B173"
        body = {
            "code": "000000",
            "message": "mock授信额度不足",
            "data": {
                "result": "S",
                "creditRateType": "D",
                "creditRate": "0.00066660",
                "credNo": "L@id",
                "capitalCreditAmt": "10.00"
            }
        }
        self.update(api, body)


    def update_loan_post_apply(self):
        """
        支用审批及放款申请前协议查询
        """
        api = "/xiaomi/xiaomi_zhongji/02B180"
        body = '''{
                "code": "000000",
                "message": "成功",
                "data": {
                    "capitalProtocolNoList": [],
                    "serialNo":  function({
                      _req
                    }) {
                      return _req.body.serialNo
                    }
                }
            }'''
        self.update(api, body)


    def update_loan_post_apply_have_protocol_no(self):
        """
        支用审批及放款申请前协议查询
        """
        api = "/xiaomi/xiaomi_zhongji/02B180"
        body = '''{
                "code": "000000",
                "message": "成功",
                "data": {
                    "capitalProtocolNoList": [{
                 "protocolNo": "000044442222_1002"
                }],
                    "serialNo":  function({
                      _req
                    }) {
                      return _req.body.serialNo
                    }
                }
            }'''
        self.update(api, body)


    def update_loan_apply_confirm(self, code="000000", result="S", message="成功"):
        """
        支用审批及放款申请
        result	交易处理状态
            S	成功
            F	失败
            W	处理中
        """
        api = "/xiaomi/xiaomi_zhongji/02B174"
        body = '''{
                "code": "%s",
                "message": "%s",
                "data": {
                    "result": "%s",
                    "serialNo":  function({
                      _req
                    }) {
                      return _req.body.serialNo
                    }
                }
            }''' % (code, message, result)
        self.update(api, body)

    def update_loan_apply_confirm_query(self, asset_info, code="000000", payStatus="S", message="成功"):
        """
        支用审批及放款结果查询
        result	交易处理状态
            S	成功
            F	失败
            W	处理中
        """
        api = "/xiaomi/xiaomi_zhongji/02B175"
        body = '''{
                "code": "%s",
                "message": "%s",
                "data": {
                    "dueBillNo": "T@id",
                    "capitalMode": "2", //1是老模式，2是联合贷模式-新的
                    "capitalInfoList": [
                        {
                            "capitalName": "小米消金",
                            "mainCapitalFlag": "Y",
                            "capitalRate": "1",
                            "capitalCode": "000044442222"
                        }
                    ],
                    "loanAmt": "%s",
                    "payStatus": "%s",
                    "payDate": "%s",
                    "serialNo":  function({
                      _req
                    }) {
                      return _req.body.serialNo
                    }
                }
            }''' % (code, message, asset_info['data']['asset']['amount'], payStatus, get_date(fmt="%Y-%m-%d"))
        self.update(api, body)

    def update_repayplan_query(self, item_no, asset_info):
        rate_info = cmdb_rate_loan_calculate_v6(asset_info)
        alr = get_asset_loan_record_by_item_no(item_no)
        loanno = alr[0].get('asset_loan_record_due_bill_no')
        api = '/xiaomi/xiaomi_zhongji/04B176'
        body = {
              "code": "000000",
              "message": "成功",
              "data": {
                "scheduleList": [],
                "dueBillNo": loanno,
                "loanInitPrin": asset_info['data']['asset']['amount'],
                "loanStatus": "A",
                "overDueDate": "",
                "currTermNo": 1,
                "capitalMode": "1",
                "capitalInfoList": [
                  {
                    "capitalName": "小米消金",
                    "mainCapitalFlag": "Y",
                    "capitalRate": 1,
                    "capitalCode": "000044442222"
                  }
                ],
                "loanInitTerm": 12
              }
            }
        scheduleList = {
                    "overDueDays": 0,
                    "pmtDueDate": "2024-05-07",
                    "prinTermPaid": 0,
                    "clearDate": "",
                    "pmtStartDate": "2024-04-07",  # 不校验这个参数
                    "repayTermInterest": 259.97,
                    "repayTermPenalty": 0,
                    "repayTermPrin": 969.29,
                    "termStatus": "A",
                    "interestTermPaid": 0,
                    "termNo": 1,
                    "penaltyTermPaid": 0
                  }
        for i in range(asset_info['data']['asset']['period_count']):
            fee_info = get_fee_info_by_period(rate_info, i + 1)
            repayment_plan = deepcopy(scheduleList)
            repayment_plan['termNo'] = i + 1
            repayment_plan['repayTermPrin'] = float(fee_info['principal']) / 100
            repayment_plan['repayTermInterest'] = float(fee_info['interest']) / 100
            repayment_plan['pmtDueDate'] = str(fee_info['date'])
            body['data']['scheduleList'].append(repayment_plan)
        self.update(api, body)

    def update_contract_signature_query(self):
        """
        凭证开立结果查询
        result	处理状态
            0	开立中
            1	开立完成
            2	不符合开立条件
        """
        api = "/xiaomi/xiaomi_zhongji/02B177"
        body = '''{
                    "code": "000000",
                    "message": "成功",
                    "data": {
                        "result": "0", //0和1状态都算作成功
                         "serialNo":  function({
                      _req
                    }) {
                      return _req.body.serialNo
                    }
                    }
                }'''
        self.update(api, body)

    def update_certificateapply_success(self):
        """
        凭证开立结果查询
        result	处理状态
            0	开立中
            1	开立完成
            2	不符合开立条件
        """
        api = "/xiaomi/xiaomi_zhongji/02B177"
        body = '''{
                    "code": "000000",
                    "message": "成功",
                    "data": {
                        "result": "0", //0和1状态都算作成功,一般只会返回0状态
                         "serialNo":  function({
                      _req
                    }) {
                      return _req.body.serialNo
                    }
                    }
                }'''
        self.update(api, body)

    def update_certificatedownload_success(self):
        """
        凭证开立结果查询
        result	处理状态
            0	开立中
            1	开立完成
            2	不符合开立条件
        """
        api = "/xiaomi/xiaomi_zhongji/02B184"
        body = '''{
                    "code": "000000",
                    "message": "成功",
                    "data": {
                        "result": "1",
                        "serialNo": function({
                      _req
                    }) {
                      return _req.body.serialNo
                    }
                    }
                }'''
        self.update(api, body)
