# coding=utf-8
from foundation_test.interface.oa.oa_interface import oa_fake_approval_data
from foundation_test.util.tools.tools import *


@pytest.mark.oa_demo
def test_approval_demo():
    case_file = 'approval_v1_case.xlsx'
    log_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    result_file = 'approval_v1_result' + log_time + '.xlsx'
    datas = load_case_data(case_file)
    for case in datas:
        case_name = case['case_name']
        params = case['params'].replace('\n', '')
        expect_code = case['expect_code']
        is_exec = case['is_exec']
        if is_exec == 1:
            print(case_name)
            payload, code, result = oa_fake_approval_data(params)
            case['payload'] = payload
            case['status'] = 'pass' if code == expect_code else 'fail'
            case['result'] = result
        else:
            case['payload'] = ''
            case['status'] = 'skip'
            case['result'] = ''
    result_to_excel(result_file, datas)


if __name__ == '__main__':
    pass
