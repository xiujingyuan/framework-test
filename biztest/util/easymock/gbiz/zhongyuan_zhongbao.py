# -*- coding: utf-8 -*-
from biztest.function.cmdb.cmdb_common_function import get_fee_info_by_period
from biztest.interface.cmdb.cmdb_interface import cmdb_rate_loan_calculate_v6
from biztest.util.easymock.easymock import Easymock
from biztest.function.gbiz.gbiz_db_function import get_asset_loan_record_by_item_no
from copy import deepcopy
from biztest.util.tools.tools import *
from biztest.function.gbiz.gbiz_check_function import get_asset_event


class ZhongYuanZhongBaoMock(Easymock):
    def update_route_access(self, code='0000000', message='操作成功', checkflag='Y'):
        """
        路由准入接口
        checkFlag 检查结果
            Y 通过
            N 不通过
        """
        api = "/zhongbao/zhongyuan_zhongbao/ZYXF004/indicator/qualifyMd5"
        body = {
                "code": code,
                "message": message,
                "data": {
                    "checkFlag": checkflag,
                    "checkMsgNo": None,
                    "checkMsg": None
                }
            }
        self.update(api, body)

    def update_get_sms(self, code='0000000', message='操作成功', checkflag='Y'):
        """
        开户：获取短信验证码
        checkFlag 鉴权结果
            Y 通过
            N 未通过
        """
        api = "/zhongbao/zhongyuan_zhongbao/ZYXF001/indicator/bindingCard"
        body = {
                "code": code,
                "message": message,
                "data": {
                    "checkFlag": checkflag,
                    "checkMsg": "通过",
                    "refuseNo": None,
                    "refuseCause": None,
                    "payCardFlag": "Y",
                    "reimburseCardFlag": "Y",
                    "senderFlag": "TLZFXPAY",
                    "uniqueCode": "tqy@id",  # 预签约协议号
                    "channelRepayId": None,
                    "bankChannel": None
                }
            }
        self.update(api, body)

    def update_checkcmsverifycode(self, code='0000000', message='操作成功', checkflag='Y'):
        """
        开户：开户验证 ------与开户获取短信验证码是同一个接口
        checkFlag 鉴权结果
            Y 通过
            N 未通过
        """
        api = "/zhongbao/zhongyuan_zhongbao/ZYXF001/indicator/bindingCard"
        body = {
                "code": code,
                "message": message,
                "data": {
                    "checkFlag": checkflag,
                    "checkMsg": "通过",
                    "refuseNo": None,
                    "refuseCause": None,
                    "payCardFlag": "Y",
                    "reimburseCardFlag": "Y",
                    "senderFlag": None,
                    "uniqueCode": None,
                    "channelRepayId": "At@id",  # 客户协议id
                    "bankChannel": "TLZFXPAY"
                }
            }
        self.update(api, body)
    def update_loan_preapply(self, code='0000000', message='操作成功'):
        """
        客户信息维护接口
        """
        api = "/zhongbao/zhongyuan_zhongbao/ZYXF003/indicator/customerInfoMaintenance"
        body = {
                "code": code,
                "message": message,
                "data": {
                    "custId": "@id"
                }
            }
        self.update(api, body)

    def update_post_apply(self, code='0000000', message='操作成功', retsinal='Y'):
        """
        影像文件同步通知接口
        retSinal 处理结果标识
                Y:处理成功
                N:处理失败
        """
        api = "/zhongbao/zhongyuan_zhongbao/ZYXFA107/indicator/imageFileSynNotification"
        body = {
                "code": code,
                "message": message,
                "data": {
                    "retSinal": retsinal,
                    "retCode": None,
                    "retDesc": None,
                    "listFileInfo": [
                        {
                            "fileType": "01",
                            "fileName": "01_0125_115218_e29bcef3-e31b-457e-8184-fb5f0f87e660.jpg",
                            "fileAddress": None,
                            "imageId": "c720ce4e6cf74b0ab73df49b581a4355"
                        },
                        {
                            "fileType": "02",
                            "fileName": "02_0125_115218_e29bcef3-e31b-457e-8184-fb5f0f87e660.jpg",
                            "fileAddress": None,
                            "imageId": "c86993f37191477eab4c68278fa5f6f7"
                        },
                        {
                            "fileType": "04",
                            "fileName": "04_0125_115218_e29bcef3-e31b-457e-8184-fb5f0f87e660.jpg",
                            "fileAddress": None,
                            "imageId": "979290b8bb904f4b828784e9f72f1d07"
                        }
                    ]
                }
            }
        self.update(api, body)

    def update_confirm_get_lpr(self, code='0000000', message='操作成功'):
        """
        LPR定价查询
        """
        api = "/zhongbao/zhongyuan_zhongbao/ZYXF080/indicator/queryLprInfo"
        body = {
                "code": code,
                "message": message,
                "data": {
                    "listLprInfo": [
                        {
                            "lprRateType": "02",
                            "lprMapriceIssueDt": "2021-10-20",
                            "lprIssueMaprice": "0.03500000"
                        },
                        {
                            "lprRateType": "01",
                            "lprMapriceIssueDt": "2021-10-20",
                            "lprIssueMaprice": "0.03500000"
                        }
                    ]
                }
            }
        self.update(api, body)

    def update_loan_confirm(self, code='0000000', message='操作成功', checkflag='Y'):
        """
        借款申请（含准入检查)
        checkFlag检查结果
            Y 通过
            N 不通过
        """
        api = "/zhongbao/zhongyuan_zhongbao/ZYXFD56/indicator/creditApply"
        body = '''{
                "code": "%s",
                "message": "%s",
                "data": {
                    "applCde": function({
                            _req
                          }) {
                            return _req.body.applCde
                          }, 
                    "cooppfApplCde": function({
                            _req
                          }) {
                            return _req.body.cooppfApplCde
                          }, 
                    "applSeq": "Ac@id",  //存入asset_loan_record_trade_no ，但是没有返回也不会报错，不校验是否为空
                    "checkFlag": "%s",
                    "checkMsgNo": null,
                    "checkMsg": null,
                    "accsDnyFlag": null
                }
            }''' % (code, message, checkflag)
        self.update(api, body)


    def update_loan_confirm_query(self, asset_info, code='0000000', message='操作成功', outSts='99',endMark='01'):
        """
        申请状态查询
        outSts	申请状态
            20 审批中
            88 待银行处理
            99 结束
        endMark	结束标志 (仅申请状态为99时此字段有效)
                 01 通过
                 02 否决
                 03 取消
        """
        api = "/zhongbao/zhongyuan_zhongbao/ZYXFD06/indicator/applyStateQuery"
        body = '''{
                    "code": "%s",
                    "message": "%s",
                    "data": {
                        "listApproveInfo": [
                            {
                                "applCde": "83012023052380",
                                "cooppfApplCde": function({
                                            _req
                                          }) {
                                            return _req.body.cooppfApplCde
                                          },  //实际上这个字段值为资产编号
                                "applSeq": "LC202305230000010893",
                                "loanTyp": "PDI0412",
                                "contTyp": "01",
                                "outSts": "%s",
                                "endMark": "%s",
                                "applyAmt": %s,
                                "apprvAmt": %s, //审批金额
                                "applyDt": "%s",
                                "refuseNo": null,
                                "refuseCause": null,
                                "contNo": "Ct@id", //合同编号，存入asset_loan_record_identifier，会校验是否为空
                                "loanNo": "Tj@id", //借据编号, 存入asset_loan_record_due_bill_no，要校验是否为空
                                "apprvTnr": "12",
                                "apprvDt": "%s",
                                "mtdCde": "SYS002",
                                "fkCardNo": "5522450413723250",
                                "purpose": "TRA",
                                "loanActvDt": "%s", //借据生效日期
                                "loanActvTime": "%s", //放款成功时间
                                "dayIntRat": 0.000233,
                                "defaultRat": 0,
                                "dayDefaultRat": 0
                            }
                        ]
                    }
                }''' % (code, message, outSts, endMark, asset_info['data']['asset']['amount'],
                        asset_info['data']['asset']['amount'], get_date(fmt="%Y-%m-%d %H:%M:%S"),
                        get_date(fmt="%Y-%m-%d %H:%M:%S"), get_date(fmt="%Y-%m-%d"), get_date(fmt="%Y-%m-%d %H:%M:%S"))
        self.update(api, body)

    def update_repayplan_query(self,  item_no, asset_info):
        rate_info = cmdb_rate_loan_calculate_v6(asset_info)
        alr = get_asset_loan_record_by_item_no(item_no)
        loanno = alr[0].get('asset_loan_record_due_bill_no')
        api = '/zhongbao/zhongyuan_zhongbao/ZYXFA21/indicator/repaymentPlanQuery'
        body = {
              "code": "0000000",
              "message": "操作成功",
              "data": {
                "listLmLoan": [
                  {
                    "loanNo": loanno,
                    "dnSeq": "Lpb@id",
                    "tkCooppfApplCde": item_no,
                    "loanDebtSts": "NORM",
                    "curSetlserviceFeeAmt": 0,
                    "loanTnr": "12",
                    "loanActvDt": get_date(fmt="%Y-%m-%d"),  # 借据起息日期
                    "acIntFlag": "N",
                    "listLmShd": []
                  }
                ]
              }
            }
        repayplan_tmp = {
                        "psPerdNo": 1,
                        "psDueDt": "2029-05-28",  # 应还款日期
                        "payDt": None,
                        "psInstmAmt": 1133.86,  # 应还总额
                        "psPerdAmt": 1133.86,
                        "psPrcpAmt": 1043.04,  # 应还本金
                        "psNormInt": 90.82,  # 应还利息
                        "feeSumAmt": 0,
                        "penalFeeAmt": 0,
                        "psOdIntAmt": 0.00,
                        "psRemPrcp": 11956.96,
                        "setlInstmAmt": 0.00,
                        "setlPrcp": 0.00,
                        "setlNormInt": 0.00,
                        "setlOdIntAmt": 0.00,
                        "setlFeeAmtS": 0,
                        "setlPenalFeeAmt": 0,
                        "amortPrimeAmt": 0,
                        "psWvNmInt": 0.00,
                        "psWvOdInt": 0.00,
                        "psWvFeeAmt": 0.00,
                        "psSts": "1",
                        "psOdInd": "N",
                        "lastSetlDt": None,
                        "hkTyp": "N",
                        "graceDays": None,
                        "psOldDueDt": "2029-05-28",
                        "psValueDay": "2029-04-28",
                        "notSetlPrefrAmt": 0,
                        "ps_disc_sts": "0"
                      }
        for i in range(asset_info['data']['asset']['period_count']):
            fee_info = get_fee_info_by_period(rate_info, i + 1)
            repayment_plan = deepcopy(repayplan_tmp)
            repayment_plan['psPerdNo'] = i + 1
            repayment_plan['psPrcpAmt'] = float(fee_info['principal']) / 100
            repayment_plan['psNormInt'] = float(fee_info['interest']) / 100
            repayment_plan['psDueDt'] = fee_info['date']
            body['data']['listLmLoan'][0]['listLmShd'].append(repayment_plan)
        self.update(api, body)


