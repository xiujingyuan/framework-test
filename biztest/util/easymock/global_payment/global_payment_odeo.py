# -*- coding: utf-8 -*-

from biztest.util.http.http_util import Http


def odeo_notify_inquiry(va_number):
    url = 'http://api.staging.odeo.co.id/v1/test/pg/notify-inquiry'
    data = 'virtual_account_number=%s' % va_number
    header = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
              "Referer": "http://api.staging.odeo.co.id/v1/test/pg/a1hmMnlFZjhkUTBiQzg0ejEwNjNkY3pvR01GZVdCalc="}
    return Http.http_post(url, data, header)


def odeo_notify_payment(va_number, ret):
    url = 'http://api.staging.odeo.co.id/v1/test/pg/notify-payment'
    data = 'virtual_account_number=%s&amount=%s&trace_no=%s' % (va_number, ret["billingAmount"], ret["traceNo"])
    header = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
              "Referer": "http://api.staging.odeo.co.id/v1/test/pg/a1hmMnlFZjhkUTBiQzg0ejEwNjNkY3pvR01GZVdCalc="}
    return Http.http_post(url, data, header)


def odeo_notify_status_success(ret1, ret2):
    url = 'http://api.staging.odeo.co.id/v1/test/pg/notify-status'
    data = 'pg_payment_id=%s&pg_payment_status=50000&trace_no=%s' % (ret2["pgPaymentId"], ret1["traceNo"])
    header = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
              "Referer": "http://api.staging.odeo.co.id/v1/test/pg/a1hmMnlFZjhkUTBiQzg0ejEwNjNkY3pvR01GZVdCalc="}
    return Http.http_post(url, data, header)


def odeo_notify_status_fail(ret1, ret2):
    url = 'http://api.staging.odeo.co.id/v1/test/pg/notify-status'
    data = 'pg_payment_id=%s&pg_payment_status=90000&trace_no=%s' % (ret2["pgPaymentId"], ret1["traceNo"])
    header = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
              "Referer": "http://api.staging.odeo.co.id/v1/test/pg/a1hmMnlFZjhkUTBiQzg0ejEwNjNkY3pvR01GZVdCalc="}
    return Http.http_post(url, data, header)
