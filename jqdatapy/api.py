# -*- coding: utf-8 -*-
import io
import json
import string

import pandas as pd
import requests

from jqdatapy import jqdata_env, save_env, init_env

url = "https://dataapi.joinquant.com/apis"

jqdata_session = requests.Session()

class HttpAccessError(Exception):
    def __init__(self, code, msg):
        self.code = code
        self.msg = msg

    def __str__(self) -> str:
        return f'code:{self.code},msg:{self.msg}'


def run_query(table='finance.STK_EXCHANGE_TRADE_INFO', columns=None, conditions=None, count=1000,
              dtype={'code': str, 'symbol': str}, parse_dates=['day', 'pub_date']):
    return request_jqdata(method='run_query', table=table, columns=columns, conditions=conditions, count=count,
                          dtype=dtype, parse_dates=parse_dates)


def get_query_count():
    return request_jqdata(method='get_query_count',parse_dates=None)


def get_money_flow(code, date, end_date=None):
    """
    :param code: 股票代码
    :param date: 开始日期
    :param end_date: 结束日期
    :return:
    """
    return request_jqdata(method='get_money_flow', code=code, date=date, end_date=end_date, parse_dates=['date'])


def get_future_contracts(code='AG', date=None):
    """

    :param code:  期货合约品种，如 'AG'(白银)
    :param date: 指定日期，默认为None，不指定时返回当前日期下可交易的合约标的列表
    """
    return request_jqdata(method='get_future_contracts', code=code, date=date, parse_dates=None)


def get_security_info(code='AG2012.XSGE'):
    """

    :param code:  期货合约品种，如 'AG'(白银)
    """
    return request_jqdata(method='get_security_info', code=code, parse_dates=['start_date', 'end_date'])


def get_dominant_future(code='AG', date=None):
    """

    :param code:  期货合约品种，如 'AG'(白银)
    :param date: 指定日期参数，获取历史上该日期的主力期货合约
    """
    return request_jqdata(method='get_dominant_future', code=code, date=date, parse_dates=None)


def get_all_securities(code='stock', date=None):
    """

    :param code: 证券类型,可选: stock, fund, index, futures, etf, lof, fja, fjb, QDII_fund, open_fund, bond_fund, stock_fund, money_market_fund, mixture_fund, options
    :param date: 日期，用于获取某日期还在上市的证券信息，date为空时表示获取所有日期的标的信息
    """
    return request_jqdata(method='get_all_securities', code=code, date=date, parse_dates=None)


def get_trade_days(date='1990-01-01', end_date=None):
    """

    :param date: 开始日期
    :param end_date: 结束日期
    """
    return request_jqdata(method='get_trade_days', date=date, end_date=end_date, parse_dates=False, header=None)


def get_fundamentals(table='balance', columns=None, code='000001.XSHE', date=None, count=1000,
                     parse_dates=['day', 'pubDate']):
    """

    :param table: 要查询表名，可选项balance，income，cash_flow，indicator，valuation，bank_indicator，security_indicator，insurance_indicator
    :param columns: 所查字段，为空时则查询所有字段，多个字段中间用,分隔。如id,company_id，columns不能有空格等特殊字符
    :param code: 证券代码，多个标的使用,分隔
    :param date: 查询日期2019-03-04或者年度2018或者季度2018q1 2018q2 2018q3 2018q4
    :param count: 查询条数，最多查询1000条。不填count时按date查询
    :return:
    """

    return request_jqdata(method='get_fundamentals', table=table, columns=columns, code=code, date=date, count=count,
                          parse_dates=parse_dates)


def get_mtss(code='000001.XSHE', date='2005-01-01', end_date=None):
    """

    :param code: 股票代码
    :param date: 开始日期
    :param end_date:te: 结束日期
    :return:
    """
    return request_jqdata(method='get_mtss', code=code, date=date, end_date=end_date, parse_dates=['date'])


def get_all_trade_days():
    return request_jqdata(method='get_all_trade_days', parse_dates=False, header=None)


def get_bars(code="600000.XSHG", count=10, unit='1d', end_date=None, fq_ref_date=None, return_type='df',
             parse_dates=['date']):
    return request_jqdata(method='get_bars', code=code, count=count, unit=unit, end_date=end_date,
                          fq_ref_date=fq_ref_date, return_type=return_type, parse_dates=parse_dates)


def get_price_period(code="600000.XSHG", unit='1d', date='2005-01-01', end_date=None, fq_ref_date=None,
                     return_type='df', parse_dates=['date']):
    """

    :param code: 证券代码
    :param unit: bar的时间单位, 支持如下周期：1m, 5m, 15m, 30m, 60m, 120m, 1d, 1w, 1M。其中m表示分钟，d表示天，w表示周，M表示月
    当unit是1w或1M时，第一条数据是开始时间date所在的周或月的行情。当unit为分钟时，第一条数据是开始时间date所在的一个unit切片的行情。
    最大获取1000个交易日数据
    :param date: 开始时间，不能为空，格式2018-07-03或2018-07-03 10:40:00，如果是2018-07-03则默认为2018-07-03 00:00:00
    :param end_date: 结束时间，不能为空，格式2018-07-03或2018-07-03 10:40:00，如果是2018-07-03则默认为2018-07-03 23:59:00
    :param fq_ref_date: 复权基准日期，该参数为空时返回不复权数据
    :param return_type:
    :param parse_dates:
    :return:
    """
    return request_jqdata(method='get_price_period', code=code, unit=unit, date=date, end_date=end_date,
                          fq_ref_date=fq_ref_date, return_type=return_type, parse_dates=parse_dates)


def get_bars_period(code="600000.XSHG", unit='1d', date=None, end_date=None, fq_ref_date=None, return_type='df',
                    parse_dates=['date']):
    return get_price_period(code=code, unit=unit, date=date, end_date=end_date, fq_ref_date=fq_ref_date,
                            return_type=return_type,
                            parse_dates=parse_dates)


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


def request_jqdata(method: string, token: string = None, return_type='df', dtype={'code': str}, parse_dates=['day'],
                   header='infer', **kwargs):
    if not token:
        token = get_token(force=True)
    resp = _request_jqdata(method=method, token=token, **kwargs)
    if resp.text == 'error: token无效，请重新获取':
        resp = _request_jqdata(method=method, token=get_token(force=True), **kwargs)

    if return_type == 'df':
        if not resp.content:
            return None
        df = pd.read_csv(io.BytesIO(resp.content), dtype=dtype, header=header, parse_dates=parse_dates)
        return df

    return resp.content


def _get_token(mob=None, pwd=None):
    body = {
        "method": "get_token",
        "mob": mob,
        "pwd": pwd,
    }
    response = requests.post(url, data=json.dumps(body))

    if response.status_code != 200:
        print(f"request jqdata error,code:{response.status_code},text:{response.text}")
        raise HttpAccessError(code=response.status_code, msg=response.text)

    return response.text


def _request_jqdata(method: string, token: string = jqdata_env["token"], **kwargs):
    body = {
        "method": method,
        "token": token,
        **kwargs
    }
    response = jqdata_session.post(url, data=json.dumps(body))

    if response.status_code != 200:
        print(f"request jqdata error,code:{response.status_code},text:{response.text}")
        raise HttpAccessError(code=response.status_code, msg=response.text)

    return response


# custom api

if __name__ == "__main__":
    pd.set_option('expand_frame_repr', False)
    pd.set_option('mode.chained_assignment', 'raise')

    # print(get_bars(code='000338.XSHE'))
    # print(get_all_securities())
    # print(get_trade_days())
    # print(get_trade_days())
    # print(get_fundamentals(count=10, columns='day,pubDate', parse_dates=None))
    # print(get_mtss())
    # print(run_query(count=10, parse_dates=None))
    # print(get_all_securities(code='futures'))
    # print(get_future_contracts())
    print(get_dominant_future())
    print(get_bars(code='AU9999.XSGE'))
    print(get_security_info())
    # print(get_price_period(end_date='2010-01-01'))
    # print(get_query_count())

# the __all__ is generated
__all__ = ['HttpAccessError', 'run_query', 'get_money_flow', 'get_future_contracts', 'get_security_info',
           'get_dominant_future', 'get_all_securities', 'get_trade_days', 'get_fundamentals', 'get_mtss',
           'get_all_trade_days', 'get_bars', 'get_price_period', 'get_bars_period', 'get_token', 'request_jqdata']
