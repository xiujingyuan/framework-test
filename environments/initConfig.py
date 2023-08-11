# @Time    : 2021/1/7 7:11 下午
# @Author  : yuanxiujing
# @File    : initConfig.py
# @Software: PyCharm
from environments.dev.config_dev import dev_config
from environments.test.config_test import test_config
from foundation_test.util.tools.tools import get_sysconfig


def initConfig():
    if get_sysconfig("--environment") == "dev":
        result = dev_config()
    elif get_sysconfig("--environment") == "test":
        result = test_config()

    return result
