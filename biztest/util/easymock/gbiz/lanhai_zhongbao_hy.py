# -*- coding: utf-8 -*-
from biztest.function.cmdb.cmdb_common_function import get_fee_info_by_period
from biztest.interface.cmdb.cmdb_interface import cmdb_rate_loan_calculate_v6
from biztest.util.easymock.easymock import Easymock
from copy import deepcopy
from biztest.util.tools.tools import get_date
from biztest.util.tools.tools import get_date_timestamp


class LanhaiZhongbaoHyMock(Easymock):
    def update_loan_pre_apply_new_user(self):
        """
        未授信过的新用户都会这样返回
        """
        api = '/hayin/lanhai_zhongbao_hy/api/limit/sumQuery'
        body = '''{
                    "serNo": "s@id",
                    "retCode": "E1007",
                    "retMsg": "授信信息不存在",
                    "reqSn": function({
                            _req
                          }) {
                            return _req.body.reqSn
                          },
                    "timestamp": "%s"
                }''' % (get_date(fmt="%Y-%m-%d %H:%M:%S"))
        self.update(api, body)

    def update_loan_pre_apply_old_user(self, retCode='0', retMsg='成功', restAmount=20000, amount=60000, lmtStatus='04',
                                       startDt=get_date(fmt="%Y-%m-%d"), endDt='2040-06-06 23:59:59'):
        """
        授信过的老用户会这样返回
        """
        api = '/hayin/lanhai_zhongbao_hy/api/limit/sumQuery'
        body = '''{
                    "serNo": "t@id",
                    "retCode": "%s",
                    "retMsg": "%s",
                    "reqSn": function({
                            _req
                          }) {
                            return _req.body.reqSn
                          },
                    "timestamp": "%s",
                    "basicInfo": {
                        "channelApplSeq": "@id", //老用户第一次授信申请时的流水号，即"第一次借款的资产编号+_1",mock时就随便写个
                        "lmtNo": "sx@id",
                        "restAmount": %s,  //剩余可用额度 -------会校验这个金额，需要大于等于借款本金
                        "lmtStatus": "%s",  //02：圈占；03：作废； 04：正常；05：冻结； 06：失效(过期)；
                        "amount": %s,  //授信额度(原始授信额度) -------不会校验这个字段值，只要有剩余可用额度就可以
                        "rate": "8.200000",
                        "custId": "C@id",  //哈银客户编号
                        "startDt": "%s",
                        "endDt": "%s"  //这个是授信额度到期时间，会校验时分秒，只要时分秒小于当前授信时间，就会授信失败，若大于就会授信成功
                    }
                }''' % (retCode, retMsg, get_date(fmt="%Y-%m-%d %H:%M:%S"), restAmount, lmtStatus, amount,
                        startDt + " 00:00:00", endDt)
        self.update(api, body)

    def update_loan_pre_apply_old_user_lose_effectiveness(self, startDt=get_date(fmt="%Y-%m-%d"), endDt='2040-06-06 23:59:59'):
        """
        授信过的老用户,额度失效了
        """
        api = '/hayin/lanhai_zhongbao_hy/api/limit/sumQuery'
        body = '''{
                       "serNo": "t@id",
                       "retCode": "0",
                       "retMsg": "mock成功",
                       "reqSn": function({
                               _req
                             }) {
                               return _req.body.reqSn
                             },
                       "timestamp": "%s",
                       "basicInfo": {
                           "channelApplSeq": "@id",
                           "lmtNo": "",
                           "restAmount": 20000,  
                           "lmtStatus": "06", 
                           "amount": 60000,  
                           "rate": "8.200000",
                           "custId": "c@id", 
                           "startDt": "%s",
                           "endDt": "%s" 
                       }
                   }''' % (get_date(fmt="%Y-%m-%d %H:%M:%S"), startDt + " 00:00:00", endDt)
        self.update(api, body)

    def update_image_upload(self, retCode="0"):
      api = '/hayin/lanhai_zhongbao_hy/api/image/upload'
      body = '''{
              "serNo": "S@id",
              "retCode": "%s",
              "timestamp": "%s",
              "reqSn":  function({
                            _req
                          }) {
                            return _req.body.reqSn
                          },
              "basicInfo": {
                "fileName": "001_1689845751159_410621198101268047_00.jpg",
                "fileId": "F@id"
              }
            }''' % (retCode, get_date_timestamp())
      self.update(api, body)

    def update_credit_apply(self, item_no, retCode="0", retMsg="成功", risCode="20000" ):
      api = '/hayin/lanhai_zhongbao_hy/api/credit/apply'
      body = {
              "serNo": "e@id",
              "retCode": retCode,
              "retMsg": retMsg,
              "reqSn": item_no + "_1",
              "timestamp": get_date(fmt="%Y-%m-%d %H:%M:%S"),
              "basicInfo": {
                "risCode": risCode  # 这个code 10000-审批通过； 90000-审批拒绝； 20000-处理中；
              }
            }
      self.update(api, body)

    def update_credit_query(self, asset_info, retCode="0", retMsg="成功", endDt='2036-12-31', risCode=10000,
                            investorApplyId='T@id'):
        api = '/hayin/lanhai_zhongbao_hy/api/credit/query'
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
                    "amount": %s, //单位元，这个金额必须要大于等于放款金额，这个是现在的校验
                    "rate": "0.24",
                    "custId": "@id",
                    "startDt": "%s",
                    "endDt": "%s", //实际上是起始时间+36H就是额度到期时间
                    "investorApplyId":"%s", //失败的时候不会返回，只有审批通过时会返回，返回了就会记录事件（就算是失败时返回也会记录事件），有这个值就有事件，有事件就可以下载额度合同
                    "risCode": "%s" //10000-审批通过； 90000-审批拒绝； 20000-处理中；
                  }
                }''' % (retCode, retMsg, get_date(fmt="%Y-%m-%d %H:%M:%S"), asset_info['data']['asset']['amount'],
                        get_date(fmt="%Y-%m-%d"), endDt, investorApplyId, risCode)
        self.update(api, body)

    def update_credit_query_amount_not_enough(self, amount=0, retCode="0", retMsg="成功", endDt='2036-12-31',
                                              risCode=10000, investorApplyId='T@id'):
        api = '/hayin/lanhai_zhongbao_hy/api/credit/query'
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
                     "amount": %s, //单位元，这个金额必须要大于等于放款金额，这个是现在的校验
                     "rate": "0.24",
                     "custId": "@id",
                     "startDt": "%s",
                     "endDt": "%s", //实际上是起始时间+36H就是额度到期时间
                     "investorApplyId":"%s", //失败的时候不会返回，只有审批通过时会返回，返回了就会记录事件（就算是失败时返回也会记录事件），有这个值就有事件，有事件就可以下载额度合同
                     "risCode": "%s" //10000-审批通过； 90000-审批拒绝； 20000-处理中；
                   }
                 }''' % (retCode, retMsg, get_date(fmt="%Y-%m-%d %H:%M:%S"), amount, get_date(fmt="%Y-%m-%d"), endDt, investorApplyId, risCode)
        self.update(api, body)


    def update_loanconfirm_apply(self, retCode="0",retMsg="成功"):
        api ='/hayin/lanhai_zhongbao_hy/api/use/apply'
        body = '''{
              "serNo": "u@id",
              "retCode": "%s",
              "retMsg": "%s",
              "reqSn": function({
                            _req
                          }) {
                            return _req.body.reqSn
                          },  //实际上就是资产编号+"_2"
              "timestamp": "%s"
            }''' % (retCode, retMsg, get_date(fmt="%Y-%m-%d %H:%M:%S"))
        self.update(api, body)

    def update_loanconfirm_query(self, asset_info, risCode="10000", dnSts=200):
        api ='/hayin/lanhai_zhongbao_hy/api/use/query'
        body = '''{
                  "serNo": "y@id",
                  "retCode": "0",
                  "retMsg": "成功",
                  "reqSn":  function({
                            _req
                          }) {
                            return _req.body.reqSn
                          },  //实际上就是资产编号+"_2"
                  "timestamp": "%s",
                  "basicInfo": {
                    "loanNo": "TL@id",  //存入asset_loan_record_due_bill_no
                    "payTime": "%s", //放款成功时间，这个时分秒没有，就用当前时间填充
                    "useAmt": "%s",  //暂时没有校验这个金额
                    "dnSts": "%s", //放款状态 100 未放款;200 放款成功;400 支付失败;450 支付处理中;800 放款冲正;900 放款失败
                    "risCode": "%s"  //10000-审批通过 90000-审批拒绝 20000-处理中
                  }
                }''' % (get_date(fmt="%Y-%m-%d %H:%M:%S"), get_date(fmt="%Y-%m-%d"), asset_info['data']['asset']['amount'],
                        dnSts, risCode)
        self.update(api, body)

    def update_repayplan_query(self, itemno, asset_info):
        rate_info = cmdb_rate_loan_calculate_v6(asset_info)
        api = '/hayin/lanhai_zhongbao_hy/api/loan/planQuery'
        body = {
              "serNo": "p@id",
              "retCode": "0",
              "retMsg": "成功",
              "reqSn": itemno + "_2",
              "timestamp": get_date(fmt="%Y-%m-%d %H:%M:%S"),
              "basicInfo": {
                "repayPlanDetail": []
              }
            }
        repay_plan_detail = {
                    "totalAmt": "1132.05",  # 总金额，似乎不校验
                    "actualInt": "0.00",
                    "inteAmt": "88.83",  # 应还利息
                    "actualPrcp": "0.00",
                    "repayDate": "20230924",  # 当期到期日
                    "termNo": "1",  # 期次
                    "prcp": "1043.22",  # 应还本金
                    "actualTotalAmt": "0.00"
                  }
        for i in range(asset_info['data']['asset']['period_count']):
          fee_info = get_fee_info_by_period(rate_info, i + 1)
          repayment_plan = deepcopy(repay_plan_detail)
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
        api = '/hayin/lanhai_zhongbao_hy/api/certify/apply'
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