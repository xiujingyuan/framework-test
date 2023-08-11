# -*- coding: utf-8 -*-
from biztest.function.cmdb.cmdb_common_function import get_fee_info_by_period
from biztest.interface.cmdb.cmdb_interface import cmdb_rate_loan_calculate_v6
from biztest.util.easymock.easymock import Easymock
from copy import deepcopy
from biztest.util.tools.tools import get_guid, get_date
from biztest.function.gbiz.gbiz_db_function import get_asset_loan_record_by_item_no, get_asset_info_by_item_no


class LangfangHengrunQjMock(Easymock):
    def update_loan_apply(self, sendflag='01', errocode='000000', sendcode='0000', sendmsg='成功', errormsg='成功'):
        """
        sendflag 业务结果
                00 处理中
                01 处理成功
                02处理失败
        """
        api = "/qingjia/langfang_hengrun_qj/loanBaseInfoPush"
        mode = {
                    "code": 0,
                    "message": "success",
                    "data": {
                        "channel": "KN10001",
                        "errocode": errocode,
                        "errormsg": errormsg,
                        "respdate": get_date(fmt="%Y%m%d"),
                        "resptime": get_date(fmt="%H%M%S"),
                        "sendcode": sendcode,
                        "sendflag": sendflag,
                        "sendmsg": sendmsg,
                        "trancode": "QLZS000000001",
                        "transerno": "TK@id",
                        "transtate": "S"
                    }
                }
        self.update(api, mode)

    def update_contract_create(self, sendflag='01', errocode='000000', sendcode='0000', sendmsg='成功', errormsg='成功'):
        """
         和任务 LoanApplyQuery调用的是同一个接口，但是返回值不一样，所以此处重写
        sendflag 业务结果
                00 处理中
                01 处理成功
                02 处理失败
        """
        api = "/qingjia/langfang_hengrun_qj/contractCreate"
        mode = {
                "code": 0,
                "message": "success",
                "data": {
                    "channel": "KN10001",
                    "errocode": errocode,
                    "errormsg": errormsg,
                    "filelist": [
                        {
                            "filetype": "lfcredit",
                            "fileurl": "http://qjosstest.oss-cn-beijing.aliyuncs.com/data/cpu/router/temp/1125455002214674432.pdf?Expires=1688374582&OSSAccessKeyId=LTAI5tESd45p5Gt7uJ7Ww1Pe&Signature=F9e8AKSO%2FJGfdJ1vCLBrF5gxEKk%3D",
                            "signpoint": "{\"persion_post_y\":\"230F\",\"persion_post_x\":\"207F\",\"persion_post_page\":\"1\"}",
                            "weburl": "https://openapitest.qinjia001.com/contract/langfangauthchaxun.html"
                        },
                        {
                            "filetype": "lfquery",
                            "fileurl": "http://qjosstest.oss-cn-beijing.aliyuncs.com/data/cpu/router/temp/1125455003280027648.pdf?Expires=1688374582&OSSAccessKeyId=LTAI5tESd45p5Gt7uJ7Ww1Pe&Signature=noX5aA0AHw9rU9U%2Bq7xLU0owidQ%3D",
                            "signpoint": "{\"persion_post_y\":\"349F\",\"persion_post_x\":\"436F\",\"persion_post_page\":\"3\"}",
                            "weburl": "https://openapitest.qinjia001.com/contract/langfangauthshiyong.html"
                        },
                        {
                            "contractno": "1093847172043059202",
                            "filetype": "lflimit",
                            "fileurl": "http://qjosstest.oss-cn-beijing.aliyuncs.com/data/cpu/router/temp/1125455004504764416.pdf?Expires=1688374583&OSSAccessKeyId=LTAI5tESd45p5Gt7uJ7Ww1Pe&Signature=dtxh1XXh58EmS12NGUb0Giy%2BvMw%3D",
                            "signpoint": "{\"persion_post_y\":\"129F\",\"persion_post_x\":\"182F\",\"persion_post_page\":\"1\"}",
                            "weburl": "https://openapitest.qinjia001.com/contract/langfanglimit.html"
                        },
                        {
                            "filetype": "lhcredit",
                            "fileurl": "http://qjosstest.oss-cn-beijing.aliyuncs.com/data/cpu/router/temp/1125455005620449280.pdf?Expires=1688374583&OSSAccessKeyId=LTAI5tESd45p5Gt7uJ7Ww1Pe&Signature=%2FTRSkqV8%2BReSY3NadFnL8OCIM40%3D",
                            "signpoint": "{\"persion_post_y\":\"370F\",\"persion_post_x\":\"265F\",\"persion_post_page\":\"2\"}",
                            "weburl": "https://openapitest.qinjia001.com/contract/lanhairenhang.html"
                        },
                        {
                            "filetype": "lhquery",
                            "fileurl": "http://qjosstest.oss-cn-beijing.aliyuncs.com/data/cpu/router/temp/1125455006656442368.pdf?Expires=1688374583&OSSAccessKeyId=LTAI5tESd45p5Gt7uJ7Ww1Pe&Signature=%2Fgllv4W9KriCDKqRX3%2FpBHn0TAY%3D",
                            "signpoint": "{\"persion_post_y\":\"180F\",\"persion_post_x\":\"400F\",\"persion_post_page\":\"2\"}",
                            "weburl": "https://openapitest.qinjia001.com/contract/lanhaiauth.html"
                        },
                        {
                            "filetype": "lhlimit",
                            "fileurl": "http://qjosstest.oss-cn-beijing.aliyuncs.com/data/cpu/router/temp/1125455007944093696.pdf?Expires=1688374583&OSSAccessKeyId=LTAI5tESd45p5Gt7uJ7Ww1Pe&Signature=WFGIT1cy8Q4o5kF5VODWLRcp2wI%3D",
                            "signpoint": "{\"persion_post_y\":\"512F\",\"persion_post_x\":\"200F\",\"persion_post_page\":\"7\"}",
                            "weburl": "https://openapitest.qinjia001.com/contract/lanhailimit.html"
                        },
                        {
                            "filetype": "lhregion",
                            "fileurl": "http://qjosstest.oss-cn-beijing.aliyuncs.com/data/cpu/router/temp/1125455009168830464.pdf?Expires=1688374584&OSSAccessKeyId=LTAI5tESd45p5Gt7uJ7Ww1Pe&Signature=nxOxj2PGHRRYkU%2F%2Bh0QA3kI71CM%3D",
                            "signpoint": "{\"persion_post_y\":\"480F\",\"persion_post_x\":\"430F\",\"persion_post_page\":\"1\"}",
                            "weburl": "https://openapitest.qinjia001.com/contract/lanhairegion.html"
                        },
                        {
                            "filetype": "lzcredit",
                            "fileurl": "http://qjosstest.oss-cn-beijing.aliyuncs.com/data/cpu/router/temp/1125455010242572288.pdf?Expires=1688374584&OSSAccessKeyId=LTAI5tESd45p5Gt7uJ7Ww1Pe&Signature=5yUYIhD%2Fny9LroTwxVk%2Ff8nAvf8%3D",
                            "signpoint": "{\"persion_post_y\":\"242F\",\"persion_post_x\":\"203F\",\"persion_post_page\":\"1\"}",
                            "weburl": "https://openapitest.qinjia001.com/contract/lanzhouauth.html"
                        },
                        {
                            "filetype": "qjcredit",
                            "fileurl": "http://qjosstest.oss-cn-beijing.aliyuncs.com/data/cpu/router/temp/1125455011303731200.pdf?Expires=1688374584&OSSAccessKeyId=LTAI5tESd45p5Gt7uJ7Ww1Pe&Signature=J3uy%2FXYPbNgg0b0TYQuFb04a5Ak%3D",
                            "signpoint": "{\"persion_post_y\":\"679F\",\"persion_post_x\":\"460F\",\"persion_post_page\":\"2\"}",
                            "weburl": "https://openapitest.qinjia001.com/contract/qinjiaauth.html"
                        },
                        {
                            "filetype": "ylcredit",
                            "fileurl": "http://qjosstest.oss-cn-beijing.aliyuncs.com/data/cpu/router/temp/1125455012473942016.pdf?Expires=1688374585&OSSAccessKeyId=LTAI5tESd45p5Gt7uJ7Ww1Pe&Signature=9ocU3oSmWT6SP7YkhnecQJIxgHE%3D",
                            "signpoint": "{\"persion_post_y\":\"256F\",\"persion_post_x\":\"260F\",\"persion_post_page\":\"2\"}",
                            "weburl": "https://openapitest.qinjia001.com/contract/yilianzhengxinshouquan.html"
                        },
                        {
                            "filetype": "ylquery",
                            "fileurl": "http://qjosstest.oss-cn-beijing.aliyuncs.com/data/cpu/router/temp/1125455013744816128.pdf?Expires=1688374585&OSSAccessKeyId=LTAI5tESd45p5Gt7uJ7Ww1Pe&Signature=%2B%2FwM6PTOUDJVmZVBcaiqUaEGUGE%3D",
                            "signpoint": "{\"persion_post_y\":\"250F\",\"persion_post_x\":\"225F\",\"persion_post_page\":\"3\"}",
                            "weburl": "https://openapitest.qinjia001.com/contract/yilianauthchaxun.html"
                        },
                        {
                            "filetype": "yluse",
                            "fileurl": "http://qjosstest.oss-cn-beijing.aliyuncs.com/data/cpu/router/temp/1125455014969552896.pdf?Expires=1688374585&OSSAccessKeyId=LTAI5tESd45p5Gt7uJ7Ww1Pe&Signature=78wub2NusLmKGZpA75y%2F2hUqwxs%3D",
                            "signpoint": "{\"persion_post_y\":\"250F\",\"persion_post_x\":\"225F\",\"persion_post_page\":\"3\"}",
                            "weburl": "https://openapitest.qinjia001.com/contract/yilianauthshiyong.html"
                        },
                        {
                            "filetype": "ylamountcontract",
                            "fileurl": "http://qjosstest.oss-cn-beijing.aliyuncs.com/data/cpu/router/temp/1125455016248815616.pdf?Expires=1688374585&OSSAccessKeyId=LTAI5tESd45p5Gt7uJ7Ww1Pe&Signature=uX1PeWu6pwGOCAKxLFvygkPwGlY%3D",
                            "signpoint": "{\"persion_post_y\":\"578F\",\"persion_post_x\":\"440F\",\"persion_post_page\":\"11\"}",
                            "weburl": "https://openapitest.qinjia001.com/contract/gerenedu.html"
                        },
                        {
                            "filetype": "ylpromise",
                            "fileurl": "http://qjosstest.oss-cn-beijing.aliyuncs.com/data/cpu/router/temp/1125455017565827072.pdf?Expires=1688374586&OSSAccessKeyId=LTAI5tESd45p5Gt7uJ7Ww1Pe&Signature=nouVJlXwt5GLoC1rCS9H3LGtFiE%3D",
                            "signpoint": "{\"persion_post_y\":\"277F\",\"persion_post_x\":\"314F\",\"persion_post_page\":\"1\"}",
                            "weburl": "https://openapitest.qinjia001.com/contract/ylpromise.html"
                        }
                    ],
                    "respdate": get_date(fmt="%Y%m%d"),
                    "resptime": get_date(fmt="%H%M%S"),
                    "sendcode": sendcode,
                    "sendflag": sendflag,
                    "sendmsg": sendmsg,
                    "trancode": "QLZS000000209",
                    "transerno": "tKN@id",
                    "transtate": "S"
                }
            }
        self.update(api, mode)

    def update_file_notice(self, sendflag='01', errocode='000000', sendcode='0000', errormsg='成功'):
        """
        文件通知接口
        LoanPostApply & LoanPostCredit 任务都调用这个接口
        sendflag 业务结果
                00 处理中
                01 处理成功
                02 处理失败
        """
        api = "/qingjia/langfang_hengrun_qj/fileNotice"
        mode = {
                "code": 0,
                "message": "success",
                "data": {
                    "channel": "KN10001",
                    "errocode": errocode,
                    "errormsg": errormsg,
                    "fileno": "F@id",  # sendflag 01时必须返回，存到事件表中
                    "respdate": get_date(fmt="%Y%m%d"),
                    "resptime": get_date(fmt="%H%M%S"),
                    "sendcode": sendcode,
                    "sendflag": sendflag,
                    "trancode": "QLZS000000011",
                    "transerno": "tkn@id",
                    "transtate": "S"
                }
            }
        self.update(api, mode)

    def update_credit_apply(self, sendflag='00', errocode='000000', sendcode='0000', sendmsg='路由处理中', errormsg='成功'):
        """
        sendflag 业务结果
                00 处理中
                01 处理成功
                02 处理失败
        sendcode 业务处理码
                0000:路由处理中
                0001:路由成功
                9999:路由失败
                0004：亲家风控拒绝
                0005：银行风控拒绝
                0006:  额度不足
                4000: 路由失败(可重试)
        """
        api = "/qingjia/langfang_hengrun_qj/route"
        mode = {
                "code": 0,
                "message": "success",
                "data": {
                    "channel": "KN10001",
                    "errocode": errocode,
                    "errormsg": errormsg,
                    "respdate": get_date(fmt="%Y%m%d"),
                    "resptime": get_date(fmt="%H%M%S"),
                    "routerno": "r@id",
                    "sendcode": sendcode,
                    "sendflag": sendflag,
                    "sendmsg": sendmsg,
                    "trancode": "QLZS000000302",
                    "transerno": "tkn@id",
                    "transtate": "S"
                }
            }
        self.update(api, mode)

    def update_credit_apply_query(self, asset_info, sendflag='01', errocode='000000', sendcode='0001', errormsg='成功',
                                  sendmsg='路由成功', ):
        """
        sendflag 业务结果
                00 处理中
                01 处理成功
                02 处理失败
        sendcode 业务处理码
                0000:路由处理中
                0001:路由成功
                9999:路由失败
                0004：亲家风控拒绝
                0005：银行风控拒绝
                0006:  额度不足
                4000: 路由失败(可重试)
        """
        api = "/qingjia/langfang_hengrun_qj/routeQuery"
        mode = '''{
                "code": 0,
                "message": "success",
                "data": {
                    "channel": "KN10001",
                    "contractflag": "01",
                    "creditamt": "%s", //授信成功金额,一般来说是等于放款金额的
                    "enddate": "%s",  //截止有效期,当日授信当日有效
                    "fundno": "F060",
                    "errocode": "%s",
                    "errormsg": "%s",
                    "respdate": "%s",
                    "resptime": "%s",
                    "routerno": function({
                      _req
                    }) {
                      return _req.body.routerno
                    },
                    "sendcode": "%s",
                    "sendflag": "%s",
                    "sendmsg": "%s",
                    "trancode": "QLZS000000303",
                    "transerno": "tkn@id",
                    "transtate": "S",
                    "lendercardlist": [
                          {
                            "bankid": "102100099996",
                            "bankname": "中国工商银行"
                          },
                          {
                            "bankid": "105100000017",
                            "bankname": "中国建设银行"
                          }
                        ]
                }
            }''' % (asset_info['data']['asset']['amount'], get_date(fmt="%Y%m%d"), errocode, errormsg,
                    get_date(fmt="%Y%m%d"), get_date(fmt="%H%M%S"), sendcode, sendflag, sendmsg)
        self.update(api, mode)

    def update_credit_apply_query_fail(self, creditamt='200000', enddate='20400606', sendflag='01', errocode='000000',
                                       sendcode='0001', errormsg='成功',  sendmsg='路由成功'):
        api = "/qingjia/langfang_hengrun_qj/routeQuery"
        mode = '''{
                   "code": 0,
                   "message": "success",
                   "data": {
                       "channel": "KN10001",
                       "contractflag": "01",
                       "creditamt": "%s", //授信成功金额,一般来说是等于放款金额的
                       "enddate": "%s",  //截止有效期,当日授信当日有效,但是没有校验这个时间是否过期！
                       "fundno": "F060",
                       "errocode": "%s",
                       "errormsg": "%s",
                       "respdate": "%s",
                       "resptime": "%s",
                       "routerno": function({
                         _req
                       }) {
                         return _req.body.routerno
                       },
                       "sendcode": "%s",
                       "sendflag": "%s",
                       "sendmsg": "%s",
                       "trancode": "QLZS000000303",
                       "transerno": "tkn@id",
                       "transtate": "S",
                       "lendercardlist": [
                             {
                               "bankid": "102100099996",
                               "bankname": "中国工商银行"
                             },
                             {
                               "bankid": "105100000017",
                               "bankname": "中国建设银行"
                             }
                           ]
                   }
               }''' % (creditamt, enddate, errocode, errormsg,
                       get_date(fmt="%Y%m%d"), get_date(fmt="%H%M%S"), sendcode, sendflag, sendmsg)
        self.update(api, mode)

    def update_contract_sign_ature(self, sendflag='01', errocode='000000', sendcode='0000', sendmsg='处理成功', errormsg='成功'):
        """
        LoanApplyQuery 任务调用接口
        和任务ContractSignature 调用的是同一个接口，但是返回值不一样，所以分开写
        sendflag 业务结果
                00 处理中
                01 处理成功
                02 处理失败
        """
        api = "/qingjia/langfang_hengrun_qj/contractCreate"
        mode = {
                "code": 0,
                "message": "success",
                "data": {
                    "channel": "KN10001",
                    "errocode": errocode,
                    "errormsg": errormsg,
                    "filelist": [
                        {
                            "filetype": "loancount",
                            "fileurl": "http://qjosstest.oss-cn-beijing.aliyuncs.com/data/cpu/router/loancontract/1125457650858930176.pdf?Expires=1688375214&OSSAccessKeyId=LTAI5tESd45p5Gt7uJ7Ww1Pe&Signature=oeFEPEcInUcK%2FIhKullN84Ok%2BTc%3D",
                            "signpoint": "{\"persion_post_y\":\"345F\",\"persion_post_x\":\"180F\",\"persion_post_page\":\"2\",\"persion_post_2_y\":\"439F\",\"persion_post_2_x\":\"211F\",\"persion_post_2_page\":\"7\"}",
                            "weburl": "https://openapitest.qinjia001.com/contract/langfangloan.html"
                        },
                        {
                            "filetype": "deduction",
                            "fileurl": "http://qjosstest.oss-cn-beijing.aliyuncs.com/data/cpu/router/loancontract/1125457652092055552.pdf?Expires=1688375214&OSSAccessKeyId=LTAI5tESd45p5Gt7uJ7Ww1Pe&Signature=OHuly%2FDGz2ADpXbrtU3amjODy9c%3D",
                            "signpoint": "{\"persion_post_y\":\"644F\",\"persion_post_x\":\"430F\",\"persion_post_page\":\"2\"}",
                            "weburl": "https://openapitest.qinjia001.com/contract/langfangweituokoukuan.html"
                        },
                        {
                            "filetype": "danbaocount",
                            "fileurl": "http://qjosstest.oss-cn-beijing.aliyuncs.com/data/cpu/router/loancontract/1125457653933355008.pdf?Expires=1688375214&OSSAccessKeyId=LTAI5tESd45p5Gt7uJ7Ww1Pe&Signature=G4ZA1F35fq7fvuIHd5eaZa%2BW%2BgQ%3D",
                            "signpoint": "{\"company_post_page\":\"5\",\"company_post_x\":\"450F\",\"company_post_y\":\"540F\",\"persion_post_y\":\"540F\",\"persion_post_x\":\"160F\",\"persion_post_page\":\"5\"}",
                            "weburl": "https://openapitest.qinjia001.com/contract/hengrunwtht.html"
                        },
                        {
                            "filetype": "danbaoletter",
                            "fileurl": "https://bizfiles-10000035.cossh.myqcloud.com/ZZ_test.pdf?sign=DGcrmxLr%2BqgX7XtBbe6%2FAAjoDslhPTEwMDAwMDM1Jms9QUtJRDVhVnBlVTRDc0h2YW1kd1ZVT25wNnRISW1TOERDTGU5JmU9MTc1MjAyNTI5OSZ0PTE2ODg5NTMyOTkmcj0xMTQ2MzQ3ODc0JmY9JmI9Yml6ZmlsZXM%3D",
                            "signpoint": "{\"company_post_y\":\"440F\",\"company_post_x\":\"440F\",\"company_post_page\":\"1\"}",
                            "weburl": "https://openapitest.qinjia001.com/contract/hengrundbh.html"
                        }
                    ],
                    "respdate": get_date(fmt="%Y%m%d"),
                    "resptime": get_date(fmt="%H%M%S"),
                    "sendcode": sendcode,
                    "sendflag": sendflag,
                    "sendmsg": sendmsg,
                    "trancode": "QLZS000000209",
                    "transerno": "KNt@id",
                    "transtate": "S"
                }
            }

        self.update(api, mode)

    def update_guarantee_apply(self, code=0, status='200', message='成功', msg='内层成功'):
        """
        签章申请接口
        调用的是担保方的接口
        status
            200 - 成功
            500 - 失败
        """
        api = "/hengrun/langfang_hengrun_qj/sign/realtime/apply"
        mode = '''{
                "code": %s,
                "message": "%s",
                "data": {
                    "fileId": "TX@id",
                    "status": "%s",
                    "reqNo":  function({
                      _req
                    }) {
                      return _req.body.reqNo
                    },
                    "msg": "%s"
                }
            }''' % (code, message, status, msg)
        self.update(api, mode)


    def update_guarantee_down(self, code=0, status='200', message='成功', msg='内层成功'):
        """
        签章结果查询接口
        调用的是担保方的接口
        status
            200 - 签署成功
            300 - 签署中
            400 - 签署文件不存在
            500 - 签署失败
        """
        api = "/hengrun/langfang_hengrun_qj/sign/realtime/query"
        mode = '''{
                  "code": %s,
                  "message": "%s",
                  "data": {
                    "fileId": function({
                      _req
                    }) {
                      return _req.body.fileId
                    },
                    "status": "%s",
                    "msg": "%s",   //下面这个fileBase64是mock的，有效期是2年，若过期了需要重新生成，到期日应该是2025-07-03
                    "fileBase64": "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"
                  }
                }''' % (code, message, status, msg)
        self.update(api, mode)

    def update_loan_apply_confirm(self, code=0, sendflag='00', message='success', sendcode='0000', errocode='000000', errormsg='内层成功'):
        """
        贷款支用申请提交接口
        sendflag 业务结果
                00 处理中
                01 处理成功
                02 处理失败
        sendcode 业务处理码
                0000 处理中(继续查询)
                0001 放款成功
                0002 放款失败
                0006 风控规则拒绝
                0007 申请失败
                0008 保证合同生成失败(可重试)
                0009 文件通知失败(可重试)
                0010 银行绑卡失败(可重试)
        """
        api = "/qingjia/langfang_hengrun_qj/loanApply"
        mode = '''{
                    "code": %s,
                    "message": "%s",
                    "data": {
                        "channel": "KN10001",
                        "errocode": "%s",
                        "errormsg": "%s",
                        "merserno":  function({
                      _req
                    }) {
                      return _req.body.merserno  //存入asset_loan_record_identifier
                    },
                        "respdate": "%s",
                        "resptime": "%s",
                        "sendcode": "%s",
                        "sendflag": "%s",
                        "trancode": "QLZS000000004",
                        "transerno": "tkn@id",
                        "transtate": "S"
                    }
                }''' % (code, message, errocode, errormsg, get_date(fmt="%Y%m%d"), get_date(fmt="%H%M%S"), sendcode,sendflag )
        self.update(api, mode)

    def update_loan_apply_confirm_query(self, asset_info, code=0, sendflag='01', message='success', sendcode='0001', errocode='000000',
                                  errormsg='内层成功'):
        """
        贷款支用结果查询接口
        sendflag 业务结果
                00 处理中
                01 处理成功
                02 处理失败
        sendcode 业务处理码
                0000 处理中(继续查询)
                0001 放款成功
                0002 放款失败
                0006 风控规则拒绝
                0007 申请失败
                0008 保证合同生成失败(可重试)
                0009 文件通知失败(可重试)
                0010 银行绑卡失败(可重试)
                0011 额度不足(额度释放后，或下个放款日)
                0012 已过当日支用时间(下个放款日可重试)
        """
        api = "/qingjia/langfang_hengrun_qj/loanQuery"
        mode = '''{
                    "code": %s,
                    "message": "%s",
                    "data": {
                        "channel": "KN10001",
                        "contractno": "C@id", //存入asset_loan_record_trade_no
                        "errocode": "%s",
                        "errormsg": "%s",
                        "loanamt": "%s", // 贷款金额
                        "loanblance": "%s", //贷款余额
                        "loanenddate": "%s",  // 贷款到期日
                        "loanno": "L@id", //存入asset_loan_record_due_bill_no
                        "loanpayway": "2",
                        "loanstartdate": "%s",  //贷款起始日,即放款成功时间，没有时分秒，需要加上当前时间
                        "loanyrate": "6.50",
                        "merserno":  function({
                              _req
                            }) {
                              return _req.body.merserno  
                            },
                        "respdate": "%s",
                        "resptime": "%s",
                        "sendcode": "%s",
                        "sendflag": "%s",
                        "trancode": "QLZS000000013",
                        "transerno": "KN1000120230703165742221f17fe69d",
                        "transtate": "S"
                    }
                }''' % (code, message, errocode, errormsg, asset_info['data']['asset']['amount'],
                        asset_info['data']['asset']['amount'], get_date(month=12, fmt="%Y-%m-%d"), get_date(fmt="%Y-%m-%d"),
                        get_date(fmt="%Y%m%d"), get_date(fmt="%H%M%S"), sendcode, sendflag)
        self.update(api, mode)

    def update_repayplan_success(self, asset_info, item_no):
        api = "/qingjia/langfang_hengrun_qj/repayPlanQuery"
        rate_info = cmdb_rate_loan_calculate_v6(asset_info)
        asset_data = get_asset_info_by_item_no(item_no)
        alr = get_asset_loan_record_by_item_no(item_no)
        loanno = alr[0].get('asset_loan_record_due_bill_no')
        loan_amount = asset_data[0]["asset_principal_amount"]/100
        mode = {
                  "code": 0,
                  "message": "success",
                  "data": {
                    "channel": "KN10001",
                    "errocode": "000000",
                    "errormsg": "成功",
                    "loanamt": loan_amount,
                    "loanno": loanno,
                    "merserno": "KN1000120230703K5GaBRCa",  # 需要和请求保持一致？
                    "paymentschedule": {
                      "payment_schedule": [],
                      "feeplanlist": []
                    },
                    "respdate": get_date(fmt="%Y%m%d"),
                    "resptime": get_date(fmt="%H%M%S"),
                    "retnum": "12",
                    "sendcode": "0000",
                    "sendflag": "01",
                    "sendmsg": "处理成功",
                    "totalnum": "12",
                    "trancode": "QLZS000000010",
                    "transerno": "T@id",
                    "transtate": "S"
                  }
                }
        repayment_plan_tmp = {
                    "actualfeetotal": "0.00",
                    "actualpayinterestamt": "0.00",
                    "actualpayprincipalamt": "0.00",
                    "actualpayprincipalpenaltyamt": "0.00",
                    "ispreps": "0",
                    "loanenddate": "2023-08-03",
                    "payfeetotal": "82.63",
                    "payinterestamt": "54.17",
                    "payprinciaalamt": "808.79",
                    "payprincipalpenaltyamt": "0.00",
                    "tpnum": "1"
                }

        for i in range(asset_info['data']['asset']['period_count']):
                fee_info = get_fee_info_by_period(rate_info, i + 1)
                repayment_plan = deepcopy(repayment_plan_tmp)
                repayment_plan['tpnum'] = i + 1
                repayment_plan['payprinciaalamt'] = float(fee_info['principal']) / 100
                repayment_plan['payinterestamt'] = float(fee_info['interest']) / 100
                repayment_plan['loanenddate'] = fee_info['date'].replace("-", "")
                mode['data']['paymentschedule']['payment_schedule'].append(repayment_plan)

        for a in range(asset_info['data']['asset']['period_count']):
            feeplanlist_tmp1 = {
                "actualfeeamt": "0.00",
                "duedate": "2024-07-03",
                "feeamt": "0.36",
                "feetype": "Q001",
                "subfeeamt": "",
                "tpnum": "12"
            }

            feeplanlist_tmp2 = {
                "actualfeeamt": "0.00",
                "duedate": "2024-07-03",
                "feeamt": "82.27",
                "feetype": "Q002",
                "subfeeamt": "",
                "tpnum": "12"
            }

            feeplanlist_tmp1['tpnum'] = a + 1
            feeplanlist_tmp2['tpnum'] = a + 1
            feeplanlist_tmp1['duedate'] = fee_info['date']
            feeplanlist_tmp2['duedate'] = fee_info['date']
            feeplanlist_tmp1['feeamt'] = float(fee_info['technical_service']) / 200
            feeplanlist_tmp2['feeamt'] = float(fee_info['technical_service']) / 200
            mode['data']['paymentschedule']['feeplanlist'].append(feeplanlist_tmp1)
            mode['data']['paymentschedule']['feeplanlist'].append(feeplanlist_tmp2)
            self.update(api, mode)

    def update_contract_down(self):
        """
        签署合同查询接口  （下载借款合同）
        sendflag 业务结果
                00 处理中
                01 处理成功
                02 处理失败
        """
        api = "/qingjia/langfang_hengrun_qj/contractSignatureQuery"
        mode = {
                "code": 0,
                "message": "success",
                "data": {
                    "channel": "KN10001",
                    "errocode": "000000",
                    "errormsg": "成功",
                    "fileurl": "https://bizfiles-10000035.cossh.myqcloud.com/ZZ_test.pdf?sign=on9ncYaDyzb5EsEe5c6Qu2a2Ng9hPTEwMDAwMDM1Jms9QUtJRDVhVnBlVTRDc0h2YW1kd1ZVT25wNnRISW1TOERDTGU5JmU9MTc1MjE5OTMyNyZ0PTE2ODkxMjczMjcmcj0xNjI2NDM0MTI4JmY9JmI9Yml6ZmlsZXM%3D",
                    "respdate": get_date(fmt="%Y%m%d"),
                    "resptime": get_date(fmt="%H%M%S"),
                    "sendcode": "0000",
                    "sendflag": "01",
                    "sendmsg": "处理成功",
                    "trancode": "QLZS000000113",
                    "transerno": "tk@id",
                    "transtate": "S"
                }
            }
        self.update(api, mode)

    def update_loan_prove_down(self):
        """
        放款证明下载
        sendflag 业务结果
                00 处理中
                01 处理成功
                02 处理失败
        """
        api = "/qingjia/langfang_hengrun_qj/postLoanProveDown"
        mode = {
                "code": 0,
                "message": "success",
                "data": {
                    "channel": "KN10001",
                    "errocode": "000000",
                    "errormsg": "成功",
                    "fileurl": "https://bizfiles-10000035.cossh.myqcloud.com/ZZ_test.pdf?sign=on9ncYaDyzb5EsEe5c6Qu2a2Ng9hPTEwMDAwMDM1Jms9QUtJRDVhVnBlVTRDc0h2YW1kd1ZVT25wNnRISW1TOERDTGU5JmU9MTc1MjE5OTMyNyZ0PTE2ODkxMjczMjcmcj0xNjI2NDM0MTI4JmY9JmI9Yml6ZmlsZXM%3D",
                    "respdate": get_date(fmt="%Y%m%d"),
                    "resptime": get_date(fmt="%H%M%S"),
                    "sendcode": "0000",
                    "sendflag": "01",
                    "sendmsg": "处理成功",
                    "trancode": "QLZS000000111",
                    "transerno": "KN@id",
                    "transtate": "S"
                }
            }
        self.update(api, mode)