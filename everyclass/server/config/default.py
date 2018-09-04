import json
import os

import git


class Config(object):
    """
    Basic Configurations
    """
    CONFIG_NAME = 'default'
    DEBUG = True
    SECRET_KEY = 'development_key'
    MYSQL_CONFIG = {
        'user'       : 'database_user',
        'password'   : 'database_password',
        'host'       : '127.0.0.1',
        'port'       : '6666',
        'database'   : 'everyclass',
        'use_unicode': True,
        'charset'    : 'utf8mb4'
    }
    SENTRY_CONFIG = {
    }
    ELASTIC_APM = {
        'SERVICE_NAME': 'everyclass-server',
        'SECRET_TOKEN': 'token',
        'SERVER_URL'  : 'http://127.0.0.1:8200',
    }

    """
    维护模式
    """
    MAINTENANCE_FILE = os.path.join(os.getcwd(), 'maintenance')
    if os.path.exists(MAINTENANCE_FILE):
        MAINTENANCE = True
    else:
        MAINTENANCE = False

    """
    静态文件、CDN 及网络优化
    """
    CDN_DOMAIN = 'cdn.domain.com'
    CDN_ENDPOINTS = ['images', 'static']
    CDN_TIMESTAMP = False
    HTML_MINIFY = True
    STATIC_VERSIONED = True
    with open(os.path.join(os.path.dirname(__file__), '../../../frontend/rev-manifest.json'), 'r') as static_manifest:
        STATIC_MANIFEST = json.load(static_manifest)

    """
    业务设置
    """
    DATA_LAST_UPDATE_TIME = '2018 年 7 月 2 日'  # 数据最后更新日期，在页面下方展示
    DEFAULT_SEMESTER = (2017, 2018, 1)
    AVAILABLE_SEMESTERS = {
        (2016, 2017, 2): {
            'start': (2017, 2, 20),
        },
        (2017, 2018, 1): {
            'start': (2017, 9, 4),
        },
        (2017, 2018, 2): {
            'start': (2018, 2, 26),
        },
        (2018, 2019, 1): {
            'start': (2018, 9, 3)
        }
    }

    # API
    API_CLIENTS = []

    """
    Git Hash
    """
    _git_repo = git.Repo(search_parent_directories=True)
    GIT_HASH = _git_repo.head.object.hexsha
    try:
        GIT_BRANCH_NAME = _git_repo.active_branch.name
    except TypeError:
        GIT_BRANCH_NAME = 'detached'
    _describe_raw = _git_repo.git.describe().split("-")  # like `v0.8.0-1-g000000`
    GIT_DESCRIBE = _describe_raw[0]  # actual tag name like `v0.8.0`
    if len(_describe_raw) > 1:
        GIT_DESCRIBE += "." + _describe_raw[1]  # tag 之后的 commit 计数，代表小版本
        # 最终结果类似于：v0.8.0.1