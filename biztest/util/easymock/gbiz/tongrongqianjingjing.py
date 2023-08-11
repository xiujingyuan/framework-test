from biztest.util.easymock.easymock import Easymock
from biztest.util.tools.tools import get_date, get_guid


class TongrongqianjingjingMock(Easymock):

    def update_bk2003(self):
    # 附件上传
        api = "/tongrong2/tongrongqianjingjing/BK2003"
        mode = {
          "code": "00000",
          "message": "成功",
          "success": True,
          "data": None
        }
        self.update(api, mode)

    def update_bk3001(self, code="00000", success=True):
    # 合同预览
        datatime = get_date(fmt="%Y%m%d%H%M%S")
        api = "/tongrong2/tongrongqianjingjing/BK3001"
        mode = {
              "code": code,
              "message": "成功",
              "success": success,
              "data": {
                "contractList": [{
                    "contractName": "崔成(274X)借款合同",
                    "contractNo": "TRJK-KN-HB-" + str(datatime),
                    "contractType": "JKHT",
                    "contractUrl": "http://img.tongrong365.org.cn/62be738179b1476cbb9375ea4e6359b5.pdf?e=1676040847&token=TNumftdWsZryZUcuD9HkgN8DXtDPlVHZgWbpRo8S:KWPAW4SO-kw7NlbMTQnTIxViGH4="
                  },
                  {
                    "contractName": "崔成(274X)人脸识别授权书",
                    "contractNo": "TRJK-KN-HB-" + str(datatime),
                    "contractType": "RLSBSQS",
                    "contractUrl": "http://img.tongrong365.org.cn/55c2ab4fa4544b09a96444a7a84894f6.pdf?e=1676040847&token=TNumftdWsZryZUcuD9HkgN8DXtDPlVHZgWbpRo8S:Xh5MQkBxjrypvtjUIOiadn18oac="
                  },
                  {
                    "contractName": "崔成(274X)征信授权书",
                    "contractNo": "TRJK-KN-HB-" + str(datatime),
                    "contractType": "ZXSQS",
                    "contractUrl": "http://img.tongrong365.org.cn/7f2527cb9a1340a88698f69341b01c99.pdf?e=1676040847&token=TNumftdWsZryZUcuD9HkgN8DXtDPlVHZgWbpRo8S:2cD8iUvlMpAvkHZ4S77z6RkgH6k="
                  }
                ]
              }
            }
        self.update(api, mode)

    def update_bk3003(self, itemno, code="00000", success=True):
    # 合同签章
        datatime = get_date(fmt="%Y%m%d%H%M%S")
        api = "/tongrong2/tongrongqianjingjing/BK3003"
        mode = {
              "code": code,
              "message": "成功",
              "success": success,
              "data": {
                "applyNo": "JP" + itemno,
                "contractList": [{
                    "contractName": "崔成(274X)人脸识别授权书",
                    "contractNo": "TRJK-KN-HB-" + str(datatime),
                    "contractType": "RLSBSQS",
                    "contractUrl": "http://img.tongrong365.org.cn/b658ba58cafe466b99c486efa15c94d3.pdf?e=1676040861&token=TNumftdWsZryZUcuD9HkgN8DXtDPlVHZgWbpRo8S:nkUlEdqkcbNuFcyXkSL9cA5UCM4="
                  },
                  {
                    "contractName": "崔成(274X)征信授权书",
                    "contractNo": "TRJK-KN-HB-" + str(datatime),
                    "contractType": "ZXSQS",
                    "contractUrl": "http://img.tongrong365.org.cn/fa034ad403fe4f36b99ae5b825f260cf.pdf?e=1676040861&token=TNumftdWsZryZUcuD9HkgN8DXtDPlVHZgWbpRo8S:jf9uiJueazWtRppksUPf2nF7fkg="
                  },
                  {
                    "contractName": "崔成(274X)借款合同",
                    "contractNo": "TRJK-KN-HB-" + str(datatime),
                    "contractType": "JKHT",
                    "contractUrl": "https://cashtest-1251122539.cossh.myqcloud.com/2022/03/29/0329_163543_d3e94c37-5195-4371-911a-154fa5f574d0.jpg?sign=zZoeUrZBzdcxux2lJRf1k6xK4jNhPTEyNTExMjI1Mzkmaz1BS0lENWFWcGVVNENzSHZhbWR3VlVPbnA2dEhJbVM4RENMZTkmZT0xNjc4OTU0NDMwJnQ9MTY3NjM2MjQzMCZyPTEzMzM3NTU2MjcmZj0mYj1jYXNodGVzdA%3D%3D"
                  }
                ],
                "outOrderNo": "W2022041675995967"
              }
            }
        self.update(api, mode)

    def update_bk2001(self, itemno, code="00000", success=True, applyStage="B", applyStatus="2"):
    # 进件申请
        api = "/tongrong2/tongrongqianjingjing/BK2001"
        mode = {
              "code": code,
              "message": "成功",
              "success": success,
              "data": {
                "applyNo": "JP" + itemno,
                "applyStage": applyStage,
                "applyStatus": applyStatus,
                "outOrderNo": itemno
              }
            }
        self.update(api, mode)

    def update_bk2002(self, itemno, code="00000", success=True, applyStage="A", applyStatus="2"):
    # 进件查询
        api = "/tongrong2/tongrongqianjingjing/BK2002"
        mode = {
          "code": code,
          "message": "成功",
          "success": success,
          "data": {
            "applyNo": "JP" + itemno,
            "applyStage": applyStage,
            "applyStatus": applyStatus,
            "outOrderNo": itemno
          }
        }
        self.update(api, mode)
    def update_bk2002_noorder(self):
    # 查询订单不存在
        api = "/tongrong2/tongrongqianjingjing/BK2002"
        mode =     {
        "code": "500001",
        "message": ":查询订单失败",
        "success": False,
        "data": None
    }
        self.update(api, mode)


    def update_bk4001(self, code="00000", success=True, status="02"):
    # 放款信息推送
        api = "/tongrong2/tongrongqianjingjing/BK4001"
        mode = {
          "code": code,
          "message": "成功",
          "success": success,
          "data": {
            "loanNo": "@id",
            "status": status
          }
        }
        self.update(api, mode)

    def update_bk3004(self, itemno, code="00000", success=True):
    # 借款合同下载
        datatime = get_date(fmt="%Y%m%d%H%M%S")
        api = "/tongrong2/tongrongqianjingjing/BK3004"
        mode = {
          "code": code,
          "message": "成功",
          "success": success,
          "data": {
            "applyNo": "JP" + itemno,
            "contracts": [{
                "contractName": "杨璐(696X)借款合同",
                "contractNo": "TRJK-KN-HB-" + str(datatime),
                "contractType": "JKHT",
                "contractUrl": "https://cashtest-1251122539.cossh.myqcloud.com/2022/03/29/0329_163543_d3e94c37-5195-4371-911a-154fa5f574d0.jpg?sign=zZoeUrZBzdcxux2lJRf1k6xK4jNhPTEyNTExMjI1Mzkmaz1BS0lENWFWcGVVNENzSHZhbWR3VlVPbnA2dEhJbVM4RENMZTkmZT0xNjc4OTU0NDMwJnQ9MTY3NjM2MjQzMCZyPTEzMzM3NTU2MjcmZj0mYj1jYXNodGVzdA%3D%3D"
              },
              {
                "contractName": "杨璐(696X)人脸识别授权书",
                "contractNo": "TRJK-KN-HB-" + str(datatime),
                "contractType": "RLSBSQS",
                "contractUrl": "http://img.tongrong365.org.cn/b653fad7ac7c4db1afe9e5b2528ed1d7.pdf?e=1676057886&token=TNumftdWsZryZUcuD9HkgN8DXtDPlVHZgWbpRo8S:bngdRjXWLANBRcR-pHMPIB84Bp0="
              },
              {
                "contractName": "杨璐(696X)债权转让协议",
                "contractNo": "TRJK-KN-HB-" + str(datatime),
                "contractType": "ZQZR",
                "contractUrl": "https://sz-biz-contract-test-1251122539.cossh.myqcloud.com/202302/10/W2022041676013443/10501/53a1933b0e134aa7a5b24a92278ec7cb.pdf"
              },
              {
                "contractName": "杨璐(696X)征信授权书",
                "contractNo": "TRJK-KN-HB-" + str(datatime),
                "contractType": "ZXSQS",
                "contractUrl": "http://img.tongrong365.org.cn/32ea834807a44fbcb9a81b272d840f2e.pdf?e=1676057886&token=TNumftdWsZryZUcuD9HkgN8DXtDPlVHZgWbpRo8S:TxMwPfF0XnqXOLMOpj3prntk2y8="
              },
              {
                "contractName": "杨璐(696X)债权转让通知书",
                "contractNo": "TRJK-KN-HB-" + str(datatime),
                "contractType": "ZZTZS",
                "contractUrl": "https://sz-biz-contract-test-1251122539.cossh.myqcloud.com/202302/10/W2022041676013443/30611/39bb046c0b4f4137a7dd5ebb96e8a5e7.pdf"
              }
            ],
            "outOrderNo": itemno
          }
        }
        self.update(api, mode)

    def update_bk3005(self, code="00000", success=True):
    # 债转合同下载
        datatime = get_date(fmt="%Y%m%d%H%M%S")
        api = "/tongrong2/tongrongqianjingjing/BK3005"
        mode = {
              "code": code,
              "message": "成功",
              "success": success,
              "data": {
                "noticeNo": "TRZZTZS-MXKJ-HB-" + str(datatime),
                "noticeUrl": "https://cashtest-1251122539.cossh.myqcloud.com/2022/03/29/0329_163543_d3e94c37-5195-4371-911a-154fa5f574d0.jpg?sign=zZoeUrZBzdcxux2lJRf1k6xK4jNhPTEyNTExMjI1Mzkmaz1BS0lENWFWcGVVNENzSHZhbWR3VlVPbnA2dEhJbVM4RENMZTkmZT0xNjc4OTU0NDMwJnQ9MTY3NjM2MjQzMCZyPTEzMzM3NTU2MjcmZj0mYj1jYXNodGVzdA%3D%3D",
                "transferAgreeUrl": "https://cashtest-1251122539.cossh.myqcloud.com/2022/03/29/0329_163543_d3e94c37-5195-4371-911a-154fa5f574d0.jpg?sign=zZoeUrZBzdcxux2lJRf1k6xK4jNhPTEyNTExMjI1Mzkmaz1BS0lENWFWcGVVNENzSHZhbWR3VlVPbnA2dEhJbVM4RENMZTkmZT0xNjc4OTU0NDMwJnQ9MTY3NjM2MjQzMCZyPTEzMzM3NTU2MjcmZj0mYj1jYXNodGVzdA%3D%3D",
                "transferAmount": "1000.00",
                "transferNo": "TRZQZR-MXKJ-HB-" + str(datatime)
              }
            }
        self.update(api, mode)

    def update_bk3011(self, code="00000", success=True):
    # 电子借据下载
        api = "/tongrong2/tongrongqianjingjing/BK3011"
        mode = {
            "code": "00000",
            "message": "成功",
            "success": True,
            "data": {
                "downloadUrl": "http://img.tongrong365.org.cn/e5e8d638e0c34f8cabc49b9daebef03d.pdf?e=1677273358&token=TNumftdWsZryZUcuD9HkgN8DXtDPlVHZgWbpRo8S:uv5-yyrZ6phYMd2miV42KwJE7VM="
            }
        }
        self.update(api, mode)