#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: Kylin Zhang
@license: Apache Licence
@file: starry_util.py
@time: 2022.01.15
@contact: cnssr4bb1t@gmail.com
"""
import re
import time
import json
import datetime
import requests
from config import *
from web3.auto import w3
from eth_account.messages import encode_defunct

def do_sign(wallet_address, key):
    """
    返回经过签名认证之后的 authorization 字段
    """
    try:
        url_sign = 'https://app.starrynift.art/api/user/challenge'
        url_auth = 'https://app.starrynift.art/api/user/login'
        data_sign = {"address": wallet_address}

        headers_sign = {
            'Host': 'app.starrynift.art',
            'Connection': 'close',
            'Content-Length': '56',
            'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
            'DNT': '1',
            'sec-ch-ua-mobile': '?0',
            'Authorization': 'Bearer null',
            'Content-Type': 'application/json;charset=UTF-8',
            'Accept': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
            'sec-ch-ua-platform': '"macOS"',
            'Origin': 'https://app.starrynift.art',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://app.starrynift.art/play/',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6',
            'Cookie': '_ga=GA1.1.374469874.1637413335; __cf_bm=.g8LgiPDSbpOTjCnl67UE58lD2ricBes_Mvr7K8oIW4-1637413341-0-AUdpxGREF8yx3JKmoGLqG7ypN0EYjPMuqjqzg5816Q17vX4rvYgW6myLiuRjocStxY85o+EqyfAYSpWuIYOkoMZMtkD8JLQwub6VpDaEj2ta/1/WGtJiALm49gDoAlsZ9g==; _ga_B8C5YL5B0B=GS1.1.1637413274.80.1.1637414094.0',
        }
        r_sign = requests.post(url_sign, data=json.dumps(data_sign), headers=headers_sign)
        message = r_sign.json()['data']['message']
        msg = encode_defunct(text=message)
        sign = w3.eth.account.sign_message(msg, key)
        r = "signature=HexBytes\('(\w{132})'"
        signature = re.findall(r, str(sign))[0]

        data_auth = {'address': wallet_address,
                     'signature': signature}

        result = requests.post(url_auth, data=data_auth)
        authorization = 'Bearer ' + result.json()['data']['token']
        print(f"{STATUS_COLOR['OK']}[+] {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Get Authorization Success.{STATUS_COLOR['RESET']}")
        return authorization
    except Exception as e:
        print(f"{STATUS_COLOR['FAIL']}[-] {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Get Authorization Fail. Caused by {e}.{STATUS_COLOR['RESET']}")
        exit()
