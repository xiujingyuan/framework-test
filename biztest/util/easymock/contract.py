# -*- coding: utf-8 -*-
from biztest.util.easymock.easymock import Easymock


class ContractMock(Easymock):
    def update_accrual_info(self, part="苏州", benefit_company_code="v_ruiying"):
        api = "/accrual/info"
        mode = '''{
          "code": 0,
          "message": "",
          "data": {
            "part": "%s",
            "benefit_company_code": "%s"
          }
        }''' % (part, benefit_company_code)
        self.update(api, mode)
