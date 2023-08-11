import json

from foundation_test.config.oa.oa_interface_url_config import oa_base_url, approval_fake_url
from foundation_test.util.http.http_util import Http
from foundation_test.util.tools.tools import get_test_token

http = Http()


def oa_fake_approval_data(params):
    test_token = get_test_token()
    headers = {"Content-Type": "application/json", "testToken": test_token}
    request_data = json.loads(params)
    fake_url = oa_base_url + approval_fake_url
    resp = http.http_post(fake_url, request_data, headers)
    return json.dumps(request_data, ensure_ascii=False), resp.get('code'), json.dumps(resp, ensure_ascii=False)


if __name__ == "__main__":
    pass
