# -*- coding: utf-8 -*-
from biztest.util.http.http_util import Http
from biztest.util.tools.tools import get_guid
import common.global_const as gc


class Msgsender(object):
    def __init__(self, system):
        self.base_url = gc.MSGSENDER_URL
        self.base_url = "https://biz-gateway-proxy.starklotus.com/tha_msgsender"
        self.db = None
        self.worker = None
        self.get_base_info(system)
        self.get_worker(system)

    def get_base_info(self, system):
        if "gbiz" in system:
            self.db = gc.GRANT_DB
        elif "rbiz" in system:
            self.db = gc.REPAY_DB
        elif "payment" in system:
            self.db = gc.PAYMENT_DB
        elif "dcs" in system:
            self.db = gc.DCS_DB
        elif "contact" in system:
            self.db = gc.CONTRACT_DB
        else:
            raise Exception("env未配置，请配置")

    def get_worker(self, system):
        worker_list = {"china": {"rbiz": "rbiz" + gc.ENV,
                                 "gbiz": "gbiz" + gc.ENV,
                                 "payment": "payment_staging"},
                       "thailand": {"rbiz": "tha_rbiz",
                                    "gbiz": "tha_gbiz"},
                       "philippines": {"rbiz": "phl_rbiz",
                                       "gbiz": "phl_gbiz"},
                       "mexico": {"rbiz": "mex_rbiz",
                                  "gbiz": "mex_gbiz"},
                       "pakistan": {"rbiz": "pak_rbiz",
                                    "gbiz": "pak_gbiz"},
                       }
        for key, value in worker_list[gc.COUNTRY].items():
            if system in key:
                self.worker = value
        if self.worker is None:
            raise Exception("Msgsender实例化失败")

    def run_msg(self, with_in_hours=48, delay_seconds=1, limit=500):
        job_url = self.base_url + "/job-test/run-job"
        body = {
            "type": "msgsender",
            "key": get_guid(),
            "from_system": "test",
            "data": {
                "workers": [
                    {
                        "workerName": self.worker,
                        "dataFetch": {
                            "withInHours": with_in_hours,
                            "delaySeconds": delay_seconds,
                            "limit": limit
                        }
                    }
                ]
            }
        }
        Http.http_post(job_url, body, {"Content-Type": "application/json"})

    def run_msg_by_id_list(self, id_list):
        self.db.update("update sendmsg set sendmsg_next_run_at = DATE_SUB(now(), interval 80 minute) "
                       "where sendmsg_id in (%s)" % str(id_list)[1:-1])
        job_url = self.base_url + "/send-msg/send?workerName=" + self.worker
        body = {"type": "msgsender",
                "key": get_guid(),
                "from_system": "test",
                "data": id_list
                }
        Http.http_post(job_url, body, {"Content-Type": "application/json"})

    def run_msg_by_order_no(self, order_no):
        msg_list = self.db.do_sql("select sendmsg_id from sendmsg "
                                  "where sendmsg_order_no = '%s' and sendmsg_status='open'" % str(order_no))
        id_list = [msg["sendmsg_id"] for msg in msg_list]
        if id_list is not None and len(id_list) > 0:
            self.run_msg_by_id_list(id_list)

    def run_msg_by_order_no_list(self, order_no_list):
        msg_list = self.db.do_sql("select sendmsg_id from sendmsg "
                                  "where sendmsg_order_no in (%s) and sendmsg_status='open'" % str(order_no_list)[1:-1])
        id_list = [msg["sendmsg_id"] for msg in msg_list]
        if id_list is not None and len(id_list) > 0:
            self.run_msg_by_id_list(id_list)

    @staticmethod
    def fof_test(worker, id_list):
        job_url = "https://biz-gateway-proxy.starklotus.com/tha_msgsender" + "/send-msg/send?workerName=" + worker
        body = {"type": "msgsender",
                "key": get_guid(),
                "from_system": "test_platform",
                "data": id_list
                }
        Http.http_post(job_url, body, {"Content-Type": "application/json"})


if __name__ == "__main__":
    Msgsender.fof_test("tha_rbiz", [63955, ])
