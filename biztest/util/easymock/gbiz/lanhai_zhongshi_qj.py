# -*- coding: utf-8 -*-
from biztest.function.cmdb.cmdb_common_function import get_fee_info_by_period
from biztest.interface.cmdb.cmdb_interface import cmdb_rate_loan_calculate_v6
from biztest.util.easymock.easymock import Easymock
from copy import deepcopy
from biztest.util.tools.tools import get_guid, get_date
from biztest.function.gbiz.gbiz_db_function import get_asset_loan_record_by_item_no, get_asset_info_by_item_no


class LanhaiZhongshiQjMock(Easymock):

    def update_get_sms_success(self):
        api = "/qingjia/lanhai_zhongshi_qj/bindCardApply"
        mode = '''{
                  "code": 0,
                  "message": "success",
                  "data": {
                    "channel": "KN10001",
                    "errocode": "000000",
                    "errormsg": "请求成功",
                    "respdate": "%s",
                    "resptime": "%s",
                    "sendcode": "0001",
                    "sendflag": "01",
                    "sendmsg": "之前未绑定，申请成功",
                    "trancode": "QLZS000000201",
                    "transerno": "T@id",
                    "transtate": "S"
                  }
                }''' % (get_date(fmt="%Y%m%d"), get_date(fmt="%H%M%S"))
        self.update(api, mode)

    def update_checkcmsverifycode_success(self):
        api = "/qingjia/lanhai_zhongshi_qj/bindCardConfirm"
        mode = '''{
                  "code": 0,
                  "message": "success",
                  "data": {
                    "channel": "KN10001",
                    "errocode": "000000",
                    "errormsg": "请求成功",
                    "respdate": "%s",
                    "resptime": "%s",
                    "sendcode": "0000",
                    "sendflag": "01",
                    "sendmsg": "处理成功",
                    "trancode": "QLZS000000202",
                    "transerno": "T@id",
                    "transtate": "S"
                  }
                }''' % (get_date(fmt="%Y%m%d"), get_date(fmt="%H%M%S"))
        self.update(api, mode)

    def update_info_push_success(self):
        api = "/qingjia/lanhai_zhongshi_qj/loanBaseInfoPush"
        mode = '''{
                  "code": 0,
                  "message": "success",
                  "data": {
                    "channel": "KN10001",
                    "errocode": "000000",
                    "errormsg": "成功",
                    "respdate": "%s",
                    "resptime": "%s",
                    "sendcode": "0000",
                    "sendflag": "01",
                    "sendmsg": "成功",
                    "trancode": "QLZS000000001", //资金方接口名称
                    "transerno": "T@id",
                    "transtate": "S"
                  }
                }''' % (get_date(fmt="%Y%m%d"), get_date(fmt="%H%M%S"))
        self.update(api, mode)

    def update_info_push_fail(self):
        api = "/qingjia/lanhai_zhongshi_qj/loanBaseInfoPush"
        mode = '''{
                  "code": 0,
                  "message": "success",
                  "data": {
                    "channel": "KN10001",
                    "errocode": "000000",
                    "errormsg": "mock失败",
                    "respdate": "%s",
                    "resptime": "%s",
                    "sendcode": "0000",
                    "sendflag": "02",
                    "sendmsg": "sendmsg失败",
                    "trancode": "QLZS000000001", //资金方接口名称
                    "transerno": "T@id",
                    "transtate": "S"
                  }
                }''' % (get_date(fmt="%Y%m%d"), get_date(fmt="%H%M%S"))
        self.update(api, mode)


    def update_postapply_success(self):
        api = "/qingjia/lanhai_zhongshi_qj/fileNotice"
        mode = '''{
                  "code": 0,
                  "message": "success",
                  "data": {
                    "channel": "KN10001",
                    "errocode": "000000",
                    "errormsg": "成功",
                    "fileno": "@id",
                    "respdate": "%s",
                    "resptime": "%s",
                    "sendcode": "0000",
                    "sendflag": "01",
                    "trancode": "QLZS000000011",
                    "transerno": "T@id",
                    "transtate": "S"
                  }
                }''' % (get_date(fmt="%Y%m%d"), get_date(fmt="%H%M%S"))
        self.update(api, mode)

    def update_creditapply_success(self):
        '''
        sendflag
            00 处理中
            01 处理成功
            02 处理失败
        sendcode
            0000:路由处理中
            0001:路由成功
            9999:路由失败
            0004：亲家风控拒绝
            0005：银行风控拒绝
            0006:  额度不足
            4000: 路由失败(可重试)
            :return:
        '''
        api = "/qingjia/lanhai_zhongshi_qj/route"
        mode = '''{
                      "code": 0,
                      "message": "success",
                      "data": {
                        "channel": "KN10001",
                        "errocode": "000000",
                        "errormsg": "成功",
                        "respdate": "%s",
                        "resptime": "%s",
                        "routerno": "@id",
                        "sendcode": "0000",
                        "sendflag": "00",
                        "sendmsg": "路由处理中 ",
                        "trancode": "QLZS000000302",
                        "transerno": "T@id",
                        "transtate": "S"
                      }
                    }''' % (get_date(fmt="%Y%m%d"), get_date(fmt="%H%M%S"))
        self.update(api, mode)

    def update_creditapply_fail(self):
        '''
            sendflag
                   00 处理中
                   01 处理成功
                   02 处理失败
            sendcode
                   0000:路由处理中
                   0001:路由成功
                   9999:路由失败
                   0004：亲家风控拒绝
                   0005：银行风控拒绝
                   0006:  额度不足
                   4000: 路由失败(可重试)
                   :return:
        '''
        api = "/qingjia/lanhai_zhongshi_qj/route"
        mode = '''{
                      "code": 0,
                      "message": "success",
                      "data": {
                        "channel": "KN10001",
                        "errocode": "000000",
                        "errormsg": "mock失败",
                        "respdate": "%s",
                        "resptime": "%s",
                        "routerno": "@id",
                        "sendcode": "9999",
                        "sendflag": "02",
                        "sendmsg": "路由mock失败",
                        "trancode": "QLZS000000302",
                        "transerno": "T@id",
                        "transtate": "S"
                      }
                    }''' % (get_date(fmt="%Y%m%d"), get_date(fmt="%H%M%S"))
        self.update(api, mode)

    def update_credit_query_new_user(self):
        '''
        授信处理中的用户
        '''
        api = "/qingjia/lanhai_zhongshi_qj/routeQuery"
        mode = '''{
                  "code": 0,
                  "message": "success",
                  "data": {
                    "channel": "KN10001",
                    "errocode": "000000",
                    "errormsg": "成功",
                    "respdate": "20221125",
                    "resptime": "142920",
                    "routerno": function({
                      _req
                    }) {
                      return _req.body.routerno
                    },
                    "sendcode": "0000",
                    "sendflag": "00",
                    "trancode": "QLZS000000303",
                    "transerno": "KN10001202211251429204358a177dc6",
                    "transtate": "S"
                  }
                }'''
        self.update(api, mode)

    def update_credit_query_success_old_user(self, creditamt='20000.00', enddate='2036-12-12'):
        '''
        授信过的用户查询
        :return:
        '''
        api = "/qingjia/lanhai_zhongshi_qj/routeQuery"
        mode = '''{
                  "code": 0,
                  "message": "success",
                  "data": {
                    "channel": "KN10001",
                    "contractflag": "01",
                    "creditamt": "%s",
                    "enddate": "%s",
                    "errocode": "000000",
                    "errormsg": "成功",
                    "fundno": "F013",
                    "lendercardlist": [],
                    "respdate": "%s",
                    "resptime": "%s",
                    "sendcode": "0001",
                    "sendflag": "01",
                    "sendmsg": "路由成功",
                    "trancode": "QLZS000000303",
                    "transerno": "T@id",
                    "transtate": "S",
                    "routerno": function({
                      _req
                    }) {
                      return _req.body.routerno
                    }
                  }
                }''' % (creditamt, enddate, get_date(fmt="%Y%m%d"), get_date(fmt="%H%M%S"))
        self.update(api, mode)


    def update_credit_query_fail(self):
        '''
        sendflag
            00 处理中
            01 处理成功
            02 处理失败
        sendcode
            0000:路由处理中
            0001:路由成功
            9999:路由失败
            0004：亲家风控拒绝
            0005：银行风控拒绝
            0006:  额度不足
            4000: 路由失败(可重试)
            :return:
        '''
        api = "/qingjia/lanhai_zhongshi_qj/routeQuery"
        mode = '''{
                  "code": 0,
                  "message": "success",
                  "data": {
                    "channel": "KN10001",
                    "errocode": "000000",
                    "errormsg": "mock授信失败",
                    "respdate": "%s",
                    "resptime": "%s",
                    "routerno": function({
                      _req
                    }) {
                      return _req.body.routerno
                    },
                    "sendcode": "0004",
                    "sendflag": "02",
                    "trancode": "QLZS000000303",
                    "transerno": "T@id",
                    "transtate": "S"
                  }
                }''' % (get_date(fmt="%Y%m%d"), get_date(fmt="%H%M%S"))
        self.update(api, mode)

    def update_contract_create_success(self):
        api = "/qingjia/lanhai_zhongshi_qj/contractCreate"
        mode = {
                  "code": 0,
                  "message": "success",
                  "data": {
                    "channel": "KN10001",
                    "errocode": "000000",
                    "errormsg": "成功",
                    "filelist": [{
                        "filetype": "lhregion",
                        "fileurl": "http://qjosstest.oss-cn-beijing.aliyuncs.com/data/cpu/router/temp/1105918394272657408.pdf?Expires=1683716692&OSSAccessKeyId=LTAI5tESd45p5Gt7uJ7Ww1Pe&Signature=vRWWGXK8jfsa4LWcKsDMwLwwxFA%3D",
                        "signpoint": "{\"persion_post_y\":\"480F\",\"persion_post_x\":\"430F\",\"persion_post_page\":\"1\"}",
                        "weburl": "https://openapitest.qinjia001.com/contract/lanhairegion.html"
                    },
                        {
                        "filetype": "lhcredit",
                        "fileurl": "http://qjosstest.oss-cn-beijing.aliyuncs.com/data/cpu/router/temp/1045712308018425856.pdf?Expires=1669362442&OSSAccessKeyId=LTAI5tESd45p5Gt7uJ7Ww1Pe&Signature=0o0grnz3oK%2Bbn97kM7ksT2wCDaM%3D",
                        "signpoint": "{\"persion_post_y\":\"370F\",\"persion_post_x\":\"265F\",\"persion_post_page\":\"2\"}",
                        "weburl": "https://openapitest.qinjia001.com/contract/lanhairenhang.html"
                      },
                      {
                        "filetype": "lhquery",
                        "fileurl": "http://qjosstest.oss-cn-beijing.aliyuncs.com/data/cpu/router/temp/1045712309280911360.pdf?Expires=1669362443&OSSAccessKeyId=LTAI5tESd45p5Gt7uJ7Ww1Pe&Signature=BxqhbsxcF9nefUue6f8X8Q61%2BNs%3D",
                        "signpoint": "{\"persion_post_y\":\"180F\",\"persion_post_x\":\"400F\",\"persion_post_page\":\"2\"}",
                        "weburl": "https://openapitest.qinjia001.com/contract/lanhaiauth.html"
                      },
                      {
                        "filetype": "lhlimit",
                        "fileurl": "http://qjosstest.oss-cn-beijing.aliyuncs.com/data/cpu/router/temp/1045712310581145600.pdf?Expires=1669362443&OSSAccessKeyId=LTAI5tESd45p5Gt7uJ7Ww1Pe&Signature=mkhOvynCYtdAV1f2Dk30YDrKcPk%3D",
                        "signpoint": "{\"persion_post_y\":\"512F\",\"persion_post_x\":\"200F\",\"persion_post_page\":\"7\"}",
                        "weburl": "https://openapitest.qinjia001.com/contract/lanhailimit.html"
                      },
                      {
                        "filetype": "lzcredit",
                        "fileurl": "http://qjosstest.oss-cn-beijing.aliyuncs.com/data/cpu/router/temp/1045712312015597568.pdf?Expires=1669362443&OSSAccessKeyId=LTAI5tESd45p5Gt7uJ7Ww1Pe&Signature=H8PAEHiqRPL%2BOJgSp711LqYeiwk%3D",
                        "signpoint": "{\"persion_post_y\":\"242F\",\"persion_post_x\":\"203F\",\"persion_post_page\":\"1\"}",
                        "weburl": "https://openapitest.qinjia001.com/contract/lanzhouauth.html"
                      },
                      {
                        "filetype": "qjcredit",
                        "fileurl": "http://qjosstest.oss-cn-beijing.aliyuncs.com/data/cpu/router/temp/1045712313223557120.pdf?Expires=1669362443&OSSAccessKeyId=LTAI5tESd45p5Gt7uJ7Ww1Pe&Signature=1h%2BWuJFL1MJVq023kQo9l0pd%2Fx4%3D",
                        "signpoint": "{\"persion_post_y\":\"113F\",\"persion_post_x\":\"455F\",\"persion_post_page\":\"1\"}",
                        "weburl": "https://openapitest.qinjia001.com/contract/qinjiaauth.html"
                      },
                      {
                        "filetype": "ylcredit",
                        "fileurl": "http://qjosstest.oss-cn-beijing.aliyuncs.com/data/cpu/router/temp/1045712314301493248.pdf?Expires=1669362444&OSSAccessKeyId=LTAI5tESd45p5Gt7uJ7Ww1Pe&Signature=FhPk1102OW0cGpBOIS7wrXR3pTM%3D",
                        "signpoint": "{\"persion_post_y\":\"256F\",\"persion_post_x\":\"260F\",\"persion_post_page\":\"2\"}",
                        "weburl": "https://openapitest.qinjia001.com/contract/yilianzhengxinshouquan.html"
                      },
                      {
                        "filetype": "ylquery",
                        "fileurl": "http://qjosstest.oss-cn-beijing.aliyuncs.com/data/cpu/router/temp/1045712315782082560.pdf?Expires=1669362444&OSSAccessKeyId=LTAI5tESd45p5Gt7uJ7Ww1Pe&Signature=qQKAQBvktSpzhZ7OvNe%2FKPTrmeY%3D",
                        "signpoint": "{\"persion_post_y\":\"250F\",\"persion_post_x\":\"225F\",\"persion_post_page\":\"3\"}",
                        "weburl": "https://openapitest.qinjia001.com/contract/yilianauthchaxun.html"
                      },
                      {
                        "filetype": "yluse",
                        "fileurl": "http://qjosstest.oss-cn-beijing.aliyuncs.com/data/cpu/router/temp/1045712316893573120.pdf?Expires=1669362444&OSSAccessKeyId=LTAI5tESd45p5Gt7uJ7Ww1Pe&Signature=jT8C%2BG4Cg%2FNOzkNoNFwCNJqhVU8%3D",
                        "signpoint": "{\"persion_post_y\":\"250F\",\"persion_post_x\":\"225F\",\"persion_post_page\":\"3\"}",
                        "weburl": "https://openapitest.qinjia001.com/contract/yilianauthshiyong.html"
                      },
                      {
                        "filetype": "ylamountcontract",
                        "fileurl": "http://qjosstest.oss-cn-beijing.aliyuncs.com/data/cpu/router/temp/1045712318189613056.pdf?Expires=1669362445&OSSAccessKeyId=LTAI5tESd45p5Gt7uJ7Ww1Pe&Signature=ZHQ4BAd%2FFBvbUdPvBYm7LoGZjC8%3D",
                        "signpoint": "{\"persion_post_y\":\"578F\",\"persion_post_x\":\"440F\",\"persion_post_page\":\"11\"}",
                        "weburl": "https://openapitest.qinjia001.com/contract/gerenedu.html"
                      },
                      {
                        "filetype": "ylpromise",
                        "fileurl": "http://qjosstest.oss-cn-beijing.aliyuncs.com/data/cpu/router/temp/1045712319477264384.pdf?Expires=1669362445&OSSAccessKeyId=LTAI5tESd45p5Gt7uJ7Ww1Pe&Signature=nNxhTLNDRZCmYRNvqEkAv%2Ftot2g%3D",
                        "signpoint": "{\"persion_post_y\":\"277F\",\"persion_post_x\":\"314F\",\"persion_post_page\":\"1\"}",
                        "weburl": "https://openapitest.qinjia001.com/contract/ylpromise.html"
                      },
                        {
                            "filetype": "loancount",
                            "fileurl": "http://qjosstest.oss-cn-beijing.aliyuncs.com/data/cpu/router/loancontract/1045712322799153152.pdf?Expires=1669362446&OSSAccessKeyId=LTAI5tESd45p5Gt7uJ7Ww1Pe&Signature=FFffDwtwFD52AFJ9Swl72j9fuD0%3D",
                            "signpoint": "{\"persion_post_y\":\"285F\",\"persion_post_x\":\"320F\",\"persion_post_page\":\"15\"}",
                            "weburl": "https://openapitest.qinjia001.com/contract/lanhailoan.html"
                        },
                        {
                            "filetype": "danbaocount",
                            "fileurl": "http://qjosstest.oss-cn-beijing.aliyuncs.com/data/cpu/router/loancontract/1045712324833390592.pdf?Expires=1669362446&OSSAccessKeyId=LTAI5tESd45p5Gt7uJ7Ww1Pe&Signature=IMGvQmV6jNebFBjx6T98swb5%2BAY%3D",
                            "signpoint": "{\"company_post_page\":\"7\",\"company_post_x\":\"270F\",\"company_post_y\":\"715F\",\"persion_post_y\":\"665F\",\"persion_post_x\":\"110F\",\"persion_post_page\":\"7\"}",
                            "weburl": "https://openapitest.qinjia001.com/contract/zhongshiwtht.html"
                        },
                        {
                            "filetype": "danbaoconsult",
                            "fileurl": "http://qjosstest.oss-cn-beijing.aliyuncs.com/data/cpu/router/loancontract/1121083871479279616.pdf?Expires=1687332423&OSSAccessKeyId=LTAI5tESd45p5Gt7uJ7Ww1Pe&Signature=91yEKsErOCi3sPL7ucVXn9W6w9M%3D",
                            "signpoint": "{\"company_post_page\":\"4\",\"company_post_x\":\"270F\",\"company_post_y\":\"355F\",\"persion_post_y\":\"450F\",\"persion_post_x\":\"180F\",\"persion_post_page\":\"4\"}",
                            "weburl": "https://openapitest.qinjia001.com/contract/zhongshiconsu.html"
                        }
                    ],
                    "respdate": get_date(fmt="%Y%m%d"),
                    "resptime": get_date(fmt="%H%M%S"),
                    "sendcode": "0000",
                    "sendflag": "01",
                    "sendmsg": "处理成功",
                    "trancode": "QLZS000000209",
                    "transerno": "T@id",
                    "transtate": "S"
                  }
                }
        self.update(api, mode)

    def update_contract_create_fail(self):
        api = "/qingjia/lanhai_zhongshi_qj/contractCreate"
        mode = {
                  "code": 0,
                  "message": "success",
                  "data": {
                    "channel": "KN10001",
                    "errocode": "000000",
                    "errormsg": "成功",
                    "filelist": [],
                    "respdate": get_date(fmt="%Y%m%d"),
                    "resptime": get_date(fmt="%H%M%S"),
                    "sendcode": "0001",
                    "sendflag": "02",
                    "sendmsg": "mock失败测试",
                    "trancode": "QLZS000000209",
                    "transerno": "T@id",
                    "transtate": "S"
                  }
                }
        self.update(api, mode)

    def update_contractpush_success(self):
        '''
        sendflag
            00 处理中
            01 处理成功
            02 处理失败
        sendcode
            0000	处理成功
            1000	数据校验（数据有效性，非空）
            1001	不支持的银行
            1002	不支持的渠道
            1003	无可用渠道
            1004	业务订单号不存在
        :return:
        '''
        api = "/qingjia/lanhai_zhongshi_qj/contractSignature"
        mode = '''{
                  "code": 0,
                  "message": "success",
                  "data": {
                    "channel": "KN10001",
                    "errocode": "000000",
                    "errormsg": "成功",
                    "respdate": "%s",
                    "resptime": "%s",
                    "sendcode": "1000",
                    "sendflag": "01",
                    "sendmsg": "等待中",
                    "trancode": "QLZS000000205",
                    "transerno": "KN1000120221125161044136320d8d3d",
                    "transtate": "S"
                  }
                }'''% (get_date(fmt="%Y%m%d"), get_date(fmt="%H%M%S"))
        self.update(api, mode)

    def update_contractpush_query_success(self):
        '''
        sendflag
            00 处理中
            01 处理成功
            02 处理失败
        sendcode
            0000	处理成功
            1000	数据校验（数据有效性，非空）
            1001	不支持的银行
            1002	不支持的渠道
            1003	无可用渠道
            1004	业务订单号不存在
        :return:
        '''
        api = "/qingjia/lanhai_zhongshi_qj/queryContractSignature"
        mode = {
                  "code": 0,
                  "message": "success",
                  "data": {
                    "channel": "KN10001",
                    "errocode": "000000",
                    "errormsg": "成功",
                    "fileUrl": "http://zhongshi-oss.oss-cn-beijing.aliyuncs.com/test/sign/deduction/371724197509101847_1045742109190074368_rd_company.pdf?Expires=1669370218&OSSAccessKeyId=LTAI5tEJS7J44ubq4GoMEjjZ&Signature=LvSkRrOI3Xd7nkwNxYc4247YrMw%3D",
                    "respdate": get_date(fmt="%Y%m%d"),
                    "resptime": get_date(fmt="%H%M%S"),
                    "sendcode": "0000",
                    "sendflag": "01",
                    "sendmsg": "处理成功",
                    "trancode": "QLZS000000206",
                    "transerno": "T@id",
                    "transtate": "S"
                  }
                }
        self.update(api, mode)

    def update_loanapplyconfirm_success(self):
        '''
        sendflag
            00 处理中
            01 处理成功
            02 处理失败
        sendcode
            0000	处理成功
            1000	数据校验（数据有效性，非空）
            1001	不支持的银行
            1002	不支持的渠道
            1003	无可用渠道
            1004	业务订单号不存在
        :return:
        '''
        api = "/qingjia/lanhai_zhongshi_qj/loanApply"
        mode = '''{
                  "code": 0,
                  "message": "success",
                  "data": {
                    "channel": "KN10001",
                    "errocode": "000000",
                    "errormsg": "成功",
                    "merserno": function({
                      _req
                    }) {
                      return _req.body.merserno
                    },
                    "respdate": "%s",
                    "resptime": "%s",
                    "sendcode": "0000",
                    "sendflag": "00",
                    "trancode": "QLZS000000004",
                    "transerno": "T@id",
                    "transtate": "S"
                  }
                }''' % (get_date(fmt="%Y%m%d"), get_date(fmt="%H%M%S"))
        self.update(api, mode)


    def update_loanapplyconfirm_fail(self):
        '''
        sendflag
            00 处理中
            01 处理成功
            02 处理失败
        sendcode
            0000	处理成功
            1000	数据校验（数据有效性，非空）
            1001	不支持的银行
            1002	不支持的渠道
            1003	无可用渠道
            1004	业务订单号不存在
        :return:
        '''
        api = "/qingjia/lanhai_zhongshi_qj/loanApply"
        mode = '''{
                  "code": 0,
                  "message": "success",
                  "data": {
                    "channel": "KN10001",
                    "errocode": "000000",
                    "errormsg": "mock失败",
                    "merserno":  function({
                      _req
                    }) {
                      return _req.body.merserno
                    },
                    "respdate": "%s",
                    "resptime": "%s",
                    "sendcode": "1002",
                    "sendflag": "02",
                    "trancode": "QLZS000000004",
                    "transerno": "T@id",
                    "transtate": "S"
                  }
                }''' % (get_date(fmt="%Y%m%d"), get_date(fmt="%H%M%S"))
        self.update(api, mode)


    def update_loanconfirmquery_success(self, asset_info):
        '''
               sendflag
                   00 处理中
                   01 处理成功
                   02 处理失败
               sendcode
                   0000	处理成功
                   1000	数据校验（数据有效性，非空）
                   1001	不支持的银行
                   1002	不支持的渠道
                   1003	无可用渠道
                   1004	业务订单号不存在
          loanno 需存入due_bill_no中
        '''
        api = '/qingjia/lanhai_zhongshi_qj/loanQuery'
        body = {
                "code": 0,
                "message": "success",
                "data": {
                    "channel": "KN10001",
                    "contractno": "C@id",
                    "errocode": "000000",
                    "errormsg": "成功",
                    "loanamt": asset_info['data']['asset']['amount'],
                    "loanblance": asset_info['data']['asset']['amount'],
                    "loanno": "L@id",
                    "loanpayway": "2",
                    "loanstartdate": get_date(fmt="%Y-%m-%d"),
                    "loanenddate": get_date(month=12, fmt="%Y-%m-%d"),
                    "loanyrate": "8.50",
                    "merserno": "M@id",
                    "respdate": get_date(fmt="%Y%m%d"),
                    "resptime": get_date(fmt="%H%M%S"),
                    "sendcode": "0001",
                    "sendflag": "01",
                    "trancode": "QLZS000000013",
                     "transerno": "T@id",
                    "transtate": "S"
                }
            }
        self.update(api, body)

    def update_loanconfirmquery_fail(self):
        '''
               sendflag
                   00 处理中
                   01 处理成功
                   02 处理失败
               sendcode
                   0000	处理成功
                   1000	数据校验（数据有效性，非空）
                   1001	不支持的银行
                   1002	不支持的渠道
                   1003	无可用渠道
                   1004	业务订单号不存在
            :return:
        '''
        api = '/qingjia/lanhai_zhongshi_qj/loanQuery'
        body = {
                  "code": 0,
                  "message": "success",
                  "data": {
                    "channel": "KN10001",
                    "errocode": "000000",
                    "errormsg": "mock失败",
                    "merserno": "M@id",
                    "respdate": get_date(fmt="%Y%m%d"),
                    "resptime": get_date(fmt="%H%M%S"),
                    "sendcode": "1001",
                    "sendflag": "02",
                    "trancode": "QLZS000000013",
                    "transerno": "T@id",
                    "transtate": "S"
                  }
                }
        self.update(api, body)

    def update_repayplan_success(self, asset_info, item_no):
        api = "/qingjia/lanhai_zhongshi_qj/repayPlanQuery"
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
                  "loanenddate": "2022-12-25",
                  "payfeetotal": "131.71",
                  "payinterestamt": "70.83",
                  "payprinciaalamt": "801.37",
                  "payprincipalpenaltyamt": "0.00",
                  "settledate": "",
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
                "duedate": "2023-11-28",
                "feeamt": "8.50",
                "feetype": "Q001",
                "subfeeamt": "",
                "tpnum": "12"}

            feeplanlist_tmp2 = {
                "actualfeeamt": "0.00",
                "duedate": "2023-11-28",
                "feeamt": "8.50",
                "feetype": "Q002",
                "subfeeamt": "",
                "tpnum": "12"}

            feeplanlist_tmp1['tpnum'] = a + 1
            feeplanlist_tmp2['tpnum'] = a + 1
            feeplanlist_tmp1['duedate'] = fee_info['date']
            feeplanlist_tmp2['duedate'] = fee_info['date']
            feeplanlist_tmp1['feeamt'] = float(fee_info['guarantee']) / 100
            feeplanlist_tmp2['feeamt'] = float(fee_info['technical_service']) / 100
            mode['data']['paymentschedule']['feeplanlist'].append(feeplanlist_tmp1)
            mode['data']['paymentschedule']['feeplanlist'].append(feeplanlist_tmp2)
        self.update(api, mode)

    def update_certificate_apply(self):
        api = "/qingjia/lanhai_zhongshi_qj/certificateApply"
        mode = {
                  "code": 0,
                  "message": "success",
                  "data": {
                    "channel": "KN10001",
                    "errocode": "000000",
                    "errormsg": "成功",
                    "respdate": "20230222",
                    "resptime": "101318",
                    "sendcode": "true",
                    "sendflag": "01",
                    "sendmsg": "处理成功",
                    "trancode": "QLZS000000110",
                    "transerno": "KN100012023022210131870893e522c9",
                    "transtate": "S"
                  }
                }
        self.update(api, mode)


    def update_certificate_download(self):
        '''
        sendflag
            00 处理中
            01 处理成功
            02 处理失败
        :return:
        '''
        api = "/qingjia/lanhai_zhongshi_qj/certificateDownload"
        mode = {
                  "code": 0,
                  "message": "success",
                  "data": {
                    "channel": "KN10001",
                    "errocode": "000000",
                    "errormsg": "成功",
                    "fileurl": "http://qjosstest.oss-cn-beijing.aliyuncs.com/data/lanzhou/attach/settleFile/001_settle_1047175727827218433_10.pdf?Expires=1677038286&OSSAccessKeyId=LTAI5tESd45p5Gt7uJ7Ww1Pe&Signature=2WTXUyehi9hMnSPkSFusXugJ%2BUo%3D",
                    "respdate": "20230222",
                    "resptime": "105806",
                    "sendcode": "00",
                    "sendflag": "01",
                    "sendmsg": "处理成功",
                    "trancode": "QLZS000000111",
                    "transerno": "KN10001202302221058058830151a6f0",
                    "transtate": "S"
                  }
                }
        self.update(api, mode)