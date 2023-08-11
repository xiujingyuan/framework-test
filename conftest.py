#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @author: snow
 @software: PyCharm  
 @time: 2018/10/12
 @file: conftest.py
 @site:
 @email:
"""
import datetime
import html

import pytest

USER_OPTIONS = ["--project_system_name",
                "--system_module",
                "--ip",
                "--port",
                "--user",
                "--pwd",
                "--database",
                "--env",
                "--case_ids",
                "--environment",
                "--env_payment",
                "--item_no",
                "--country"]


def pytest_addoption(parser):
    parser.addoption("--project_system_name", action="store", default="",
                     help="run the case's project's name")

    parser.addoption("--system_module", action="store", default="",
                     help="input run which module's cases")

    parser.addoption("--ip", action="store",
                     help="input connect which ip")

    parser.addoption("--port", action="store",
                     help="input connect which port")

    parser.addoption("--user", action="store",
                     help="input connect database's user")

    parser.addoption("--pwd", action="store",
                     help="input connect database's pwd")

    parser.addoption("--database", action="store",
                     help="input connect which database")

    parser.addoption("--env", action="store",
                     help="input connect which database")

    parser.addoption("--env_payment", action="store",
                     help="input connect which database")

    parser.addoption("--case_ids", action="store",
                     help="input connect which database")

    parser.addoption("--environment", action="store",
                     help="input connect which database")

    parser.addoption("--item_no", action="store",
                     help="input connect which database")

    parser.addoption("--country", action="store",
                     help="input country")


@pytest.fixture
def project_system_name(request):
    return request.config.getoption("--project_system_name")


@pytest.fixture
def system_module(request):
    return request.config.getoption("--system_module")


@pytest.fixture
def env(request):
    return request.config.getoption("--env")


@pytest.fixture
def env_payment(request):
    return request.config.getoption("--env_payment")


@pytest.fixture
def case_ids(request):
    return request.config.getoption("--case_ids")


# @pytest.mark.optionalhook
# def pytest_html_results_table_header(cells):
#     # cells.pop(-1)  # 删除link列，标题
#     cells.insert(1, html.th('Description'))
#
#
# @pytest.mark.optionalhook
# def pytest_html_results_table_row(report, cells):
#     # cells.pop(-1)  # 删除link列，内容
#     cells.insert(1, html.td(report.description))
#
#
# def pytest_configure(config):
#     # 添加接口地址与项目名称
#     config._metadata['工作目录'] = 'https://jenkins-test.kuainiujinke.com/jenkins/job/Auto_Test_DH_asset_sync/ws'
#     config._metadata["项目名称"] = "Auto_Test_DH_asset_sync"
#     config._metadata['项目 Url'] = 'https://jenkins-test.kuainiujinke.com/jenkins/job/Auto_Test_DH_asset_sync/'
#
#     # 删除Java_Home
#     config._metadata.pop("Packages")
#     config._metadata.pop("Platform")
#     config._metadata.pop("Plugins")
#     config._metadata.pop("Python")

@pytest.fixture
def get_environment(request):
    return request.config.getoption("--environment")


@pytest.fixture
def get_country(request):
    return request.config.getoption("--country")


@pytest.fixture
def get_env(request):
    return request.config.getoption("--env")


def pytest_collection_modifyitems(items):
    """
    测试用例收集完成时，将收集到的item的name和nodeid的中文显示在控制台上
    :return:
    """
    for item in items:
        item.name = item.name.encode('utf-8').decode('unicode_escape')
        item._nodeid = item.nodeid.encode('utf-8').decode('unicode_escape')
