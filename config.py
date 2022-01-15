#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: Kylin Zhang
@license: Apache Licence
@file: config.py
@time: 2022.01.15
@contact: cnssr4bb1t@gmail.com
"""

STATUS_COLOR = {
    "OK": "\033[92m",  # GREEN
    "WARNING": "\033[93m",  # YELLOW
    "FAIL": "\033[91m",  # RED
    "INFO": "\033[96m",  # Blue
    "RESET": "\033[0m"  # RESET COLOR
}

# 这里添加账户
ACCOUNTS = {
    "account_1": {
        "address": "",
        "private_key": ""
    },
}