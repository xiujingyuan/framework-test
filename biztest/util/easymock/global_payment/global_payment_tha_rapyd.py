from biztest.config.payment.url_config import global_rapyd_payment_id, global_rapyd_paid_at
from biztest.util.easymock.easymock import Easymock


class RapydMock(Easymock):
    def update_qrcode_withhold_success(self):
        api = "/v1/payments"
        mode = {
            "status": {
                "error_code": "",
                "status": "SUCCESS",  # 表示创建支付请求成功
                "message": "",
                "response_code": "",
                "operation_id": "213c2354-639c-40de-b5c0-dc0ad369a7dc"
            },
            "data": {
                "id": global_rapyd_payment_id,  # 更新到withhold_receipt_channel_inner_key
                "amount": 0,
                "original_amount": 10,
                "is_partial": False,
                "currency_code": "THB",
                "country_code": "TH",
                "status": "ACT",  # 表示等待支付中
                "description": "",
                "merchant_reference_id": "",
                "customer_token": "cus_fc3304643a974680767eab599efe1619",
                "payment_method": "other_80239a6de2f5a5b6985f6ac2dcfc6d29",
                "payment_method_data": {
                    "id": "other_80239a6de2f5a5b6985f6ac2dcfc6d29",
                    "type": "th_thaipromptpayqr_bank",
                    "category": "bank_transfer",
                    "metadata": {},
                    "image": "",
                    "authentication_url": "",
                    "webhook_url": "",
                    "supporting_documentation": ""
                },
                "expiration": 1651334400,
                "captured": True,
                "refunded": False,
                "refunded_amount": 0,
                "receipt_email": "",
                "redirect_url": "",
                "complete_payment_url": "",
                "error_payment_url": "",
                "receipt_number": "",
                "flow_type": "",
                "address": None,
                "statement_descriptor": "Saphhire Skysrapper Co",
                "transaction_id": "",
                "created_at": 1620961334,
                "metadata": {},
                "failure_code": "",
                "failure_message": "",
                "paid": False,
                "paid_at": 0,
                "dispute": None,
                "refunds": None,
                "order": None,
                "outcome": None,
                "visual_codes": {
                    "qrcode_url": "https://d2o8h9r6avao9o.cloudfront.net/payments/213c2354-639c-40de-b5c0-dc0ad369a7dc_qrcode.png",
                    "qrcode_image_base64": "iVBORw0KGgoAAAANSUhEUgAAANkAAADZCAMAAACaYGVEAAAABlBMVEUAAAD///+l2Z/dAAACDUlEQVR42u3bSXLDMAwEQPn/n845i6UZkHJSTvPmRbKaFxQw9PF413WQkZGRkT2VHe36cpuTzz5/5eyzH+8yfTIyMjIysktZUidOZAE3/6HFJyMjIyMjS2VBfQmqTVC6gnI4fjIyMjIysrtkRZkJ+o92J8nIyMjI/oBscQ/IyMjIyF4kq8tT8Ls5dzrsIiMjIyMrZX0a/KpXL0/gycjIyN5ZNl15AJGfQHpsWWRkZGRkz2V1Dam5i4lFH4iTkZGRkV3J8gBiGjlsTSxO3yQjIyMju5rw5JFDUInq4VMdUCf1jIyMjIxsRRb0LVP81hpJRkZGRjaTTR9tOoPaU93IyMjIyNIzPEWvsDNvno6pfr6cjIyMjOwx+f9ZEELvybCn7dI4gScjIyP7r7K8V6iD5sXdGmfmZGRkZGRdPau507andiZ3ISMjIyPbILsjrt5zSKmYXZGRkZGRrZwmrS/vm5K6cJKRkZGRjSY8dcJ8R2pdT7nIyMjIyFJZ3aJME4tjuJLuh4yMjIzsqWy6bnRO024yMjIyskvZnjFVTpruT3FSioyMjIysSyzy6CB/tWdjgluTkZGRkZWnk6b1ZToIy2trsgdkZGRkZL8hKxqPnaWSjIyMjOw2WR0rbOX2567IyMjIyEazq3pj6qefBuJkZGRkZJeyOqe+ozwtXkBGRkZGdil7v0VGRkZG9n19ANqjZ13sz1WoAAAAAElFTkSuQmCC"
                },
                "textual_codes": {
                    "pay_code": "paygw_efa3893d47a82032d624a86c8ba14421"
                },
                "instructions": [{
                    "name": "instructions",
                    "steps": [{
                        "step1": "Scan QR Code."
                    },
                        {
                            "step2": "Enter OTP to authorize Payment."
                        },
                        {
                            "step3": "Complete Payment."
                        }
                    ]
                }],
                "ewallet_id": "ewallet_1445a08ddab7e1ade98188a161159694",
                "ewallets": [{
                    "ewallet_id": "ewallet_1445a08ddab7e1ade98188a161159694",
                    "amount": 10,
                    "percent": 100,
                    "refunded_amount": 0
                }],
                "payment_method_options": {},
                "payment_method_type": "th_thaipromptpayqr_bank",
                "payment_method_type_category": "bank_transfer",
                "fx_rate": 1,
                "merchant_requested_currency": None,
                "merchant_requested_amount": None,
                "fixed_side": "",
                "payment_fees": None,
                "invoice": "",
                "escrow": None,
                "group_payment": "",
                "cancel_reason": None,
                "initiation_type": "customer_present",
                "mid": "",
                "next_action": "pending_confirmation"
            }
        }
        self.update(api, mode)

    def update_qrcode_withhold_fail(self):
        api = "/v1/payments"
        mode = {
            "status": {
                "error_code": "ERROR_CREATE_PAYMENT",
                "status": "ERROR",  # 表示创建支付请求失败
                "message": "The request tried to create a payment, but the payment method was not found.",
                "response_code": "ERROR_CREATE_PAYMENT",
                "operation_id": "336482a8-24e7-4266-841f-af6279fc593a"
            }
        }
        self.update(api, mode)

    def update_qrcode_withhold_500(self):
        api = "/v1/payments"
        mode = {"_res": {"status": 500}}
        self.update(api, mode)

    def update_qrcode_query_not_exist(self):
        api = "/v1/payments/" + global_rapyd_payment_id
        mode = {
            "status": {
                "error_code": "ERROR_GET_PAYMENT",
                "status": "ERROR",
                "message": "The request tried to retrieve a payment, but the payment was not found. The request was rejected. Corrective action: Use a valid payment ID.",
                "response_code": "ERROR_GET_PAYMENT",
                "operation_id": "c4560895-9d58-4a5b-b91e-e6bf956a8a9b"
            }
        }
        self.update(api, mode)

    def update_qrcode_query_success(self, withhold_receipt, expire_at):
        amount = round(withhold_receipt[0]["withhold_receipt_amount"] / 100, 2)
        api = "/v1/payments/" + global_rapyd_payment_id
        mode = {
            "status": {
                "error_code": "",
                "status": "SUCCESS",  # 表示查询请求是成功的
                "message": "",
                "response_code": "",
                "operation_id": "2f239c1d-a381-4742-a01d-1a1c26c3d24c"
            },
            "data": {
                "id": withhold_receipt[0]["withhold_receipt_channel_inner_key"],
                "amount": amount,
                "original_amount": amount,
                "is_partial": False,
                "currency_code": "THB",
                "country_code": "TH",
                "status": "CLO",  # 表示支付结果为成功
                "description": "",
                "merchant_reference_id": "RBIZ505125901789243621",
                "customer_token": "cus_4deb0426cbefed9cc580dc08611d847a",
                "payment_method": "other_124248b8f2507a90d5238ece022f2b82",
                "payment_method_data": {
                    "id": "other_124248b8f2507a90d5238ece022f2b82",
                    "type": "th_thaipromptpayqr_bank",
                    "category": "bank_transfer",
                    "metadata": {},
                    "image": "",
                    "authentication_url": "",
                    "webhook_url": "",
                    "supporting_documentation": ""
                },
                "expiration": expire_at,
                "captured": True,
                "refunded": False,
                "refunded_amount": 0,
                "receipt_email": "",
                "redirect_url": "",
                "complete_payment_url": "http://www.baidu.com",
                "error_payment_url": "",
                "receipt_number": "",
                "flow_type": "",
                "address": None,
                "statement_descriptor": "Saphhire Skysrapper Co",
                "transaction_id": "",
                "created_at": 1620785885,
                "metadata": {},
                "failure_code": "",
                "failure_message": "",
                "paid": True,
                "paid_at": global_rapyd_paid_at,  # 支付完成时间戳
                "dispute": None,
                "refunds": None,
                "order": None,
                "outcome": None,
                "visual_codes": {
                    "qrcode_url": "https://d2o8h9r6avao9o.cloudfront.net/payments/d3c7fd77-2b51-45a5-8e44-38bae3bebafd_qrcode.png",
                    "qrcode_image_base64": "iVBORw0KGgoAAAANSUhEUgAAANkAAADZCAMAAACaYGVEAAAABlBMVEUAAAD///+l2Z/dAAACCUlEQVR42u3dUVICQQwEULj/pT2AuHR6Alr49g+E3bzxIzXpKb3dP/W6kZGRkZH9KLtNr+TeF598+LOrN8eVkZGRkZE9lbX1Jk/Ka7p4lVdGRkZGRpbK2ucGVeSFnlZGRkZGRvZiWY4/XDsyMjIyst+UjettB1pkZGRkZPuydlex8/W/MZUjIyMj+weyeRr8rldvT+DJyMjIPlnWXnk/W809ksrIyMjIyH6UtROpVWCwdkEtZGRkZGSpLMgM8uggv2ebkFy+SUZGRka2PrtaHT61azfoZ2RkZGRkVQsaI8aN83S7REZGRkYWzq7GB5FaUrBvGQ+0yMjIyMiGp5PawLgNLlZjEzIyMjKyVJZXv3OcabxTOU3gycjIyMiqLnV50zJkOIw4yMjIyMi6xGJ1hNXeLG+qjx9ERkZGRjaTjc8cHbbD28pFRkZGRtbl1If9rG1y4/yinsqRkZGRkVWbi+BYUh54HAbUZGRkZGSd7HDD0h42Oty+kJGRkZE9lR0eNto5wNQOwh7/PsjIyMjI7tt/X78db7XZRj27IiMjIyO7r/2/mPEn2/FWsO0hIyMjIxvKxgFEHnHszK6SNSAjIyMje7Eszy92lul9/YyMjIyMLPxeDszX5zSBJyMjIyOrZlfj00ltIxtvZsjIyMjInsrGzeOVw6fp+pCRkZGRpbLPu8jIyMjIvl9fS+NjJ5M0+h4AAAAASUVORK5CYII="
                },
                "textual_codes": {
                    "pay_code": "paygw_7caedc8bb674e2e132c7148f60aef1d1"
                },
                "instructions": [
                    {
                        "name": "instructions",
                        "steps": [
                            {
                                "step1": "Scan QR Code."
                            },
                            {
                                "step2": "Enter OTP to authorize Payment."
                            },
                            {
                                "step3": "Complete Payment."
                            }
                        ]
                    }
                ],
                "ewallet_id": "ewallet_1445a08ddab7e1ade98188a161159694",
                "ewallets": [
                    {
                        "ewallet_id": "ewallet_1445a08ddab7e1ade98188a161159694",
                        "amount": 5025.12,
                        "percent": 100,
                        "refunded_amount": 0
                    }
                ],
                "payment_method_options": {},
                "payment_method_type": "th_thaipromptpayqr_bank",
                "payment_method_type_category": "bank_transfer",
                "fx_rate": 1,
                "merchant_requested_currency": None,
                "merchant_requested_amount": None,
                "fixed_side": "",
                "payment_fees": None,
                "invoice": "",
                "escrow": None,
                "group_payment": "",
                "cancel_reason": None,
                "initiation_type": "customer_present",
                "mid": "",
                "next_action": "not_applicable"
            }
        }
        self.update(api, mode)

    def update_qrcode_query_fail(self, withhold_receipt, expire_at):
        amount = round(withhold_receipt[0]["withhold_receipt_amount"] / 100, 2)
        api = "/v1/payments/" + global_rapyd_payment_id
        mode = {
            "status": {
                "error_code": "",
                "status": "SUCCESS",  # 表示查询请求是成功的
                "message": "",
                "response_code": "",
                "operation_id": "a0c7e90b-bdcc-4ce5-8322-a4e19ef8e929"
            },
            "data": {
                "id": "payment_3f02affc1594567649a50450959b3fe3",
                "amount": 0,
                "original_amount": amount,
                "is_partial": False,
                "currency_code": "THB",
                "country_code": "TH",
                "status": "CAN",  # 表示支付结果是失败的，但是需要配置在channel_error表中
                "description": "",
                "merchant_reference_id": "RBIZ505133181342019460",
                "customer_token": "cus_8e33ca699148911c98101f61945d4859",
                "payment_method": "other_3256791a327bb07dade1e61f8e1ee9d2",
                "payment_method_data": {
                    "id": "other_3256791a327bb07dade1e61f8e1ee9d2",
                    "type": "th_thaipromptpayqr_bank",
                    "category": "bank_transfer",
                    "metadata": {},
                    "image": "",
                    "authentication_url": "",
                    "webhook_url": "",
                    "supporting_documentation": ""
                },
                "expiration": expire_at,
                "captured": True,
                "refunded": False,
                "refunded_amount": 0,
                "receipt_email": "",
                "redirect_url": "",
                "complete_payment_url": "",
                "error_payment_url": "",
                "receipt_number": "",
                "flow_type": "",
                "address": None,
                "statement_descriptor": "Saphhire Skysrapper Co",
                "transaction_id": "",
                "created_at": 1620873306,
                "metadata": {},
                "failure_code": "",
                "failure_message": "",
                "paid": False,
                "paid_at": 0,
                "dispute": None,
                "refunds": None,
                "order": None,
                "outcome": None,
                "visual_codes": {
                    "qrcode_url": "https://d2o8h9r6avao9o.cloudfront.net/payments/3d641726-dbbb-4246-b2b6-8870214af483_qrcode.png",
                    "qrcode_image_base64": "iVBORw0KGgoAAAANSUhEUgAAANkAAADZCAMAAACaYGVEAAAABlBMVEUAAAD///+l2Z/dAAACFklEQVR42u3cS3KDQAwFQHP/S2ef8HmSBlxFena4AKtno5I09md76/qQkZGRkR3KPtX16zXXt+w+kH9YjoyMjIyM7FKW5Ilq2LtXwz1IvpaMjIyMLJSd5on46iwvFaqRbmRkZGRkZHfJgvojL3u66ZCMjIyM7FlZ/ly3oUVGRkZGtl7WrSq6Sa5bGd3ZlSMjIyP7B7L6NPipq8cn8GRkZGRvlnVXuWDJjyVNIyMjIyMjO5R1O1J37MiaWMjIyMjIUlk5tOFWDElJfUZGRkZGtj15Omn4zvxrycjIyMhSWb1WuCGmPH8WeldkZGRkZIcTiyBLlYcT06IkfhkZGRkZWXo66Y45RPnxcsbcv5OMjIyMbMvO6xeyxux00pqaplCfkZGRkZHVMsrSqUTen5r2rsjIyMjIriYWQQ7p5rM1vavTbSIjIyMjC2WFWmHWbhq+rDCxICMjIyMLJxbd4qJb4XTz4Gk+IyMjIyPbLn6J0G1hralwhpGRkZGRkaWycmIpN5jyJlm+yMjIyMhSWXd1i5J8t4JO1v4VGRkZGdm2+v/1uwOI8iS8Pv4gIyMjI2tNLLpD6KXj6vJukZGRkZGlsnJ/Ki9m8qHGMLeSkZGRkd0mWzpvHra+yMjIyMi+KeseWcoTWf3cFRkZGRnZZA5Rjinfybx3RUZGRkZWlHVjyrNifo6pPNEmIyMjI0tl71tkZGRkZH/XD1aPZdUxdE6nAAAAAElFTkSuQmCC"
                },
                "textual_codes": {
                    "pay_code": "paygw_918a67a47f36619070a31e0ea96599c0"
                },
                "instructions": [
                    {
                        "name": "instructions",
                        "steps": [
                            {
                                "step1": "Scan QR Code."
                            },
                            {
                                "step2": "Enter OTP to authorize Payment."
                            },
                            {
                                "step3": "Complete Payment."
                            }
                        ]
                    }
                ],
                "ewallet_id": "ewallet_1445a08ddab7e1ade98188a161159694",
                "ewallets": [
                    {
                        "ewallet_id": "ewallet_1445a08ddab7e1ade98188a161159694",
                        "amount": 3142.49,
                        "percent": 100,
                        "refunded_amount": 0
                    }
                ],
                "payment_method_options": {},
                "payment_method_type": "th_thaipromptpayqr_bank",
                "payment_method_type_category": "bank_transfer",
                "fx_rate": 1,
                "merchant_requested_currency": None,
                "merchant_requested_amount": None,
                "fixed_side": "",
                "payment_fees": None,
                "invoice": "",
                "escrow": None,
                "group_payment": "",
                "cancel_reason": None,
                "initiation_type": "customer_present",
                "mid": "",
                "next_action": "not_applicable"
            }
        }
        self.update(api, mode)

    def update_qrcode_query_process(self, withhold_receipt, expire_at):
        amount = round(withhold_receipt[0]["withhold_receipt_amount"] / 100, 2)
        api = "/v1/payments/" + global_rapyd_payment_id
        mode = {
            "status": {
                "error_code": "",
                "status": "SUCCESS",  # 表示创建支付请求成功
                "message": "",
                "response_code": "",
                "operation_id": "213c2354-639c-40de-b5c0-dc0ad369a7dc"
            },
            "data": {
                "id": global_rapyd_payment_id,  # 更新到withhold_receipt_channel_inner_key
                "amount": 0,
                "original_amount": amount,
                "is_partial": False,
                "currency_code": "THB",
                "country_code": "TH",
                "status": "ACT",  # 表示等待支付中
                "description": "",
                "merchant_reference_id": "",
                "customer_token": "cus_fc3304643a974680767eab599efe1619",
                "payment_method": "other_80239a6de2f5a5b6985f6ac2dcfc6d29",
                "payment_method_data": {
                    "id": "other_80239a6de2f5a5b6985f6ac2dcfc6d29",
                    "type": "th_thaipromptpayqr_bank",
                    "category": "bank_transfer",
                    "metadata": {},
                    "image": "",
                    "authentication_url": "",
                    "webhook_url": "",
                    "supporting_documentation": ""
                },
                "expiration": expire_at,
                "captured": True,
                "refunded": False,
                "refunded_amount": 0,
                "receipt_email": "",
                "redirect_url": "",
                "complete_payment_url": "",
                "error_payment_url": "",
                "receipt_number": "",
                "flow_type": "",
                "address": None,
                "statement_descriptor": "Saphhire Skysrapper Co",
                "transaction_id": "",
                "created_at": 1620961334,
                "metadata": {},
                "failure_code": "",
                "failure_message": "",
                "paid": False,
                "paid_at": 0,
                "dispute": None,
                "refunds": None,
                "order": None,
                "outcome": None,
                "visual_codes": {
                    "qrcode_url": "https://d2o8h9r6avao9o.cloudfront.net/payments/213c2354-639c-40de-b5c0-dc0ad369a7dc_qrcode.png",
                    "qrcode_image_base64": "iVBORw0KGgoAAAANSUhEUgAAANkAAADZCAMAAACaYGVEAAAABlBMVEUAAAD///+l2Z/dAAACDUlEQVR42u3bSXLDMAwEQPn/n845i6UZkHJSTvPmRbKaFxQw9PF413WQkZGRkT2VHe36cpuTzz5/5eyzH+8yfTIyMjIysktZUidOZAE3/6HFJyMjIyMjS2VBfQmqTVC6gnI4fjIyMjIysrtkRZkJ+o92J8nIyMjI/oBscQ/IyMjIyF4kq8tT8Ls5dzrsIiMjIyMrZX0a/KpXL0/gycjIyN5ZNl15AJGfQHpsWWRkZGRkz2V1Dam5i4lFH4iTkZGRkV3J8gBiGjlsTSxO3yQjIyMju5rw5JFDUInq4VMdUCf1jIyMjIxsRRb0LVP81hpJRkZGRjaTTR9tOoPaU93IyMjIyNIzPEWvsDNvno6pfr6cjIyMjOwx+f9ZEELvybCn7dI4gScjIyP7r7K8V6iD5sXdGmfmZGRkZGRdPau507andiZ3ISMjIyPbILsjrt5zSKmYXZGRkZGRrZwmrS/vm5K6cJKRkZGRjSY8dcJ8R2pdT7nIyMjIyFJZ3aJME4tjuJLuh4yMjIzsqWy6bnRO024yMjIyskvZnjFVTpruT3FSioyMjIysSyzy6CB/tWdjgluTkZGRkZWnk6b1ZToIy2trsgdkZGRkZL8hKxqPnaWSjIyMjOw2WR0rbOX2567IyMjIyEazq3pj6qefBuJkZGRkZJeyOqe+ozwtXkBGRkZGdil7v0VGRkZG9n19ANqjZ13sz1WoAAAAAElFTkSuQmCC"
                },
                "textual_codes": {
                    "pay_code": "paygw_efa3893d47a82032d624a86c8ba14421"
                },
                "instructions": [{
                    "name": "instructions",
                    "steps": [{
                        "step1": "Scan QR Code."
                    },
                        {
                            "step2": "Enter OTP to authorize Payment."
                        },
                        {
                            "step3": "Complete Payment."
                        }
                    ]
                }],
                "ewallet_id": "ewallet_1445a08ddab7e1ade98188a161159694",
                "ewallets": [{
                    "ewallet_id": "ewallet_1445a08ddab7e1ade98188a161159694",
                    "amount": 10,
                    "percent": 100,
                    "refunded_amount": 0
                }],
                "payment_method_options": {},
                "payment_method_type": "th_thaipromptpayqr_bank",
                "payment_method_type_category": "bank_transfer",
                "fx_rate": 1,
                "merchant_requested_currency": None,
                "merchant_requested_amount": None,
                "fixed_side": "",
                "payment_fees": None,
                "invoice": "",
                "escrow": None,
                "group_payment": "",
                "cancel_reason": None,
                "initiation_type": "customer_present",
                "mid": "",
                "next_action": "pending_confirmation"
            }
        }
        self.update(api, mode)

    def update_qrcode_query_500(self):
        api = "/v1/payments/" + global_rapyd_payment_id
        mode = {"_res": {"status": 500}}
        self.update(api, mode)
