# -*- coding: utf-8 -*-
from biztest.function.cmdb.cmdb_common_function import get_fee_info_by_period
from biztest.interface.cmdb.cmdb_interface import cmdb_rate_loan_calculate_v6
from biztest.util.easymock.easymock import Easymock
from copy import deepcopy
from biztest.util.tools.tools import get_date
from biztest.util.tools.tools import get_date_timestamp


class HayinZhongbaoMock(Easymock):

    def update_open_account_query(self):
        api = "/hayin/hayin_zhongbao/api/bind/query"
        body = '''{
                  "serNo": "a@id",
                  "retCode": "0",
                  "retMsg": "成功",
                  "reqSn":  function({
                            _req
                          }) {
                            return _req.body.reqSn
                          },  //这个时候这个参数是随机生成的
                  "timestamp": "%s",
                  "basicInfo": {}
                }''' % (get_date(fmt="%Y-%m-%d %H:%M:%S"))
        self.update(api, body)

    def update_old_user_open_account_query(self, four_element):
        api = "/hayin/hayin_zhongbao/api/bind/query"
        body = '''{
                  "serNo": "a@id",
                  "retCode": "0",
                  "retMsg": "成功",
                  "reqSn":  function({
                            _req
                          }) {
                            return _req.body.reqSn
                          },  //这个时候这个参数是随机生成的
                  "timestamp": "%s",
                  "basicInfo": {
                  "bankCards": [
                        {
                            "modifiedTime": "%s",
                            "bankCode": "CCB",
                            "bankCardNo": "%s",
                            "phone": "%s",
                            "isDeductCard": true,
                            "bankName": "中国建设银行",
                            "custName": "%s"
                        }
                    ]}
                }''' % (get_date(fmt="%Y-%m-%d %H:%M:%S"), get_date(fmt="%Y-%m-%d %H:%M:%S"),
                        four_element['data']['bank_code'], four_element['data']['phone_number'],
                        four_element['data']['user_name'])
        self.update(api, body)

    def update_account_bind_apply(self):
      api = '/hayin/hayin_zhongbao/api/bind/apply'
      body ='''{
              "serNo": "b@id",
              "retCode": "0",
              "retMsg": "成功",
               "reqSn":  function({
                            _req
                          }) {
                            return _req.body.reqSn
                          },  // 存入：capital_account_step_serial_no
              "timestamp": "%s",
              "basicInfo": {
                "bindSn": "@id"
              }
            }''' % (get_date(fmt="%Y-%m-%d %H:%M:%S"))
      self.update(api, body)

    def update_account_bind_confirm(self):
        api = '/hayin/hayin_zhongbao/api/bind/confirm'
        body = '''{
                  "serNo": "c@id",
                  "retCode": "0",
                  "retMsg": "成功",
                   "reqSn":  function({
                            _req
                          }) {
                            return _req.body.reqSn
                          },
                  "timestamp": "%s",
                  "basicInfo": {
                    "agrementNo": "T@id"  //存入capital_account_user_key中，但是未判断是否为空
                  }
                }''' % (get_date(fmt="%Y-%m-%d %H:%M:%S"))
        self.update(api, body)

    def update_image_upload_success(self):
        api = '/hayin/hayin_zhongbao/api/image/upload'
        body = '''{
                  "serNo": "d@id",
                  "retCode": "0",
                  "timestamp": "%s",
                   "reqSn":  function({
                            _req
                          }) {
                            return _req.body.reqSn
                          },
                  "basicInfo": {
                    "fileId": "F@id"
                  }
                }''' % (get_date_timestamp())
        self.update(api, body)

    def update_credit_apply(self, item_no, retCode="0", retMsg="成功", risCode="20000" ):
      api = '/hayin/hayin_zhongbao/api/credit/apply'
      body = {
              "serNo": "e@id",
              "retCode": retCode,
              "retMsg": retMsg,
              "reqSn": item_no,
              "timestamp": get_date(fmt="%Y-%m-%d %H:%M:%S"),
              "basicInfo": {
                "risCode": risCode  # 这个code 10000-审批通过； 90000-审批拒绝； 20000-处理中；开发说不校验这个参数
              }
            }
      self.update(api, body)

    def update_credit_query(self, asset_info, retCode="0", retMsg="成功", endDt='2036-12-31', risCode=10000):
        api = '/hayin/hayin_zhongbao/api/credit/query'
        body = '''{
              "serNo": "i@id",
              "retCode": "%s",
              "retMsg": "%s",
              "reqSn":  function({
                            _req
                          }) {
                            return _req.body.reqSn
                          },
              "timestamp": "%s",
              "basicInfo": {
                "lmtNo": "L@id", // 存入asset_loan_record_trade_no，用信申请时入参使用
                "amount": %s, //单位元，这个金额必须要等于放款金额，这个是现在的校验
                "rate": "0.24",
                "custId": "@id",
                "startDt": "%s",
                "endDt": "%s", //实际上是起始时间+36H就是额度到期时间
                "risCode": "%s" //10000-审批通过； 90000-审批拒绝； 20000-处理中；
              }
            }''' % (retCode, retMsg, get_date(fmt="%Y-%m-%d %H:%M:%S"), asset_info['data']['asset']['amount'], get_date(fmt="%Y-%m-%d"),
                    endDt, risCode)
        self.update(api, body)


    def update_loanconfirm_apply(self, retCode="0",retMsg="成功"):
        api ='/hayin/hayin_zhongbao/api/use/apply'
        body = '''{
              "serNo": "u@id",
              "retCode": "%s",
              "retMsg": "%s",
              "reqSn": function({
                            _req
                          }) {
                            return _req.body.reqSn
                          },  //实际上就是资产编号
              "timestamp": "%s"
            }''' % (retCode, retMsg, get_date(fmt="%Y-%m-%d %H:%M:%S"))
        self.update(api, body)

    def update_loanconfirm_query(self, asset_info, risCode="10000", dnSts=200):
        api ='/hayin/hayin_zhongbao/api/use/query'
        body = '''{
                  "serNo": "y@id",
                  "retCode": "0",
                  "retMsg": "成功",
                  "reqSn":  function({
                            _req
                          }) {
                            return _req.body.reqSn
                          },  //实际上就是资产编号
                  "timestamp": "%s",
                  "basicInfo": {
                    "loanNo": "hy@id",
                    "payTime": "%s", //放款成功时间，这个时分秒没有，就用当前时间填充
                    "useAmt": "%s", 
                    "dnSts": "%s", //放款状态 100 未放款;200 放款成功;400 支付失败;450 支付处理中;800 放款冲正;900 放款失败
                    "risCode": "%s"  //10000-审批通过 90000-审批拒绝 20000-处理中
                  }
                }''' % (get_date(fmt="%Y-%m-%d %H:%M:%S"), get_date(fmt="%Y-%m-%d"), asset_info['data']['asset']['amount'],
                        dnSts, risCode)
        self.update(api, body)

    def update_repayplan_query(self, itemno, asset_info):
        rate_info = cmdb_rate_loan_calculate_v6(asset_info)
        api = '/hayin/hayin_zhongbao/api/loan/planQuery'
        body = {
              "serNo": "p@id",
              "retCode": "0",
              "retMsg": "成功",
              "reqSn": itemno,
              "timestamp": get_date(fmt="%Y-%m-%d %H:%M:%S"),
              "basicInfo": {
                "repayPlanDetail": []
              }
            }

        payschedule = {
                    "reductionCompoundIntr": "0",
                    "actualInt": "0",
                    "redOverduePrcp": "0",
                    "reductionServiceCharge": "0",
                    "actualTotalAmt": "0",
                    "actualServiceCharge": "0",
                    "reductionLateFee": "0",
                    "serviceCharge": "0",
                    "deductAmt": "0",
                    "borrowServiceFee": "0",
                    "reductionBorrowServiceFee": "0",
                    "reductionTotalAmt": "0",
                    "redServiceCharge": "0",
                    "repaymentPlanStatus": "0",
                    "prcp": "591.06",  # 应还本金
                    "reductionPrincipal": "0",
                    "serviceFee": "0",
                    "actualDefaultFee": "0",
                    "actualOverduePrcp": "0",
                    "inteAmt": "165.42",  # 应还利息
                    "reductionInterest": "0",
                    "overdueInt": "0",
                    "redBorrowServiceFee": "0",
                    "actualServiceFee": "0",
                    "totalAmt": "756.48",  # 总金额，似乎不校验
                    "guarFee": "0",
                    "redLateFee": "0",
                    "actualPrcp": "0",
                    "lateFee": "0",
                    "redLineReduceAmt": "0",
                    "repayDate": "20230929",  # 当期到期日
                    "actualLateFee": "0",
                    "termNo": "1",  # 期次
                    "overduePrcp": "0",
                    "reductionPenaltyIntr": "0",
                    "reductionServiceFee": "0",
                    "redInterest": "0",
                    "actualGuarFee": "0",
                    "redDefaultFee": "0",
                    "actualOverdueInt": "0",
                    "actualBorrowServiceFee": "0"
                  }
        for i in range(asset_info['data']['asset']['period_count']):
          fee_info = get_fee_info_by_period(rate_info, i + 1)
          repayment_plan = deepcopy(payschedule)
          repayment_plan['termNo'] = i + 1
          repayment_plan['prcp'] = float(fee_info['principal'])/100
          repayment_plan['inteAmt'] = float(fee_info['interest'])/100
          repayment_plan['repayDate'] = str(fee_info['date']).replace('-', '')
          body['basicInfo']['repayPlanDetail'].append(repayment_plan)
        self.update(api, body)



    def update_certificate_apply(self):
        """
        申请结清证明接口
        status：
            INIT-未处理（暂无）
            PROC-申请处理中
            SUCC-开具证明成功
            FAIL-开具证明失败
        """
        api = '/hayin/hayin_zhongbao/api/certify/apply'
        body = '''{
                  "serNo": "K@id",
                  "retCode": "0",
                  "retMsg": "成功",
                  "reqSn":  function({
                            _req
                          }) {
                            return _req.body.reqSn
                          }, 
                  "timestamp": "%s",
                  "basicInfo": {
                    "status": "SUCC"
                  }
                }''' % (get_date(fmt="%Y-%m-%d %H:%M:%S"))
        self.update(api, body)