# -*- coding: utf-8 -*-
from biztest.function.cmdb.cmdb_common_function import get_fee_info_by_period
from biztest.interface.cmdb.cmdb_interface import cmdb_rate_loan_calculate_v6
from biztest.util.easymock.easymock import Easymock
from biztest.function.gbiz.gbiz_db_function import get_asset_loan_record_by_item_no
from copy import deepcopy
from biztest.util.tools.tools import *
import time
import random

class ZhongjiMock(Easymock):
    def update_guaranteeapply_success(self):
        api = "/zhongji/v2/hami_tianshan/ASSET_APPLY"
        mode = '''{"code": "0",
                         "desc": "成功"
                       }
                       '''
        self.update(api, mode)

    def update_guaranteeapplyquery_success(self):
        api = "/zhongji/v2/hami_tianshan/ASSET_APPLY_QUERY"
        mode = '''{"code": "0",
                 "desc": "成功",
                 "data": {
                   "requestNo": function({
                     _req
                   }) {
                     return _req.body.bizData.loanRequestNo
                   },
                   "status": "AUDITED"
                 }
               }'''
        self.update(api, mode)

    def update_guaranteeapplyquery_fail(self):
        api = "/zhongji/v2/hami_tianshan/ASSET_APPLY_QUERY"
        mode = '''{"code": "0",
                  "desc": "成功",
                  "data": {
                    "requestNo": function({
                      _req
                    }) {
                      return _req.body.bizData.loanRequestNo
                    },
                    "status": "REJECT"
                  }
                }'''
        self.update(api, mode)

    def update_guaranteeupload_success(self):
        api = "/zhongji/v2/hami_tianshan/ASSET_IMAGE_UPLOAD"
        mode = '''{"code": "0",
                     "desc": "成功"
                   }'''
        self.update(api, mode)


    def update_guaranteestatussync_success(self):
        api = "/zhongji/v2/hami_tianshan/ASSET_APPLY_STATUS"
        mode = '''{
                      "code": "0",
                      "desc": "成功"
                    }'''
        self.update(api, mode)

    def update_guaranteeapplyrevoke_success(self):
        api = "/zhongji/v2/hami_tianshan/ASSET_APPLY_REVOKE"
        mode = '''{
                      "code": "0",
                      "desc": "成功"
                    }'''
        self.update(api, mode)

if __name__ == "__main__":
        pass
