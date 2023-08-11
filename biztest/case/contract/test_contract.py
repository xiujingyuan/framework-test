#!/usr/bin/python
# -*- coding: UTF-8 -*-
from biztest.config.contract.contract_interface_params_config import app_subject_dict
from biztest.config.easymock.easymock_config import gbiz_mock
from biztest.function.contract.contract_common_function import *
from biztest.function.contract.contract_check_function import *
from biztest.config.contract.contract_kv_config import *
from biztest.util.easymock.gbiz.yixin_rongsheng import YiXinRongShengMock
from biztest.util.task.task import TaskContract
from biztest.util.easymock.contract import ContractMock


class TestContract:

    def setup_class(self):
        monitor_check()
        # contractsvr_interface.warning_pool_size("ssqUploadPool", 10) -----签约系统设置线程池，控制并发的，用不上了，并且该接口现在404了
        update_contract_capital_config()
        update_contract_sign_config()
        self.mock = ContractMock("contract")
        self.task = TaskContract()

    @classmethod
    def teardown_class(cls):
        pass

    def setup_method(self):
        self.mock.update_accrual_info()

    @pytest.mark.contract
    @pytest.mark.parametrize("sign_company, need_sign, contract_types",
                             [("my", True, (21612, 21614)),
                              ("tq", True, (21612, 21614)),
                              ("hm", False, ()),
                              ])
    def test_bind_success_contract(self, sign_company, need_sign, contract_types):
        """
        绑卡成功签合同
        """
        opportunity = "BindSuccess"
        four_element = get_four_element()
        # 调用绑卡签合同接口
        bind_success_sign(four_element, sign_company)
        if need_sign:
            # 执行task
            self.task.run_task(four_element['data']['id_number_encrypt'], opportunity, excepts={"code": 0})
            self.task.run_task_until_close_or_timeout(four_element['data']['id_number_encrypt'])
            # 检查合同
            check_contract(four_element['data']['id_number_encrypt'], opportunity, contract_types)
        else:
            check_task_not_exist(four_element['data']['id_number_encrypt'], opportunity)

    @pytest.mark.contract
    @pytest.mark.parametrize("from_system_name, sub_type, contract_types",
                             [
                                 ("香蕉", "risk", (20710, 20720, 20760, 20761, 20762, 20763, 20764, 20765, 20766)),
                                 # ("杭州草莓", "authenticate", (20715, 20725)),
                                 # ("杭州草莓", "diversion", (20751, ))
                             ])
    def test_before_import_contract(self, from_system_name, sub_type, contract_types):
        """
        测试进件前签合同
        """
        opportunity = "BeforeImport"
        item_no = "B{}".format(get_item_no())
        four_element = get_four_element()
        # 调用进件前签合同接口
        before_import_sign(item_no, four_element, sub_type, from_system_name)
        # 执行task
        self.task.run_task(four_element['data']['id_number_encrypt'], opportunity, excepts={"code": 0})
        self.task.run_task_until_close_or_timeout(four_element['data']['id_number_encrypt'])
        # 检查合同
        check_contract(four_element['data']['id_number_encrypt'], opportunity, contract_types)

    # @pytest.mark.contract
    @pytest.mark.parametrize("channel, from_system_name, contract_types",
                             [("shoujin", "杭州草莓", (30150,)),
                              ("shoujin", "香蕉", (30150,))])
    def test_before_register_contract(self, channel, from_system_name, contract_types):
        """
        测试开户前签合同
        """
        opportunity = "BeforeRegister"
        item_no = "BR{}".format(get_item_no())
        four_element = get_four_element()
        # 调用开户前签合同接口
        before_register_sign(channel, from_system_name, item_no, four_element)
        # 执行task
        self.task.run_task(item_no, opportunity, excepts={"code": 0})
        self.task.run_task_until_close_or_timeout(item_no)
        # 检查合同
        check_contract(item_no, opportunity, contract_types, app_subject_dict[from_system_name])

    @pytest.mark.contract
    @pytest.mark.parametrize("channel, period, from_system_name, contract_types",
                             [
                                 ("yilian_dingfeng", 12, "香蕉", (31700, 31715, 31716, 31717, 31703, 31704)),
                                 ("zhenong_rongsheng", 12, "香蕉", (33900,)),
                                 ("zhongyuan_zunhao", 12, "香蕉", (33006,)),
                                 ("hebei_jiahexing_ts", 12, "香蕉", (35000, 35001, 35002, 35003)),
                                 ("hayin_zhongbao", 12, "香蕉", (35301, 35302, 35303, 35304, 35305, 35306))
                             ])
    def test_import_contract(self, channel, period, from_system_name, contract_types):
        """
        测试进件时签合同
        """
        opportunity = "AssetImport"
        # 造资产数据：进件状态
        item_no, asset_info, item_no_noloan, asset_info_noloan = make_asset_data("sale", channel=channel, period=period,
                                                                                 from_system_name=from_system_name)
        # 执行task
        self.task.run_task(item_no, opportunity)
        self.task.run_task_until_close_or_timeout(item_no)
        # 检查合同
        if channel == 'zhongyuan_zunhao':
            check_contract(item_no, opportunity, contract_types, "sz-biz-contract-test")
        else:
            check_contract(item_no, opportunity, contract_types, app_subject_dict[from_system_name])

    @pytest.mark.contract
    @pytest.mark.parametrize("channel, period, from_system_name, contract_types",
                             [
                                 ("yixin_rongsheng", 12, "香蕉", (33406, 33405)),
                                 ("yilian_dingfeng", 12, "香蕉", (31706, 31714)),
                                 ("lanzhou_haoyue", 12, "香蕉", (31100, 30601)),
                             ])
    def test_before_apply_contract(self, channel, period, from_system_name, contract_types):
        """
        试算成功后，进件资方前签合同
        """
        capital_mock = YiXinRongShengMock(gbiz_mock)
        capital_mock.update_repay_trial()
        opportunity = "BeforeApply"
        # 造资产数据：进件状态
        item_no, asset_info, item_no_noloan, asset_info_noloan = make_asset_data("sale", channel=channel, period=period,
                                                                                 from_system_name=from_system_name)
        # 调用试算成功签合同接口
        before_apply_sign(asset_info)
        # 执行task
        self.task.run_task(item_no, opportunity, excepts={"code": 0})
        self.task.run_task_until_close_or_timeout(item_no)
        # 检查合同
        check_contract(item_no, opportunity, contract_types, app_subject_dict[from_system_name])

    @pytest.mark.contract
    @pytest.mark.parametrize("channel, period, status, contract_types",
                             [
                                 # ("tongrongqianjingjing", 12, "repay", (30501, 30502, 30506)),
                                 # ("tongrongqianjingjing", 12, "writeoff", (30501, 30502, 30506)),
                                 # ("tongrongqianjingjing", 12, "payoff", (30501, 30502, 30506)),
                                 # ("tongrongqianjingjing", 12, "void", ()),
                                 # ("haohanqianjingjing", 12, "repay", (30750, 30751, 30752, 30501, 30502, 30506)),
                                 # ("lanzhou_haoyue", 12, "repay", (31102, 30505, 30504, 30508)),
                                 # ("lanzhou_haoyue_qinjia", 12, "repay", (32005, 32008, 32009, 30504, 30505)),
                                 # ("yilian_dingfeng", 12, "repay", (31711, 31712, 30504, 30505, 31708, 31709)),
                                 # ("zhongke_hegang", 12, "repay", (30746, 30748, 30504, 30505)),
                                 # 上面几个资方较老，合同仍然在用，自动执行先屏蔽，本地测试可打开执行
                                 ("jincheng_hanchen", 12, "repay", (30504, 31908)),
                                 ("zhongyuan_zunhao", 12, "repay", (33010, 33007, 33008)),
                                 ("yixin_rongsheng", 6, "repay", (33407, 30504, 33408)),
                                 ("yumin_zhongbao", 12, "repay", (33500, 33504, 33505, 33506, 33507)),
                                 ("zhongbang_zhongji", 12, "repay", (34301, 34302, 30504, 30505))
                             ])
    def test_withdraw_success_contract(self, channel, period, status, contract_types):
        """
        测试放款成功签合同
        """
        opportunity = "AssetWithdrawSuccess"
        # 造资产数据：还款状态
        item_no, asset_info, item_no_noloan, asset_info_noloan = make_asset_data(status, channel=channel, period=period)
        # 调用放款成功签合同接口
        withdraw_success_sign(asset_info)
        # 执行task
        self.task.run_task(item_no, opportunity)
        self.task.run_task_until_close_or_timeout(item_no)
        # 检查合同
        check_contract(item_no, opportunity, contract_types)

    @pytest.mark.contract
    @pytest.mark.parametrize(
        "from_system_name, part, benefit_company_code, status, noloan_source_type, sub_order_type, contract_types",
        [
            ("香蕉", "如皋智萃", "v_sh_lingte", "repay", "rongdan", "tianbang",
             (20950, 20960, 20930, 20931, 20910, 20911, 20902, 20903, 20904, 20905, 20711)),
            ("香蕉", "如皋智萃", "v_sh_lingte", "repay", "rongdan", "daqin",
             (20951, 20961, 20932, 20933, 20910, 20911, 20902, 20903, 20904, 20905, 20711)),
            ("香蕉", "如皋智萃", "v_sh_lingte", "repay", "rongdan_irr", "runqian",
             (20952, 20962, 20934, 20935, 20910, 20911, 20902, 20903, 20904, 20905, 20711)),
            ("香蕉", "如皋智萃", "v_sh_lingte", "repay", "lieyin", "",
             (21211, 20833, 20836, 20821, 20822, 20812, 20813, 20814, 20815, 20843, 20716)),
            ("香蕉", "如皋智萃", "v_sh_lingte", "repay", "rongdan", "",
             (20711, 20960, 20930, 20931, 20910, 20911, 20902, 20903, 20904, 20905, 20950)),
            ("香蕉", "如皋智萃", "v_sh_lingte", "repay", "rongdan_irr", "",
             (20711, 20960, 20930, 20931, 20910, 20911, 20902, 20903, 20904, 20905, 20950)),
            ("香蕉", "苏州", "", "void", "lieyin", "", ())
        ])
    def test_withdraw_success_contract_noloan(self, from_system_name, part, benefit_company_code, status,
                                              noloan_source_type,
                                              sub_order_type,
                                              contract_types):
        """
        测试小单放款成功签合同
        双场景：
        1、大单进件，放款成功
        2、小单进件，放款成功（进件app：香蕉）
        3、mock中造part数据为如皋智萃，benefit_company_code不为运营平台
        4、执行合同task
        5、预期合同签约签约分润公司的相关协议，签B4协议
        单场景：
        1、大单进件，放款成功
        2、小单进件，放款成功（进件app：草莓）
        3、mock中造part数据为如皋智萃，benefit_company_code为运营平台
        4、执行合同task
        5、预期合同签约不签分润公司的相关协议，不签B4协议
        """
        opportunity = "AssetWithdrawSuccess"
        item_no, asset_info, item_no_noloan, asset_info_noloan = make_asset_data(status,
                                                                                 noloan_source_type=noloan_source_type,
                                                                                 from_system_name=from_system_name)
        # 修改sub_order_type
        update_asset_extend_by_item_no(item_no_noloan, asset_extend_sub_order_type=sub_order_type)
        # 调用放款成功签合同接口
        withdraw_success_sign(asset_info_noloan)

        self.mock.update_accrual_info(part, benefit_company_code)
        # 执行task
        self.task.run_task(item_no_noloan, opportunity)
        self.task.run_task_until_close_or_timeout(item_no_noloan)
        time.sleep(10)
        # 检查合同
        check_contract(item_no_noloan, opportunity, contract_types)

    # @pytest.mark.contract
    @pytest.mark.parametrize("old_system_name, new_system_name, contract_types",
                             [("香蕉", "杭州草莓", (20714,)),
                              ("杭州草莓", "香蕉", (20714,))])
    def test_diversion_contract(self, old_system_name, new_system_name, contract_types):
        """
        测试导流签合同
        :param old_system_name:
        :param new_system_name:
        :param contract_types:
        :return:
        """
        opportunity = "Diversion"
        # 造资产数据：进件状态
        item_no, asset_info = make_asset_data("sale", from_system_name=old_system_name)
        # 调用导流签合同接口
        diversion_sign(item_no, new_system_name)
        # 执行task
        self.task.run_task(item_no, opportunity, excepts={"code": 0})
        self.task.run_task_until_close_or_timeout(item_no)
        # 检查合同
        check_contract(item_no, opportunity, contract_types, app_subject_dict[new_system_name])

    @pytest.mark.contract
    @pytest.mark.parametrize("old_channel, old_contract_types, new_channel, new_contract_types",
                             [("yilian_dingfeng", (31700, 31715, 31716, 31717, 31703, 31704),
                               "lanzhou_haoyue_qinjia", (32007, 32006, 32010))])
    def test_change_channel_contract(self, old_channel, old_contract_types, new_channel, new_contract_types):
        """
        测试切资方签合同
        :param old_channel:
        :param old_contract_types:
        :param new_channel:
        :param new_contract_types:
        :return:
        """
        opportunity = "AssetImport"
        # 1、资产进件签合同
        item_no, asset_info, item_no_noloan, asset_info_noloan = make_asset_data("sale", channel=old_channel)
        self.task.run_task(item_no, opportunity, excepts={"code": 0})
        self.task.run_task_until_close_or_timeout(item_no)
        check_contract(item_no, opportunity, old_contract_types, expect_status="SUCCESS")
        # 2、切资方
        do_change_capital(item_no, old_channel, new_channel)
        time.sleep(10)
        # 3、检查之前的合同已作废
        self.task.run_task(item_no, "AssetChannelChange")
        check_contract(item_no, opportunity, old_contract_types, expect_status="VOID")
        # 4、检查新资方合同签成功
        self.task.run_task_until_close_or_timeout(item_no)
        check_contract(item_no, opportunity, new_contract_types, expect_status="SUCCESS")

    @pytest.mark.contract
    @pytest.mark.parametrize("noloan_source_type, sub_order_type, period, contract_types",
                             [("rongdan_irr", "tianbang", 3, (22403, 22503, 22603, 22703)),
                              ("lieyin", "", 3, (21803, 21903, 22103, 22003)),
                              ])
    def test_payoff_asset_contract(self, noloan_source_type, sub_order_type, period, contract_types):
        """
        资产逾期结清签合同
        """
        opportunity = "PayoffAsset"
        # 造资产数据：还款状态
        item_no, asset_info, item_no_noloan, asset_info_noloan = make_asset_data("repay", period=12,
                                                                                 noloan_source_type=noloan_source_type)
        # 修改sub_order_type
        update_asset_extend_by_item_no(item_no_noloan, asset_extend_sub_order_type=sub_order_type)
        # 调用资产结清签合同接口
        payoff_asset_sign(item_no_noloan, period)
        # 执行task
        self.task.run_task(item_no_noloan, "AssetPayoff", excepts={"code": 0})
        self.task.run_task_until_close_or_timeout(item_no_noloan)
        # 检查合同
        check_contract(item_no_noloan, opportunity, contract_types)

    @pytest.mark.contract
    @pytest.mark.parametrize("channel, period, loan_contract_code, loan_contact_type, guarantee_company",
                             [
                                 # ("qinnong", 12, "KN#item_no#", None, "陕西天邦融资担保有限公司"),
                                 # ("qinnong_jieyi", 12, "KN#item_no#", None, "陕西杰益融资担保有限公司"),
                                 # ("qinnong_dingfeng", 12, "KN#item_no#", None, "云南鼎丰融资担保有限公司"),
                                 # ("hami_tianshan_tianbang", 12, "#contract_code#", 30181, "陕西天邦融资担保有限公司"),
                                 # ("huabei_runqian", 12, "#item_no#", None, "深圳市润乾融资担保有限公司"),
                                 # ("zhongke_lanzhou", 12, "#item_no#", None, "黑龙江鼎盛融资担保有限公司"),
                                 # 以上资方未放量，先屏蔽
                                 ("lanzhou_haoyue", 12, "#item_no#", None, "陕西昊悦融资担保有限公司"),
                                 # ("weipin_zhongwei", 12, "#item_no#", None, "陕西中为融资担保有限公司"),
                             ])
    def test_fox_contract(self, channel, period, loan_contract_code, loan_contact_type, guarantee_company):
        """
        贷后法催签合同
        """
        opportunity = "FoxContractSign"
        fox_contract_lt = [23000, 23001, 23002]
        # 造资产数据：sale状态
        item_no, asset_info, item_no_noloan, asset_info_noloan = make_asset_data("sale", channel=channel, period=period)
        update_asset(item_no, asset_due_at='2020-12-01 00:00:00')
        # 执行task
        self.task.run_task_until_close_or_timeout(item_no)

        for contract_type in fox_contract_lt:
            # 调用贷后法催签合同接口
            fox_sign(item_no, contract_type)
            # 执行task
            self.task.run_task_until_close_or_timeout(item_no)
            # 检查合同
            check_contract_info(item_no, opportunity, contract_type, contract_status='SUCCESS')
            if "#contract_code#" in loan_contract_code:
                contract_code = get_contract(item_no, "AssetImport", loan_contact_type)[0]['contract_code']
                expect_loan_contract_code = loan_contract_code.replace('#contract_code#', contract_code)
            else:
                expect_loan_contract_code = loan_contract_code.replace('#item_no#', item_no)
            # 检查通知消息的债转参数
            check_sendmsg_data(item_no, debt_transfer_date='2020-12-10',
                               loan_contract_code=expect_loan_contract_code,
                               guarantee_company=guarantee_company)

    @pytest.mark.contract
    def test_before_import_void(self):
        """
        根据身份证号作废合同
        """
        opportunity = "BeforeImportVoid"
        item_no = get_item_no() + "BIV"
        create_contract(item_no, 20710, "测试合同-预期作废", "http://test.pdf", "BeforeImport")
        create_contract(item_no, 30000, "测试合同-预期不作废", "http://test.pdf", "AssetImport")
        # 调用作废合同接口
        before_import_void(item_no)
        # 执行task
        self.task.run_task(item_no, opportunity, excepts={"code": 0})
        self.task.run_task_until_close_or_timeout(item_no)
        # 检查合同
        check_contract_info(item_no, "BeforeImport", 20710, contract_status="VOID")
        check_contract_info(item_no, "AssetImport", 30000, contract_status="SUCCESS")
