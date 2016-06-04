#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ._base import ApiConfig, WebConfig

all = ['ProdApiConfig', 'ProdWebConfig']


class ProdMixin(object):
    pass


class ProdApiConfig(ProdMixin, ApiConfig):
    pass


class ProdWebConfig(ProdMixin, WebConfig):
    pass
