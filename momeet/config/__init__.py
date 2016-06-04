#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from .local import *
from .dev import *
from .prod import *

__MAPPING = {
    'local.api': LocalApiConfig,
    'local.web': LocalWebConfig,
    'dev.api': DevApiConfig,
    'dev.web': DevWebConfig,
    'prod.api': ProdApiConfig,
    'prod.web': ProdWebConfig,
}
_ = os.environ.get('RUN_ENV', '')
if not _:
    _ = 'dev.web'

if _ not in __MAPPING:
    raise Exception("CONFIG ERROR")

c = __MAPPING.get(_)()
