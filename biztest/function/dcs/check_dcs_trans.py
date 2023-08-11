import json, time, unittest, pytest
import pandas as pd

from biztest.function.dcs.biz_database import get_asset
from biztest.function.dcs.capital_database import get_final_all, get_db_time, get_trans_all, get_clearing_rule_value, \
    get_buyback_dcs, get_trans_one, get_settlement_pending
import common.global_const as gc
from biztest.util.tools.tools import get_date_before_today


class CheckDcsTrans:
    def __init__(self, item_no, period, clearing_type, repay_channel, void='N'):
        """
        :param item_no:
        :param period:
        :param clearing_type:  还款还是代偿
        :param repay_channel:  我方／资方／我方和资方
        :param void:
        """
        self.env_test = gc.ENV
        self.item_no = item_no
        self.period = period
        self.clearing_type = clearing_type
        self.repay_channel = repay_channel  # 注意有资方参与代扣时不能用qsq，目前结算状态没有检查有资方代扣的场景
        self.void = void

    def assert_equal(self, excepts, actual, msg):
        unittest.TestCase().assertEqual(excepts, actual, msg)
        pass

    # 常规的检查
    def check_trans_all(self):
        final_all = get_final_all(self.item_no, self.period, self.clearing_type)
        trans_all = get_trans_all(self.item_no, self.period, self.clearing_type)
        print("###############", trans_all, "###############")
        if not trans_all:
            print("###############", get_db_time(), "###############")
            raise AssertionError('trans无数据！')
        not_comp_channel = ['mozhi_jinmeixin']
        # 1、检查 trans_type
        for final_i in range(0, len(final_all)):
            # 风险保障金和贷后管理费写repay_before_compensate
            # 墨智金美信不代偿本息
            if final_all[final_i]["compensated"] == "Y" and trans_all[final_i]["loan_channel"] in not_comp_channel and \
                    trans_all[final_i]["amount_type"] in ['consult']:
                self.assert_equal('repay_after_compensate', trans_all[final_i]["trans_type"], '不代偿本息，只代偿了consult')
                print("检查trans_type都是repay_after_compensate通过")
            elif final_all[final_i]["compensated"] == "Y" and trans_all[final_i]["loan_channel"] in not_comp_channel and \
                    trans_all[final_i]["amount_type"] not in ['consult']:
                self.assert_equal('repay_before_compensate', trans_all[final_i]["trans_type"],
                                  '除咨询服务费外，trans_type都是repay_before_compensate')
                print("检查trans_type都是repay_before_compensate通过")
            elif final_all[final_i]["compensated"] == "Y" and trans_all[final_i]["amount_type"] not in ["reserve",
                                                                                                        "after_loan_manage"]:
                self.assert_equal('repay_after_compensate', trans_all[final_i]["trans_type"],
                                  '除reserve和after_loan_manage之外，trans_type都是repay_after_compensate')
                print("检查trans_type都是repay_after_compensate通过")
            elif final_all[final_i]["biz_type"] == "Y" and trans_all[final_i]["amount_type"] in ["reserve",
                                                                                                 "after_loan_manage"]:
                self.assert_equal('repay_before_compensate', trans_all[final_i]["trans_type"],
                                  "风险保障金和贷后管理费都是repay_before_compensate")
                print("检查trans_type都是repay_before_compensate通过")
            elif final_all[final_i]["biz_type"] == "compensate" and final_all[final_i][
                "asset_loan_channel"] not in not_comp_channel:
                self.assert_equal('compensate', trans_all[final_i]["trans_type"], '代偿还款判断错误')
                print("检查 代偿 通过")
            elif final_all[final_i]["biz_type"] == "compensate" and final_all[final_i][
                "asset_loan_channel"] in not_comp_channel and final_all[final_i]["amount_type"] in ['consult']:
                self.assert_equal('compensate', trans_all[final_i]["trans_type"], '代偿还款判断错误')
                print("检查 墨智金美信 只代偿consult 通过")
            elif final_all[final_i]["asset_loan_channel"] not in not_comp_channel:
                self.assert_equal('repay_before_compensate', trans_all[final_i]["trans_type"], '代偿前还款判断错误')
                print("只要是资方代扣的就一定是代偿前")
        # 2、检查 存管 ，需要读取nacos (20201224修改方案为代码固定，若验证不通过，则表示程序有bug或者配置被擅动）
        qs_loan_channel = ["yunxin_quanhu", "hami_tianshan", "hami_tianshan_tianbang", "hamitianbang_xinjiang"]
        qjj_loan_channel = ["tongrongqianjingjing", "tongrongmiyang", "haohanqianjingjing"]
        zz_loan_channel = []
        # zz_loan_channel = ["qinnong", "mozhi_jinmeixin", "huabei_runqian"]
        # 代偿后仍由资方代扣
        channel_loan_channel = ["mozhi_beiyin_zhongyi"]
        bytb_channel_loan_channel = ["beiyin_tianbang"]
        channel_withhold_fess = ["consult", 'after_loan_manage', 'guarantee', 'reserve', 'risk_manage']
        for deposit_num in range(0, len(trans_all)):
            if final_all[deposit_num]["asset_loan_channel"] in qs_loan_channel:
                self.assert_equal("qs_tengqiao", trans_all[deposit_num]["deposit"], '全互和哈密结算qishang存管不正确')
                print("检查 存管 通过")
            elif final_all[deposit_num]["asset_loan_channel"] in qjj_loan_channel:
                self.assert_equal("qs_qianjingjing", trans_all[deposit_num]["deposit"], '兰州结算qianjingjing存管不正确')
                print("检查 存管 通过")
            elif final_all[deposit_num]["asset_loan_channel"] in zz_loan_channel:
                self.assert_equal("zz_tengqiao", trans_all[deposit_num]["deposit"], '结算应是zz_tengqiao存管，不正确')
                print("检查 存管 通过")
            # else:
            #     self.assert_equal("jining", trans_all[deposit_num]["deposit"], '默认结算jining存管不正确')
            #     print("检查 存管 通过")
            else:
                self.assert_equal("ht_tengqiao", trans_all[deposit_num]["deposit"], '默认结算ht_tengqiao存管不正确')
                print("检查 存管 通过")
        # 3、检查 出户 ，需要读取nacos (20201224修改方案为代码固定，若验证不通过，则表示程序有bug或者配置被擅动）
        for out_num in range(0, len(trans_all)):
            if self.clearing_type == 'repay':
                if final_all[out_num]["asset_loan_channel"] in qs_loan_channel:
                    self.assert_equal("v_tengqiao_hk", trans_all[out_num]["transfer_out"], '全互和哈密还款资产出户不正确')
                    print("检查 出户 通过")
                elif final_all[out_num]["asset_loan_channel"] in qjj_loan_channel:
                    self.assert_equal("v_qjj_hk", trans_all[out_num]["transfer_out"], '兰州还款资产出户不正确')
                    print("检查 出户 通过")
                elif final_all[out_num]["asset_loan_channel"] in zz_loan_channel:
                    self.assert_equal("v_tengqiao_hk", trans_all[out_num]["transfer_out"], '微神马还款资产出户不正确')
                    print("检查 出户 通过")
                # 墨智北银中裔 贷后管理费代偿后还款特殊处理
                elif trans_all[out_num]['amount_type'] in channel_withhold_fess \
                        and trans_all[out_num]["trans_type"] == 'repay_before_compensate' \
                        and trans_all[out_num]["amount_type"] == 'after_loan_manage' \
                        and "mozhi_beiyin_zhongyi_BAOFU_KUAINIU" in final_all[out_num]['withhold_result_channel']:
                    self.assert_equal("v_mozhi_rd_compensate", trans_all[out_num]["transfer_out"],
                                      '墨智after_loan_manage的代偿后还款出户不正确')
                    print("检查 after_loan_manage repay_before_compensate 出户 通过")
                # 墨智北银代偿前还款，费的出户为v_zydanbao_gj，本金利息不结算
                elif trans_all[out_num]['amount_type'] in channel_withhold_fess \
                        and trans_all[out_num]["trans_type"] == 'repay_before_compensate' \
                        and "mozhi_beiyin_zhongyi" in final_all[out_num]['withhold_result_channel']:
                    self.assert_equal("v_zydanbao_gj", trans_all[out_num]["transfer_out"], '墨智还款资产出户不正确')
                    print("检查 出户 通过")
                # 墨智jingmeixin代偿前还款，费的出户为v_mozhi_jinmeixin_gj，本金利息不结算
                elif trans_all[out_num]['amount_type'] in channel_withhold_fess \
                        and trans_all[out_num]["trans_type"] == 'repay_before_compensate' \
                        and "mozhi_jinmeixin" in final_all[out_num]['withhold_result_channel']:
                    self.assert_equal("v_mozhi_jinmeixin_gj", trans_all[out_num]["transfer_out"], '墨智jmx还款资产出户不正确')
                    print("检查 出户 通过")
                # 北银天邦代偿前还款，费的出户为v_tbdanbao_gj，本金利息不结算
                elif trans_all[out_num]['amount_type'] in channel_withhold_fess \
                        and trans_all[out_num]["trans_type"] == 'repay_before_compensate' \
                        and "beiyin_tianbang_BEIYIN" in final_all[out_num]['withhold_result_channel']:
                    self.assert_equal("v_tbdanbao_gj", trans_all[out_num]["transfer_out"], '北银天邦还款资产出户不正确')
                    print("检查 出户 通过")
                # 墨智北银代偿后还款，出户全部为v_mozhi_rd_compensate
                elif final_all[out_num]["asset_loan_channel"] in channel_loan_channel \
                        and trans_all[final_i]["trans_type"] == 'repay_after_compensate':
                    self.assert_equal("v_mozhi_rd_compensate", trans_all[out_num]["transfer_out"], '墨智还款资产出户不正确')
                    print("检查 出户 通过")
                # 北银天邦代偿后还款，v_tianbang_rd_compensate
                elif final_all[out_num]["asset_loan_channel"] in bytb_channel_loan_channel \
                        and trans_all[final_i]["trans_type"] == 'repay_after_compensate':
                    self.assert_equal("v_tianbang_rd_compensate", trans_all[out_num]["transfer_out"], '墨智还款资产出户不正确')
                    print("检查 出户 通过")
                elif trans_all[out_num]['amount_type'] in channel_withhold_fess \
                        and trans_all[out_num]["trans_type"] == 'repay_before_compensate' \
                        and "longjiang_daqin" in final_all[out_num]['withhold_result_channel']:
                    self.assert_equal("v_rd_daqinds", trans_all[out_num]["transfer_out"], '龙江还款资产出户不正确')
                    print("检查 出户 通过")

                # else:
                #     self.assert_equal("v_tengqiao_hf_hk", trans_all[out_num]["transfer_out"], '默认jining还款资产出户不正确')
                #     print("检查 出户 通过")
                else:
                    self.assert_equal("v_tengqiao_hk", trans_all[out_num]["transfer_out"], '默认qs_tengqiao还款资产出户不正确')
                    print("检查 出户 通过")
            else:
                self.assert_equal("v_hefei_weidu_bobei", trans_all[out_num]["transfer_out"], '代偿资产出户不正确')
                print("检查 出户 通过")
        # 4、检查 入户 （ 微神马有单独的逻辑）
        asset = get_asset(self.item_no)
        if asset is not None and asset["asset_product_code"]:  # 有product_code就需要去读取其专属的清分规则
            rule_value = get_clearing_rule_value(final_all[0]["asset_cmdb_no"], asset["asset_product_code"])
        else:  # 没有product_code就需要去读取原有的清分规则
            rule_value = get_clearing_rule_value(final_all[0]["asset_cmdb_no"])
        if rule_value is None:  # 可能有product_code，但是没有配置专属的清分规则，就用原来的
            rule_value = get_clearing_rule_value(final_all[0]["asset_cmdb_no"])
        rule_value = json.loads(rule_value)
        final_all = get_final_all(self.item_no, self.period, self.clearing_type)
        for rule_num in range(0, len(trans_all)):
            if trans_all[rule_num]["trans_type"] == "repay_after_compensate":
                self.assert_equal('v_hefei_weidu_bobei', trans_all[rule_num]["transfer_in"], '代偿后还款入户不正确')
                print("检查 入户 通过")
            elif final_all[rule_num]["partly"] == "N" and self.clearing_type == "compensate":  # 需要代偿本金 取 compensate_in
                rule_value_type = trans_all[rule_num]["amount_type"]
                self.assert_equal(rule_value["amount_type"][rule_value_type]["compensate_in"],
                                  trans_all[rule_num]["transfer_in"], '代偿入户不正确')
                print("检查 入户 通过")
            elif final_all[rule_num]["partly"] == "Y" and self.clearing_type == "compensate":
                rule_value_type = trans_all[rule_num]["amount_type"]
                self.assert_equal(rule_value["amount_type"][rule_value_type]["part_compensate_in"],
                                  trans_all[rule_num]["transfer_in"], '代偿入户不正确')
                print("检查 入户 通过")
            else:
                rule_value_type = trans_all[rule_num]["amount_type"]
                self.assert_equal(rule_value["amount_type"][rule_value_type]["transfer_in"],
                                  trans_all[rule_num]["transfer_in"], '其他代扣还款入户不正确')
                print("检查 入户 通过")
        # 5、检查 结算状态，需要读取配置，先不读
        for status_num in range(0, len(trans_all)):
            if trans_all[status_num]["transfer_out"] == trans_all[status_num]["transfer_in"]:
                self.assert_equal("Y", trans_all[status_num]["can_settlement"], '出入户一致能够结算')
                self.assert_equal("N", trans_all[status_num]["is_need_settlement"], '出入户一致不需要结清')
                self.assert_equal("finished", trans_all[status_num]["status"], '出入户一致结算状态不正确')
                print("检查 结算状态 通过")
            elif self.repay_channel == 'qsq':
                # self.assert_equal("Y", trans_all[status_num]["can_settlement"], '我方代扣能够结算')
                if trans_all[status_num]["transfer_out_channel_code"] == trans_all[status_num][
                    "transfer_in_channel_code"]:
                    self.assert_equal("N", trans_all[status_num]["is_need_settlement"], '出入户一致不需要结算')
                    self.assert_equal("finished", trans_all[status_num]["status"], '出入户一致结算状态直接为finished')
                    print("检查 结算状态 通过")
                else:
                    self.assert_equal("Y", trans_all[status_num]["is_need_settlement"], '我方代扣需要结算')
                    self.assert_equal("new", trans_all[status_num]["status"], '我方代扣结算状态不正确')
                    print("检查 结算状态 通过")
            else:
                print("资方代扣的需要精确到费用类型")
        # # 6、检查 expect_settlement_at
        # expect_settlement_channel = {
        #     "": [
        #         ""
        #     ]
        # }
        # for expect_settlement_num in range(0, len(trans_all)):
        #     if final_all[expect_settlement_num]["asset_loan_channel"] not in expect_settlement_channel \
        #             and final_all[expect_settlement_num]["amount_type"] == "principal":
        #         self.assert_equal("1000-01-01 00:00:00", trans_all[expect_settlement_num]["expect_settlement_at"], 'principal默认预计结算时间不正确')
        #         print("principal默认预计结算时间不正确")
        #     elif final_all[expect_settlement_num]["asset_loan_channel"] not in expect_settlement_channel \
        #             and final_all[expect_settlement_num]["amount_type"] == "interest":
        #         self.assert_equal("1000-01-01 00:00:00", trans_all[expect_settlement_num]["expect_settlement_at"], 'interest默认预计结算时间不正确')
        #         print("interest默认预计结算时间不正确")
        #     elif self.clearing_type == "repay":
        #         self.assert_equal(final_all()[expect_settlement_num]["actual_finish_time"],
        #                           trans_all[expect_settlement_num]["expect_settlement_at"][:10], '我方费用默认预计结算时间不正确')
        #         print("我方费用默认预计结算时间不正确")
        #     elif self.clearing_type == "compensate":
        #         self.assert_equal(final_all()[expect_settlement_num]["expect_finish_time"],
        #                           trans_all[expect_settlement_num]["expect_settlement_at"][:10], '我方费用默认预计结算时间不正确')
        #         print("我方费用默认预计结算时间不正确")
        #     else:
        #         self.assert_equal(get_date_before_today()[:10], trans_all[expect_settlement_num]["expect_settlement_at"][:10], '我方费用默认预计结算时间不正确')
        #         print("我方费用默认预计结算时间不正确")

    # 常规的检查金额
    def check_trans_amount(self):
        final_all = get_final_all(self.item_no, self.period, self.clearing_type)
        trans_all = get_trans_all(self.item_no, self.period, self.clearing_type)
        # 取出需要的列组装二维数组
        final_pd = pd.DataFrame(final_all, columns=[
            'asset_item_no', 'amount_type', 'amount'])
        trans_pd = pd.DataFrame(trans_all, columns=[
            'item_no', 'amount_type', 'amount'])
        # 排序
        final_sort = final_pd.sort_values(by=["amount_type"])
        trans_sort = trans_pd.sort_values(by=["amount_type"])
        compare_result = trans_sort.values == final_sort.values
        print("#########capital_sort###########")
        print(trans_sort.values)
        print("##########final_risk_sort##########")
        print(final_sort.values)
        self.assert_equal(compare_result.all(), True, '费用金额不正确')
        # 求和且返回和  axis 0为列，1为行
        trans_total_amount = trans_sort.filter(regex='amount').sum(axis=0)
        final_total_amount = final_sort.filter(regex='amount').sum(axis=0)
        return trans_total_amount["amount"], final_total_amount["amount"]

    # 提前结清的检查，目前只有华北小贷在用了
    def check_advance_clearing(self, channel, period_min, process_date, is_all='Y', clearing_type='repay'):
        """
        :param channel: 资金方
        :param period_min: 资产结清的最小期次
        :param process_date: 提前结清的推送时间，接口里的pushat，也是提前结清的时间
        :param is_all: 是否需要沾满利息（默认需要沾满）
        :param clearing_type: 本逻辑展示只检查还款的数据，该参数默认先不用传
        :return:
        """
        time.sleep(5.5)  # 有时候 buyback 数据生成比较晚，先等一会儿再执行，以免后面报错提示缺失 buyback
        final_all = get_final_all(self.item_no, self.period, clearing_type)
        trans_all = get_trans_all(self.item_no, self.period, clearing_type)
        buyback_dcs = get_buyback_dcs(self.item_no, self.period, channel)
        trans_interest = []
        trans_principal = []
        trans_guarantee = []
        interest_amount = 0

        # 先取出 trans 的本金和利息，因为目前只有利息有特殊处理
        for trans_i in range(0, len(trans_all)):
            if trans_all[trans_i]["amount_type"] == "interest":
                trans_interest = trans_interest + [trans_all[trans_i]]  # 最小期次只有一条，非最小期次有三条
            if trans_all[trans_i]["amount_type"] == "principal":
                trans_principal = trans_principal + [trans_all[trans_i]]  # 只有一条
            if trans_all[trans_i]["amount_type"] == "guarantee":
                trans_guarantee = trans_guarantee + [trans_all[trans_i]]  # 最小期次只有一条，非最小期次有三条

        if not buyback_dcs:
            print("###############", get_db_time(), "###############")
            raise AssertionError('buyback 无数据！')

        # 检查 buyback 本金和利息，注意最小期次的本息会满额
        for buyback_i in range(0, len(buyback_dcs)):
            if buyback_dcs[buyback_i]["amount_type"] == "principal" and self.period == period_min:
                self.assert_equal(buyback_dcs[buyback_i]["amount"], trans_principal[0]["amount"], '最小期次的 buyback 本金不正确')
            elif buyback_dcs[buyback_i]["amount_type"] == "interest" and self.period == period_min:
                print("###############", buyback_dcs[buyback_i])
                print("###############", trans_interest)
                # trans_all 搜索的数据进行了排序，同理 trans_interest 也是按照金额从小到大排序
                if is_all == 'N':
                    interest_amount = trans_interest[-1]["amount"] * 0.8  # 0.8 是写死的
                else:  # 否则利息是占满的
                    interest_amount = trans_interest[0]["amount"]
                self.assert_equal(buyback_dcs[buyback_i]["amount"], int(interest_amount), '最小期次的 buyback 利息不正确')
            elif buyback_dcs[buyback_i]["amount_type"] == "guarantee" and self.period == period_min:
                self.assert_equal(buyback_dcs[buyback_i]["amount"], trans_guarantee[0]["amount"],
                                  '最小期次的 buyback 担保费不正确')
            elif buyback_dcs[buyback_i]["amount_type"] == "principal" and self.period != period_min:
                self.assert_equal(buyback_dcs[buyback_i]["amount"], trans_principal[0]["amount"],
                                  '非最小期次的 buyback 本金不正确')
            else:
                self.assert_equal(buyback_dcs[buyback_i]["amount"], 0, '非最小期次的 buyback 利息不为0')
            # 检查 expect_compensate_at
            self.assert_equal(process_date, buyback_dcs[buyback_i]["expect_compensate_at"][:10],
                              'expect_compensate_at 不正确')
            self.assert_equal("new", buyback_dcs[buyback_i]["status"], 'status 不正确')

        self.assert_equal(process_date, final_all[0]["actual_finish_time"][:10], '提前结清完成时间不正确')

        # 检查重写的 trans ，重写的数据 withhold_serial_no 为 _our
        for trans_i in range(0, len(trans_interest)):
            # 结算给我方的数据
            if trans_interest[trans_i]["withhold_serial_no"][-4:] == '_our':
                # 入户是 清分规则的 part_repay_in
                rule_value = get_clearing_rule_value(final_all[0]["asset_cmdb_no"])
                rule_value = json.loads(rule_value)
                self.assert_equal(rule_value["amount_type"]["interest"]["part_repay_in"],
                                  trans_interest[trans_i]["transfer_in"], '重写入户part_repay_in不正确')
                # if channel in ["qinnong", "huabeixiaodai_zhitou", "hami_tianshan", "zhongke_lanzhou", "qinnong_jieyi"]:
                #     self.assert_equal("v_rs_servicefee", trans_interest[trans_i]["transfer_in"], '重写的入户不正确')
                # else:
                #     self.assert_equal("v_hefei_weidu_bobei", trans_interest[trans_i]["transfer_in"], '重写的入户不正确')
                self.assert_equal("Y", trans_interest[trans_i]["can_settlement"], '重写的结算状态不正确')
                if trans_interest[trans_i]["transfer_in"] == trans_interest[trans_i]["transfer_out"]:
                    self.assert_equal("N", trans_interest[trans_i]["is_need_settlement"], '重写的结算状态不正确')
                    self.assert_equal("finished", trans_interest[trans_i]["status"], '重写的结算状态不正确')
                else:
                    self.assert_equal("Y", trans_interest[trans_i]["is_need_settlement"], '重写的结算状态不正确')
                    self.assert_equal("new", trans_interest[trans_i]["status"], '重写的结算状态不正确')
            # cancel的数据
            elif trans_interest[trans_i]["withhold_serial_no"][-4:] != '_our' and self.period != period_min:
                self.assert_equal("cancel", trans_interest[trans_i]["status"], '原本结算状态不正确')
            # shoujin 首金结算给资方的费用
            if channel == "shoujin" and trans_interest[trans_i]["withhold_serial_no"][
                                        -8:] == '_capital' and self.period == period_min:
                self.assert_equal("v_shoujin", trans_interest[trans_i]["transfer_in"], '首金重写的入户不正确')
                self.assert_equal("N", trans_interest[trans_i]["can_settlement"], '首金重写的结算状态不正确')
                self.assert_equal("Y", trans_interest[trans_i]["is_need_settlement"], '首金重写的结算状态不正确')
                self.assert_equal("new", trans_interest[trans_i]["status"], '首金重写的结算状态不正确')
            # qinnong 秦农结算给资方的费用
            if channel in ["qinnong", "qinnong_jieyi"] and trans_interest[trans_i]["withhold_serial_no"][
                                                           -8:] == '_capital' and self.period == period_min:
                self.assert_equal("v_bx_qingnong_jining", trans_interest[trans_i]["transfer_in_channel_code"],
                                  '秦农重写的入户不正确')
                self.assert_equal("N", trans_interest[trans_i]["can_settlement"], '秦农重写的结算状态不正确')
                self.assert_equal("Y", trans_interest[trans_i]["is_need_settlement"], '秦农重写的结算状态不正确')
                self.assert_equal("new", trans_interest[trans_i]["status"], '秦农重写的结算状态不正确')
                self.assert_equal(interest_amount, trans_interest[trans_i]["amount"], '秦农最小期次给资方的金额不正确')
            # zhongke_lanzhou 兰州结算给资方的费用
            if channel == "zhongke_lanzhou" and trans_interest[trans_i]["withhold_serial_no"][
                                                -8:] == '_capital' and self.period == period_min:
                self.assert_equal("v_bx_lzzk", trans_interest[trans_i]["transfer_in"], '兰州重写的入户不正确')
                self.assert_equal("N", trans_interest[trans_i]["can_settlement"], '兰州重写的结算状态不正确')
                self.assert_equal("Y", trans_interest[trans_i]["is_need_settlement"], '兰州重写的结算状态不正确')
                self.assert_equal("new", trans_interest[trans_i]["status"], '兰州重写的结算状态不正确')
                self.assert_equal(int(interest_amount), int(trans_interest[trans_i]["amount"]), '兰州最小期次给资方的金额不正确')
        # 检查重写的 trans 的 担保费 ，重写的数据 withhold_serial_no 为 _our
        # 目前只有华北小贷的担保费会重写
        for trans_i in range(0, len(trans_guarantee)):
            if trans_guarantee[trans_i]["withhold_serial_no"][-4:] == '_our':
                # 入户是 清分规则的 part_repay_in
                rule_value = get_clearing_rule_value(final_all[0]["asset_cmdb_no"])
                rule_value = json.loads(rule_value)
                self.assert_equal(rule_value["amount_type"]["guarantee"]["part_repay_in"],
                                  trans_guarantee[trans_i]["transfer_in"], '重写入户part_repay_in不正确')
                self.assert_equal("Y", trans_guarantee[trans_i]["can_settlement"], '重写的结算状态不正确')
                if trans_guarantee[trans_i]["transfer_in"] == trans_guarantee[trans_i]["transfer_out"]:
                    self.assert_equal("N", trans_guarantee[trans_i]["is_need_settlement"], '重写的结算状态不正确')
                    self.assert_equal("finished", trans_guarantee[trans_i]["status"], '重写的结算状态不正确')
                else:
                    self.assert_equal("Y", trans_guarantee[trans_i]["is_need_settlement"], '重写的结算状态不正确')
                    self.assert_equal("new", trans_guarantee[trans_i]["status"], '重写的结算状态不正确')
            elif trans_guarantee[trans_i]["withhold_serial_no"][-4:] != '_our' and self.period != period_min:
                self.assert_equal("cancel", trans_interest[trans_i]["status"], '原本结算状态不正确')

    # 新模式的提前结清
    def check_settlement_notify_clearing(self, period_min, period, clearing_type, amount_type):
        # 一期一期的检查本金清分
        trans_all = get_trans_all(self.item_no, period, clearing_type)
        principal_pending = get_settlement_pending(self.item_no, period, "principal")
        interest_pending = get_settlement_pending(self.item_no, period, "interest")
        our_interest = None
        capital_interest = 0
        capital_interest1 = 0
        if amount_type == "guarantee":
            guarantee_pending = get_settlement_pending(self.item_no, period, "guarantee")
        for iii in range(0, len(trans_all)):  # 先把利息取出来
            if trans_all[iii]["amount_type"] == "interest":
                if trans_all[iii]["withhold_serial_no"][-4:] == "_our":
                    our_interest = trans_all[iii]
                elif trans_all[iii]["withhold_serial_no"][-8:] == "_capital":
                    capital_interest = capital_interest + trans_all[iii]["amount"]
                elif trans_all[iii]["status"] == "cancel":
                    interest_all = trans_all[iii]
                else:
                    capital_interest1 = trans_all[iii]["amount"]
        for iii in range(0, len(trans_all)):
            if trans_all[iii]["amount_type"] == "principal":  # 本金始终是全额，本金不管谁代扣都不会涉及重写，但是资方代扣的本金就不会更新
                self.assert_equal(principal_pending["settlement_amount"], trans_all[iii]["amount"], '本金结算金额不正确')
                print("检查 本金结算金额 通过")
                if trans_all[iii]["is_need_settlement"] == "Y":
                    self.assert_equal(principal_pending["repay_type"], trans_all[iii]["repay_type"], '本金结算类型不正确')
                    self.assert_equal(principal_pending["expect_operate_at"], trans_all[iii]["expect_settlement_at"],
                                      '本金结算时间不正确')
                    print("检查 本金结算时间 通过")
            elif trans_all[iii]["amount_type"] == "interest":
                if self.repay_channel == "qsq" and trans_all[iii]["withhold_serial_no"][-8:] == "_capital":
                    self.assert_equal(interest_pending["settlement_amount"], capital_interest, '给资方的利息金额不正确')
                    self.assert_equal("N", trans_all[iii]["can_settlement"], '给资方的利息结算状态can_settlement')
                    self.assert_equal("new", trans_all[iii]["status"], '给资方的利息结算状态new')
                    print("检查 给资方的利息 通过")
                elif self.repay_channel == "qsq_channel" and trans_all[iii]["withhold_serial_no"][-8:] == "_capital":
                    print("capital_interest1", capital_interest1)
                    c_interest = interest_pending["settlement_amount"] - capital_interest1
                    self.assert_equal(c_interest, capital_interest, '给资方的贴息金额不正确')
                    self.assert_equal("N", trans_all[iii]["can_settlement"], '给资方的贴息can_settlement')
                    self.assert_equal("new", trans_all[iii]["status"], '给资方的贴息new')
                    print("检查 给资方的贴息 通过")
                elif trans_all[iii]["withhold_serial_no"][-4:] == "_our":
                    i_interest = interest_all["amount"] - capital_interest
                    self.assert_equal(i_interest, our_interest["amount"], '给我方的利息结算金额不正确')
                    self.assert_equal("Y", our_interest["can_settlement"], '给我方的利息结算状态can_settlement')
                    # self.assert_equal("Y", our_interest["is_need_settlement"], '减免的利息is_need_settlement')
                    # self.assert_equal("new", our_interest["status"], '减免的利息状态new')
                    print("检查 给我方的利息 通过")
                    if trans_all[iii]["loan_channel"] in ["shilong_siping", "weishenma_daxinganling"]:
                        self.assert_equal("v_hefei_weidu_bobei", our_interest["transfer_in"], '减免的利息入户')
                        print(f"检查{trans_all[iii]['loan_channel']}减免的利息入户 通过")

                    elif trans_all[iii]["loan_channel"] in ["qinnong", "qinnong_jieyi"]:
                        self.assert_equal("v_hefei_weidu_bobei", our_interest["transfer_in"], '减免的利息入户')
                        print(f"检查{trans_all[iii]['loan_channel']}减免的利息入户 通过")
                    else:
                        self.assert_equal("v_rs_servicefee", our_interest["transfer_in"], '减免的利息入户')
                        print("检查 减免的利息入户 通过")
            elif trans_all[iii]["amount_type"] == "guarantee":
                if trans_all[iii]["transfer_out"] == "v_zydanbao_gj":  # 墨智资方代扣
                    self.assert_equal(guarantee_pending["settlement_amount"], trans_all[iii]["amount"],
                                      '墨智资方代扣担保费结算金额不正确')
                    print("检查 墨智资方代扣担保费结算金额 通过")
                elif trans_all[iii]["period"] == period_min and trans_all[iii][
                    "repay_type"] != "chargeback":  # 担保费一般只收当期
                    self.assert_equal(guarantee_pending["settlement_amount"], trans_all[iii]["amount"], '担保费结算金额不正确')
                    print("检查 担保费结算金额 通过")
                elif trans_all[iii]["period"] == period_min and trans_all[iii][
                    "repay_type"] == "chargeback":  # 担保费一般只收当期
                    print("待更新")
                elif trans_all[iii]["withhold_serial_no"][-4:] == "_our":
                    if trans_all[iii]["loan_channel"] in ["zhongke_lanzhou", 'mozhi_beiyin_zhongyi', 'huabei_runqian',
                                                          'longjiang_daqin', 'lanzhou_haoyue',
                                                          'lanzhou_dingsheng_zkbc2', 'zhongke_hegang']:
                        self.assert_equal("v_rs_servicefee", trans_all[iii]["transfer_in"], '减免的担保费入户')
                        print("检查 减免的担保费入户 通过")
                    else:
                        self.assert_equal("v_hefei_weidu_bobei", trans_all[iii]["transfer_in"], '减免的担保费入户')
                        print("检查 减免的担保费入户 通过")
                elif trans_all[iii]["withhold_serial_no"][-8:] == "_capital":
                    self.assert_equal("new", trans_all[iii]["status"], '未减免的担保费')
                    print("检查 未减免的担保费 通过")
                elif trans_all[iii]["transfer_out_channel_code"] == trans_all[iii]["transfer_in_channel_code"]:
                    self.assert_equal("finished", trans_all[iii]["status"], '担保费的入户和出户一样，直接finished')
                    print("检查 finished的担保费 通过")
                else:
                    self.assert_equal("cancel", trans_all[iii]["status"], 'cancel的担保费')
                    print("检查 cancel的担保费 通过")

    # 微神马的提前结清，只处理担保费 - 目前只有华北小袋尚在使用
    def check_wsm_advance_clearing(self, period_min, period, clearing_type, amount_type):
        # 一期一期的检查担保费清分
        final_all = get_final_all(self.item_no, period, clearing_type)
        trans_all = get_trans_all(self.item_no, period, clearing_type)
        rule_value = get_clearing_rule_value(final_all[0]["asset_cmdb_no"])
        rule_value = json.loads(rule_value)
        guarantee_pending = get_settlement_pending(self.item_no, period, "guarantee")
        if amount_type == "interest":
            interest_pending = get_settlement_pending(self.item_no, period, "interest")
            for iii in range(0, len(trans_all)):
                if trans_all[iii]["amount_type"] == "interest":
                    trans_interest = trans_all[iii]
                    self.assert_equal(interest_pending["repay_type"], trans_interest["repay_type"], 'repay_type不正确')
                    if trans_interest["period"] == period_min and trans_interest["withhold_serial_no"][
                                                                  -8:] == "_capital":
                        self.assert_equal(interest_pending["settlement_amount"], trans_interest["amount"],
                                          '利息结算给资方金额不正确')  # 结算给我方的利息暂时不验证
                        # self.assert_equal("v_weishenma", trans_interest["transfer_in"], '资方利息入户')
                        self.assert_equal(rule_value["amount_type"]["interest"]["transfer_in"],
                                          trans_interest["transfer_in"], '资方利息入户')
                    elif trans_interest["withhold_serial_no"][-4:] == "_our" and trans_all[iii][
                        "loan_channel"] == "weishenma_daxinganling":
                        self.assert_equal("v_hefei_weidu_bobei", trans_interest["transfer_in"], '微神马减免的利息入户')
                    elif trans_interest["withhold_serial_no"][-4:] == "_our" and trans_all[iii][
                        "loan_channel"] == "huabeixiaodai_zhitou":
                        self.assert_equal("v_rs_servicefee", trans_interest["transfer_in"], '华北小贷减免的利息入户')
                    else:
                        self.assert_equal("cancel", trans_interest["status"], 'cancel的担保费')
        for iii in range(0, len(trans_all)):
            if trans_all[iii]["amount_type"] == "guarantee":
                trans_guarantee = trans_all[iii]
                if clearing_type == "compensate":
                    self.assert_equal(guarantee_pending["repay_type"], trans_guarantee["repay_type"], 'repay_type不正确')
                if trans_guarantee["period"] == period_min and trans_guarantee[
                    "repay_type"] != "charge_back":  # 回购和提前结清的担保费一般只收当期，退单的担保费全部减免
                    self.assert_equal(guarantee_pending["settlement_amount"], trans_guarantee["amount"], '担保费结算金额不正确')
                elif trans_guarantee["withhold_serial_no"][-4:] == "_our" and trans_all[iii][
                    "loan_channel"] == "weishenma_daxinganling":
                    self.assert_equal("v_hefei_weidu_bobei", trans_guarantee["transfer_in"], '微神马减免的担保费入户')
                elif trans_guarantee["withhold_serial_no"][-4:] == "_our" and trans_all[iii][
                    "loan_channel"] == "huabeixiaodai_zhitou":
                    self.assert_equal("v_rs_servicefee", trans_guarantee["transfer_in"], '华北小贷减免的担保费入户')
                else:
                    self.assert_equal("cancel", trans_guarantee["status"], 'cancel的担保费')
