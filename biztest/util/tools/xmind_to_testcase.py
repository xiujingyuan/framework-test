import csv
import logging
import os

import pandas as pd
from xmind2testcase.utils import get_absolute_path
from xmind2testcase.utils import get_xmind_testcase_list


def xmind_to_tapd_excel_file(xmind_file):
    """Convert XMind file to a csv file"""
    xmind_file = get_absolute_path(xmind_file)
    logging.info('Start converting XMind file(%s) to file...', xmind_file)
    testcases = get_xmind_testcase_list(xmind_file)

    fileheader = ["用例目录", "用例名称", "前置条件", "用例步骤", "预期结果", "用例状态", "用例等级", "用例类型"]
    tapd_testcase_rows = [fileheader]
    for testcase in testcases:
        row = gen_a_testcase_row(testcase)
        # print(testcase)
        tapd_testcase_rows.append(row)

    csv_file = xmind_file[:-6] + '.csv'
    tapd_file = xmind_file[:-6] + '.xlsx'
    if os.path.exists(tapd_file):
        os.remove(tapd_file)

    with open(csv_file, 'w', encoding='utf8') as f:
        writer = csv.writer(f)
        writer.writerows(tapd_testcase_rows)
        logging.info('Convert XMind file(%s) to a tapd xlxs file(%s) successfully!', xmind_file, csv_file)
    read_file = pd.read_csv(csv_file)
    read_file.to_excel(tapd_file, index=None, header=True)
    if os.path.exists(csv_file):
        os.remove(csv_file)
    return tapd_file


def gen_a_testcase_row(testcase_dict):
    case_module = gen_case_module(testcase_dict['product'], testcase_dict['suite'])
    case_title = testcase_dict['name']
    case_precontion = testcase_dict['preconditions']
    case_step, case_expected_result = gen_case_step_and_expected_result(testcase_dict['steps'])
    case_keyword = '正常'
    case_priority = gen_case_priority(testcase_dict['importance'])
    case_type = gen_case_type(testcase_dict['execution_type'])
    # case_result = gen_case_result(testcase_dict['result'])
    # case_apply_phase = '迭代测试'
    row = [case_module, case_title, case_precontion, case_step, case_expected_result, case_keyword, case_priority,
           case_type]
    return row


def gen_case_module(product_name, module_name):
    if module_name:
        module_name = module_name.replace('（', '(')
        module_name = module_name.replace('）', ')')
    else:
        module_name = '/'
    dir_name = product_name + "-" + module_name
    return dir_name


def gen_case_step_and_expected_result(steps):
    case_step = ''
    case_expected_result = ''

    for step_dict in steps:
        case_step += str(step_dict['step_number']) + '. ' + step_dict['actions'].replace('\n', '').strip() + '\n'
        case_expected_result += str(step_dict['step_number']) + '. ' + \
                                step_dict['expectedresults'].replace('\n', '').strip() + '\n' \
            if step_dict.get('expectedresults', '') else ''

    return case_step, case_expected_result


def gen_case_priority(priority):
    mapping = {1: '高', 2: '中', 3: '低'}
    if priority in mapping.keys():
        return mapping[priority]
    else:
        return '中'


def gen_case_type(case_type):
    mapping = {1: '功能测试', 2: '性能测试'}
    if case_type in mapping.keys():
        return mapping[case_type]
    else:
        return '功能测试'


def gen_case_result(case_result):
    mapping = {1: '是', 0: '否'}
    if case_result in mapping.keys():
        return mapping[case_result]
    else:
        return '否'


def main():
    xmind_file = '小单权责分配重构V1.xmind'
    print('Start to convert XMind file: %s' % xmind_file)
    tapd_xls_file = xmind_to_tapd_excel_file(xmind_file)
    print('Convert XMind file to tapd excel file successfully: %s' % tapd_xls_file)
    print('Finished conversion, Congratulations!')


if __name__ == '__main__':
    main()
