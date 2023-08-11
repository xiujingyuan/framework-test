import pytest
import redis

from biztest.util.db.db_util import DataBase
from biztest.util.nacos.nacos import Nacos

BASE_URL = {
    "china": {
        'biz': "https://biz-gateway-proxy.k8s-ingress-nginx.kuainiujinke.com/biz{0}-api",
        'repay': "https://biz-gateway-proxy.k8s-ingress-nginx.kuainiujinke.com/repay{0}",
        'grant': "https://biz-gateway-proxy.k8s-ingress-nginx.kuainiujinke.com/grant{0}",
        'biz-central': "https://biz-gateway-proxy.k8s-ingress-nginx.kuainiujinke.com/central{0}",
        'biz-dcs': "https://biz-gateway-proxy.k8s-ingress-nginx.kuainiujinke.com/biz-dcs-1",
        'grouter': "https://biz-gateway-proxy.k8s-ingress-nginx.kuainiujinke.com/grouter{0}",
        'contract': "https://biz-gateway-proxy.k8s-ingress-nginx.kuainiujinke.com/contract{0}",
        'cmdb': "https://biz-gateway-proxy.k8s-ingress-nginx.kuainiujinke.com/biz-cmdb1",
        "msgsender": "",
        'jaeger': "https://biz-tracing.k8s-ingress-nginx.kuainiujinke.com",
        'es': "http://biz-elasticsearch.k8s-ingress-nginx.kuainiujinke.com:80",
        'nacos': "nacos.k8s-ingress-nginx.kuainiujinke.com",
        'payment': "https://biz-gateway-proxy.k8s-ingress-nginx.kuainiujinke.com/biz-payment-staging",
        'deposit': "https://biz-gateway-proxy.k8s-ingress-nginx.kuainiujinke.com/biz-deposit",
    },
    "thailand": {
        'cmdb': "https://biz-gateway-proxy.starklotus.com/tha_cmdb{0}",
        "grant": "https://biz-gateway-proxy.starklotus.com/tha_grant{0}",
        'repay': "https://biz-gateway-proxy.starklotus.com/tha_repay{0}",
        'grouter': "https://biz-gateway-proxy.starklotus.com/tha_grouter{0}",
        'payment': "https://biz-gateway-proxy.starklotus.com/tha_payment{0}",
        'biz-dcs': "https://biz-gateway-proxy.starklotus.com/tha_dcs{0}",
        'jaeger': "http://jaeger.c99349d1eb3d045a4857270fb79311aa0.cn-shanghai.alicontainer.com",
        'es': "",
        'biz': '',
        'nacos': "nacos-test-tha.starklotus.com",
        "msgsender": "https://biz-gateway-proxy.starklotus.com/tha_msgsender",
        'deposit': ""
    },
    "india": {
        'cmdb': "https://biz-gateway-proxy.starklotus.com/ind_cmdb{0}",
        "grant": "https://biz-gateway-proxy.starklotus.com/ind_grant{0}",
        'repay': "https://biz-gateway-proxy.starklotus.com/ind_repay{0}",
        'grouter': "https://biz-gateway-proxy.starklotus.com/ind_grouter{0}",
        'payment': "https://biz-gateway-proxy.starklotus.com/ind_payment{0}",
        'biz-dcs': "https://biz-gateway-proxy.starklotus.com/ind_dcs{0}",
        'jaeger': "http://jaeger.c99349d1eb3d045a4857270fb79311aa0.cn-shanghai.alicontainer.com",
        'es': "",
        'biz': '',
        'nacos': "nacos-test-ind.starklotus.com",
        "msgsender": "",
        'deposit': ""
    },
    "philippines": {
        'cmdb': "https://biz-gateway-proxy.starklotus.com/phl_cmdb{0}",
        "grant": "https://biz-gateway-proxy.starklotus.com/phl_grant{0}",
        'repay': "https://biz-gateway-proxy.starklotus.com/phl_repay{0}",
        'grouter': "https://biz-gateway-proxy.starklotus.com/phl_grouter{0}",
        'payment': "https://biz-gateway-proxy.starklotus.com/phl_payment{0}",
        'biz-dcs': "https://biz-gateway-proxy.starklotus.com/phl_dcs{0}",
        'jaeger': "http://jaeger.c99349d1eb3d045a4857270fb79311aa0.cn-shanghai.alicontainer.com",
        'es': "",
        'biz': '',
        'nacos': "nacos-test-phl.starklotus.com",
        "msgsender": "",
        'deposit': ""
    },
    "mexico": {
        'cmdb': "https://biz-gateway-proxy.starklotus.com/mex_cmdb{0}",
        "grant": "https://biz-gateway-proxy.starklotus.com/mex_grant{0}",
        'repay': "https://biz-gateway-proxy.starklotus.com/mex_repay{0}",
        'grouter': "https://biz-gateway-proxy.starklotus.com/mex_grouter{0}",
        'payment': "https://biz-gateway-proxy.starklotus.com/mex_payment{0}",
        'biz-dcs': "https://biz-gateway-proxy.starklotus.com/mex_dcs{0}",
        'jaeger': "http://jaeger.c99349d1eb3d045a4857270fb79311aa0.cn-shanghai.alicontainer.com",
        'es': "",
        'biz': '',
        'nacos': "nacos-test-mex.starklotus.com",
        "msgsender": "",
        'deposit': ""
    },
    "pakistan": {
        'cmdb': "https://biz-gateway-proxy.starklotus.com/pak_cmdb{0}",
        "grant": "https://biz-gateway-proxy.starklotus.com/pak_grant{0}",
        'repay': "https://biz-gateway-proxy.starklotus.com/pak_repay{0}",
        'grouter': "https://biz-gateway-proxy.starklotus.com/pak_grouter{0}",
        'payment': "https://biz-gateway-proxy.starklotus.com/pak_payment{0}",
        'biz-dcs': "https://biz-gateway-proxy.starklotus.com/pak_dcs{0}",
        'jaeger': "http://jaeger.c99349d1eb3d045a4857270fb79311aa0.cn-shanghai.alicontainer.com",
        'es': "",
        'biz': '',
        'nacos': "nacos-test-pak.starklotus.com",
        "msgsender": "",
        'deposit': ""
    }
}

DB = {
    "china": {
        'biz': "biz{0}",
        'repay': "rbiz{0}",
        'grant': "gbiz{0}",
        'payment': 'payment_{0}',
        'deposit': 'tq_deposit1',
        'biz-dcs': "",
        'cmdb': 'cmdb_v1'
    },
    "thailand": {
        'repay': 'global_rbiz{0}_{1}',
        'grant': 'global_gbiz{0}_{1}',
        'payment': 'global_payment{0}_{1}',
        'biz-dcs': 'global_dcs{0}_{1}'
    },
    "india": {
        'repay': 'global_rbiz{0}_{1}',
        'grant': 'global_gbiz{0}_{1}',
        'payment': 'global_payment{0}_{1}',
        'biz-dcs': 'global_dcs{0}_{1}'
    },
    "philippines": {
        'repay': 'global_rbiz{0}_{1}',
        'grant': 'global_gbiz{0}_{1}',
        'payment': 'global_payment{0}_{1}',
        'biz-dcs': 'global_dcs{0}_{1}'
    },
    "mexico": {
        'repay': 'global_rbiz{0}_{1}',
        'grant': 'global_gbiz{0}_{1}',
        'payment': 'global_payment{0}_{1}',
        'biz-dcs': 'global_dcs{0}_{1}'
    },
    "pakistan": {
        'repay': 'global_rbiz{0}_{1}',
        'grant': 'global_gbiz{0}_{1}',
        'payment': 'global_payment{0}_{1}',
        'biz-dcs': 'global_dcs{0}_{1}'
    }
}

GRANT_ASSET_IMPORT_URL = "/paydayloan/asset-sync"
ROUTER_LOCALE_URL = "/router/locate"
PAYMENT_CALLBACK_URL = "/payment/callback"

JOB_GROUP_MAPPING_ENV = {
    "repay1": 53,
    "repay2": 122,
    "repay3": 55,
    "repay4": 56,
    "repay5": 57,
    "repay6": 58,
    "repay7": 59,
    "repay8": 59,
    "repay9": 60,
    "biz-central1": 130,
    "biz-central2": 131
}

GLOBAL_JOB_GROUP_MAPPING_ENV = {
    "global_rbiz1": 2,
    "global_rbiz1_thailand": 4,
    "global_rbiz1_philippines": 4,
    "dcs_tha": 5
}

PAYMENT_ENV_DICT = {
    "1": "test",
    "2": "staging",
    "3": "staging",
    "4": "staging",
    "5": "test",
    "6": "staging",
    "7": "test",
    "8": "staging",
    "9": "test"
}

REDIS_CONF = {
    "china": {
        "host": "175.24.253.104",
        "port": 6379,
        "password": "kuainiujinke"
    },
    "thailand": {
        "host": "xx.xx.xx.xx",
        "port": 6379,
        "password": "kuainiujinke"
    },
    "india": {
        "host": "81.69.165.99",
        "port": 6379,
        "password": "kuainiujinke"
    },
    "philippines": {
        "host": "xx.xx.xx.xx",
        "port": 6379,
        "password": "kuainiujinke"
    },
    "mexico": {
        "host": "xx.xx.xx.xx",
        "port": 6379,
        "password": "kuainiujinke"
    },
    "pakistan": {
        "host": "xx.xx.xx.xx",
        "port": 6379,
        "password": "kuainiujinke"
    }
}

DEFAULT_OPT = {
    "--env": 9,
    "--country": 'china',
    "--environment": 'dev'
}


def get_env_dict(env):
    env_d = PAYMENT_ENV_DICT
    env_test = env_d[str(env)]
    return env_test


def get_sysconfig(option):
    return pytest.config.getoption(option) if hasattr(pytest, 'config') else DEFAULT_OPT[option]


ENV = get_sysconfig('--env')
COUNTRY = get_sysconfig('--country')
ENVIRONMENT = get_sysconfig('--environment')
NACOS = Nacos(BASE_URL[COUNTRY]['nacos'])
GROUTER_URL = BASE_URL[COUNTRY]['grouter'].format(ENV)
GRANT_URL = BASE_URL[COUNTRY]['grant'].format(ENV)
REPAY_URL = BASE_URL[COUNTRY]['repay'].format(ENV)
BIZ_CENTRAL_URL = BASE_URL[COUNTRY]['biz-central'].format(ENV) if COUNTRY == 'china' else None
BIZ_URL = BASE_URL[COUNTRY]['biz'].format(ENV) if COUNTRY == 'china' else None
CONTRACT_URL = BASE_URL[COUNTRY]['contract'].format(ENV) if COUNTRY == 'china' else None
CMDB_URL = BASE_URL[COUNTRY]['cmdb'].format(ENV) if COUNTRY == 'china' else None
MSGSENDER_URL = BASE_URL[COUNTRY]['msgsender']
JAEGER_URL = BASE_URL[COUNTRY]['jaeger']
ES_URL = BASE_URL[COUNTRY]['es']
DCS_URL = BASE_URL[COUNTRY]['biz-dcs'].format(ENV)
PAYMENT_URL = BASE_URL[COUNTRY]['payment'].format(ENV) if COUNTRY != 'china' else BASE_URL[COUNTRY]['payment']
DEPOSIT_URL = BASE_URL[COUNTRY]['deposit'] if COUNTRY == 'china' else None

GRANT_DB = DataBase(DB[COUNTRY]['grant'].format(ENV), ENVIRONMENT) if COUNTRY == 'china' \
    else DataBase(DB[COUNTRY]['grant'].format(ENV, COUNTRY), ENVIRONMENT)
REPAY_DB = DataBase(DB[COUNTRY]['repay'].format(ENV), ENVIRONMENT) if COUNTRY == 'china' \
    else DataBase(DB[COUNTRY]['repay'].format(ENV, COUNTRY), ENVIRONMENT)
BIZ_DB = DataBase(DB[COUNTRY]['biz'].format(ENV, COUNTRY), ENVIRONMENT) if COUNTRY == 'china' else None
PAYMENT_DB = DataBase(DB[COUNTRY]['payment'].format(get_env_dict(ENV)), ENVIRONMENT) if COUNTRY == 'china' else \
    DataBase(DB[COUNTRY]['payment'].format(ENV, COUNTRY), ENVIRONMENT)
GLOBAL_DCS_DB = DataBase(DB[COUNTRY]['biz-dcs'].format(ENV, COUNTRY), ENVIRONMENT)
CMDB_DB = DataBase(DB[COUNTRY]['cmdb'], ENVIRONMENT) if COUNTRY == 'china' else None
JC_DB = DataBase('jc-mock', ENVIRONMENT)
DEPOSIT_DB = DataBase(DB[COUNTRY]['deposit'], ENVIRONMENT) if COUNTRY == 'china' else None

# 目前 约定 capital7对应biz3， capital6对应biz2
DCS_DB = DataBase(f"capital{int(ENV) + 4}", ENVIRONMENT)
DCS_DB_NAME = f"capital{int(ENV) + 4}"
DEPOSIT_DB_NAME = "tq_deposit1"
PAYMENT_DB_NAME = "payment_staging"

CONTRACT_DB = DataBase("contract", ENVIRONMENT)

GRANT_REDIS = redis.Redis(host=REDIS_CONF[COUNTRY]['host'], port=REDIS_CONF[COUNTRY]['port'],
                          password=REDIS_CONF[COUNTRY]['password'], db=0)


def init_public_env(env, country, environment):
    global ENV, COUNTRY, ENVIRONMENT, NACOS, JAEGER_URL, ES_URL, JC_DB
    ENV = env
    COUNTRY = country
    ENVIRONMENT = environment
    NACOS = Nacos(BASE_URL[country]['nacos'])
    JAEGER_URL = BASE_URL[country]['jaeger']
    ES_URL = BASE_URL[country]['es']
    JC_DB = DataBase('jc-mock', ENVIRONMENT)


def init_grant_env(env, country, environment):
    global GRANT_DB, GRANT_URL, GROUTER_URL, CONTRACT_URL, CMDB_URL, CONTRACT_DB, GRANT_REDIS, CMDB_DB
    GRANT_DB = DataBase(DB[country]['grant'].format(env), environment) if country == 'china' \
        else DataBase(DB[country]['grant'].format(env, country), environment)
    GRANT_URL = BASE_URL[country]['grant'].format(env)
    GROUTER_URL = BASE_URL[country]['grouter'].format(env)
    CONTRACT_URL = BASE_URL[country]['contract'].format(env) if country == 'china' else None
    CMDB_URL = BASE_URL[country]['cmdb'].format(env)
    CONTRACT_DB = DataBase("contract", environment) if country == 'china' else None
    GRANT_REDIS = redis.Redis(host=REDIS_CONF[COUNTRY]['host'], port=REDIS_CONF[COUNTRY]['port'],
                              password=REDIS_CONF[COUNTRY]['password'], db=0)
    CMDB_DB = DataBase(DB[country]['cmdb'], environment) if country == 'china' else None


def init_repay_env(env, country, environment):
    global REPAY_DB, REPAY_URL
    REPAY_DB = DataBase(DB[country]['repay'].format(env), environment) if COUNTRY == 'china' \
        else DataBase(DB[COUNTRY]['repay'].format(ENV, COUNTRY), environment)
    REPAY_URL = BASE_URL[country]['repay'].format(env)


def init_biz_env(env, country, environment):
    global BIZ_DB, BIZ_CENTRAL_URL, BIZ_URL, DCS_DB
    BIZ_DB = DataBase(DB[country]['biz'].format(env), environment) if country == 'china' else None
    BIZ_URL = BASE_URL[country]['biz'].format(env) if country == 'china' else None
    BIZ_CENTRAL_URL = BASE_URL[country]['biz-central'].format(env) if country == 'china' else None
    DCS_DB = DataBase(f"capital{int(ENV) + 4}", ENVIRONMENT)


def init_payment_env(env, country, environment):
    global PAYMENT_DB, PAYMENT_URL
    PAYMENT_DB = DataBase(DB[country]['payment'].format(get_env_dict(env)), environment) if country == 'china' else \
        DataBase(DB[country]['payment'].format(env, country), environment)
    PAYMENT_URL = BASE_URL[country]['payment'].format(env) if country != 'china' else BASE_URL[country]['payment']


def init_env(env, country, environment):
    # 工具环境初始化
    init_public_env(env, country, environment)
    init_grant_env(env, country, environment)
    init_repay_env(env, country, environment)
    init_biz_env(env, country, environment)
    init_payment_env(env, country, environment)


# pytest环境初始化
init_env(env=get_sysconfig('--env'), country=get_sysconfig('--country'), environment=get_sysconfig('--environment'))
