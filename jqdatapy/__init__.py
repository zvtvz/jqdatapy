# -*- coding: utf-8 -*-
import json
import os
from pathlib import Path

JQDATA_HOME = os.environ.get('JQDATA_HOME')
if not JQDATA_HOME:
    JQDATA_HOME = os.path.abspath(os.path.join(Path.home(), 'jqdata-home'))

jqdata_env = {}


def init_env(jqdata_home: str = JQDATA_HOME) -> None:
    """

    :param jqdata_home: home path for jqdata
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

    import pprint
    pprint.pprint(jqdata_env)

    return config_path


config_path = init_env()


def save_env():
    with open(config_path, 'w+') as outfile:
        json.dump(jqdata_env, outfile)
