# -*- coding: utf-8 -*-
import io
import json
import string

import pandas as pd
import requests

from jqdatapy import jqdata_env, save_env

url = "https://dataapi.joinquant.com/apis"


def get_bars(code="600000.XSHG", count=10, unit='1d', end_date=None, fq_ref_date=None, return_type='df'):
    result = request_jqdata(method='get_bars', code=code, count=count, unit=unit, end_date=end_date,
                            fq_ref_date=fq_ref_date)
    if return_type == 'df':
        df = pd.read_csv(io.BytesIO(result), dtype=str)

        return df

    return result


def get_token(mob=None, pwd=None, force=False):
    """

    :param mob: 申请JQData时所填写的手机号
    :param pwd:  Password为聚宽官网登录密码，新申请用户默认为手机号后6位
    """
    # refresh mob pwd token
    if mob and pwd:
        jqdata_env["username"] = mob
        jqdata_env["password"] = pwd
        jqdata_env["token"] = _get_token(mob, pwd)

        save_env()
        return jqdata_env["token"]

    # refresh token
    if force:
        jqdata_env["token"] = _get_token(jqdata_env["username"], jqdata_env["password"])

        save_env()
        return jqdata_env["token"]

    # current token
    if jqdata_env["token"]:
        return jqdata_env["token"]


def request_jqdata(method: string, token: string = None, return_content=True, **kwargs):
    if not token:
        token = get_token(force=True)
    result = _request_jqdata(method=method, token=token, return_content=return_content, **kwargs)
    if result == 'error: token无效，请重新获取':
        result = _request_jqdata(method=method, token=get_token(force=True), return_content=return_content, **kwargs)

    return result


def _get_token(mob=None, pwd=None):
    body = {
        "method": "get_token",
        "mob": mob,
        "pwd": pwd,
    }
    response = requests.post(url, data=json.dumps(body))

    if response.status_code != 200:
        print(f"request jqdata error,code:{response.status_code},text:{response.text}")
        return None

    return response.text


def _request_jqdata(method: string, token: string = jqdata_env["token"], return_content=False, **kwargs):
    body = {
        "method": method,
        "token": token,
        **kwargs
    }
    response = requests.post(url, data=json.dumps(body))

    if response.status_code != 200:
        print(f"request jqdata error,code:{response.status_code},text:{response.text}")
        return None

    if return_content:
        return response.content
    return response.text


if __name__ == "__main__":
    print(get_bars(code='000338.XSHE'))
