# -*- coding: utf-8 -*-
from .context import init_test_context

init_test_context()

from jqdatapy.api import get_token


def test_pass():
    try:
        print(get_token())
    except:
        assert False
