# -*- coding: utf-8 -*-
import json
import os
from pathlib import Path

JQDATA_HOME = os.environ.get('JQDATA_HOME')
if not JQDATA_HOME:
    JQDATA_HOME = os.path.abspath(os.path.join(Path.home(), 'jqdata-home'))

jqdata_env = {}


def init_env(username: str = None, password: str = None, jqdata_home: str = JQDATA_HOME) -> str:
    """

    :param username: 聚宽用户名，即注册手机号
    :param password: 密码
    :param jqdata_home: 配置存储路径，默认为~/jqdata-home
    """
    if not os.path.exists(jqdata_home):
        os.makedirs(jqdata_home)

    # create default config.json if not exist
    config_path = os.path.join(jqdata_home, 'config.json')
    if not os.path.exists(config_path):
        from shutil import copyfile
        copyfile(os.path.abspath(os.path.join(os.path.dirname(__file__), 'config.json')), config_path)

    with open(config_path) as f:
        config_json = json.load(f)
        for k in config_json:
            jqdata_env[k] = config_json[k]

    if username and password:
        jqdata_env['username'] = username
        jqdata_env['password'] = password
        with open(config_path, 'w+') as outfile:
            json.dump(jqdata_env, outfile)

    import pprint
    pprint.pprint(jqdata_env)

    return config_path


config_path = init_env()


def save_env():
    with open(config_path, 'w+') as outfile:
        json.dump(jqdata_env, outfile)


# the __all__ is generated
__all__ = ['init_env', 'save_env']

# __init__.py structure:
# common code of the package
# export interface in __all__ which contains __all__ of its sub modules

# import all from submodule api
from .api import *
from .api import __all__ as _api_all
__all__ += _api_all