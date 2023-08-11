from biztest.config.payment.url_config import global_rapyd_payment_id, global_rapyd_paid_at, global_amount, \
    xendit_redirect_url, xendit_resp_payment_mode, xendit_ebank_resp_payment_mode, payloro_resp_payment_mode, \
    global_withhold_failed_link_expired
from biztest.util.easymock.easymock import Easymock
from foundation_test.util.tools.tools import get_guid


class PayloroMock(Easymock):

    # 代扣下单，获取付款码
    def update_payloro_ebank_charge(self, status, channel_redirect, channel_inner_key):
        api = "/api/pay/code"
        # payloro发起代扣不能走mock，因为需要从返回的链接中获取过期时间，获取不到会直接代扣失败
        if status == "success":
            mode = {
                "status": "200",
                "message": "success",
                "data": {
                    "orderMessage": "PENDING",
                    "orderStatus": "PENDING",
                    "merchantOrderNo": "Rbiz000711035588613024",
                    "platOrderNo": channel_inner_key,
                    "method": payloro_resp_payment_mode,
                    "name": "BENGNAN ADELYN ANGID",
                    "email": "default@123.com",
                    "accountNumber": "LHNWSXG5",
                    "paymentLink": channel_redirect,
                    "paymentImage": "https://bux-api-prd-storage.s3.amazonaws.com/media/barcodes/LHNWSXG5.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAYFTIVUQLPJG42SNS%2F20220516%2Fap-southeast-1%2Fs3%2Faws4_request&X-Amz-Date=20220516T095956Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Signature=0ec8a3bafab8c42eed8103cd9a46b929c4b011e7c392aa52afa47c65d7502041",
                    "payAmount": global_amount / 100,
                    "merchantFee": None,
                    "description": "payloro_ebank",
                    "expiredDate": "2022-05-31T17:59:56+0800",
                    "sign": None
                }
            }
        elif status == "fail":  # 没有返回paymentLink
            mode = {
                "status": "200",
                "message": "success",
                "data": {
                    "orderMessage": "PENDING",
                    "orderStatus": "PENDING",
                    "merchantOrderNo": channel_inner_key,
                    "platOrderNo": "PI-0516173052280761341364232",
                    "method": payloro_resp_payment_mode,
                    "name": "BENGNAN ADELYN ANGID",
                    "email": "default@123.com",
                    "accountNumber": "LHNWSXG5",
                    # "paymentLink": channel_redirect,
                    "paymentImage": "https://bux-api-prd-storage.s3.amazonaws.com/media/barcodes/LHNWSXG5.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAYFTIVUQLPJG42SNS%2F20220516%2Fap-southeast-1%2Fs3%2Faws4_request&X-Amz-Date=20220516T095956Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Signature=0ec8a3bafab8c42eed8103cd9a46b929c4b011e7c392aa52afa47c65d7502041",
                    "payAmount": global_amount / 100,
                    "merchantFee": None,
                    "description": "payloro_ebank",
                    "expiredDate": "2022-06-30T23:59:00+0800",
                    "sign": None
                }
            }
        elif status == "error":  # 发起代扣请求异常
            mode = {
                "status": "416",
                "message": "param payAmount invalid, more than 49",
                "data": None
            }
        elif status == "500":
            mode = {"_res": {"status": 500}}
        else:
            pass
        self.update(api, mode)

    # 代扣查询
    def update_payloro_ebank_query(self, status, channel_key):
        api = "/api/pay/query"
        if status == "success":
            mode = {
                "status": "200",
                "message": "message",
                "data": {
                    "merchantNo": "NO121920285830",
                    "merchantFee": global_amount / 100,
                    "merchantOrderNo": channel_key,
                    "platOrderNo": get_guid(),
                    "amount": global_amount / 100,
                    "accountNumber": "JFNVUUP8",
                    "orderMessage": "SUCCESS",
                    "sign": None,
                    "orderStatus": "SUCCESS"  # ARRIVED/SUCCESS/CLEARED 都表示成功
                }
            }
        elif status == "fail":
            mode = {
                "status": "200",
                "message": "message",
                "data": {
                    "merchantNo": "NO121920285830",
                    "merchantFee": global_amount / 100,
                    "merchantOrderNo": channel_key,
                    "platOrderNo": get_guid(),
                    "amount": global_amount / 100,
                    "accountNumber": "JFNVUUP8",
                    "orderMessage": "FAILED",#不要改
                    "sign": None,
                    "orderStatus": "FAILED"#不要改
                }
            }
        elif status == "process":
            mode = {
                "status": "200",
                "message": "message",
                "data": {
                    "merchantNo": "NO121920285830",
                    "merchantFee": global_amount / 100,
                    "merchantOrderNo": channel_key,
                    "platOrderNo": get_guid(),
                    "amount": global_amount / 100,
                    "accountNumber": "JFNVUUP8",
                    "orderMessage": "pending",
                    "sign": None,
                    "orderStatus": "PENDING"
                }
            }
        elif status == "expired":
            mode = {
                "status": "200",
                "message": "message",
                "data": {
                    "merchantNo": "NO121920285830",
                    "merchantFee": global_amount / 100,
                    "merchantOrderNo": channel_key,
                    "platOrderNo": get_guid(),
                    "amount": global_amount / 100,
                    "accountNumber": "JFNVUUP8",
                    "orderMessage": global_withhold_failed_link_expired,
                    "sign": None,
                    "orderStatus": "PENDING"
                }
            }
        elif status == "no_close":
            mode = {
                "status": "200",
                "message": "message",
                "data": {
                    "merchantNo": "NO121920285830",
                    "merchantFee": global_amount / 100,
                    "merchantOrderNo": channel_key,
                    "platOrderNo": get_guid(),
                    "amount": global_amount / 100,
                    "accountNumber": "JFNVUUP8",
                    "orderMessage": "no_close",
                    "sign": None,
                    "orderStatus": "no_close"#不要改
                }
            }
        elif status == "error":
            mode = {
                "status": "416",
                "message": "param payAmount invalid, more than 49",
                "data": None
            }
        elif status == "not_exsit":
            mode = {
                "status": "404",
                "message": "order not exist",
                "data": None
            }
        elif status == "500":
            mode = {"_res": {"status": 500}}
        else:
            pass
        self.update(api, mode)
