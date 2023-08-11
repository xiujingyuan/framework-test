from foundation_test.util.db.db_util import DataBase
import pytest


DB = {
    "china": {
        'fox': 'qsq_fox{0}'
    },
    "thailand": {
        'fox': 'arcticfox-thailand'
    },
    "philippines": {
        'fox': 'arcticfox-philippines'
    },
    "mexico": {
        'fox': 'arcticfox-mexico'
    },
    "india": {
        'fox': 'arcticfox-india'
    },
    "pakistan": {
        'fox': 'arcticfox-pakistan'
    }
}

DEFAULT_OPT = {
    "--env": 1,
    "--country": 'china',
    "--environment": 'test'
}


def get_sysconfig(option):
    return pytest.config.getoption(option) if hasattr(pytest, 'config') else DEFAULT_OPT[option]


ENV = get_sysconfig('--env')
COUNTRY = get_sysconfig('--country')
ENVIRONMENT = get_sysconfig('--environment')


DH_DB = DataBase(DB[COUNTRY]['fox'].format(ENV), ENVIRONMENT) if COUNTRY == 'china' \
    else DataBase(DB[COUNTRY]['fox'], ENVIRONMENT)


def init_dh_env(env, country, environment):
    global DH_DB
    # china中国、thailand泰国、philippines菲律宾、mexico墨西哥、pakistan巴基斯坦、india印度
    DH_DB = DataBase(DB[country]['fox'].format(env), environment) if country == 'china' \
        else DataBase(DB[country]['fox'], environment)


def init_env(env, country, environment):
    # 工具环境初始化
    init_dh_env(env, country, environment)


# pytest环境初始化
init_env(env=get_sysconfig('--env'), country=get_sysconfig('--country'), environment=get_sysconfig('--environment'))
