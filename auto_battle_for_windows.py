#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: Kylin Zhang
@license: Apache Licence
@file: auto_battle_for_windows.py
@time: 2022.01.15
@contact: cnssr4bb1t@gmail.com
"""
import re
import time
import json
import datetime
import requests
from web3 import Web3
from web3.auto import w3
from colorama import init, Fore
from eth_account.messages import encode_defunct

init(autoreset=True)


def do_sign(address, key):
    """
    返回经过签名认证之后的 authorization 字段
    """
    try:
        wallet_address = address
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
        print(f"{Fore.GREEN}[+] {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Get Authorization Success.")
        return authorization
    except Exception as e:
        print(
            f"{Fore.RED}[-] {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Get Authorization Fail. Caused by {e}.")
        exit()


def battle_prepare():
    preparation_url = "https://app.starrynift.art/api-v2/game/battle/preparation"
    data = json.dumps({})
    res = requests.post(url=preparation_url, data=data, headers=global_headers).json()
    avatars = list()
    items = list()
    for avatar in res['avatars']:
        if avatar['identity']['source'] == 1:  # 角色卡
            # 0质量，1重量，2token_id，3名称，4等级，5已战斗次数
            info = [avatar['quality'], avatar['weight'], avatar['identity']['id'], avatar['name'], avatar['level'],
                    avatar['quota'][0]]
            avatars.append(info)
    for item in res['items']:
        if item['identity']['source'] == 2:   # 装备卡
            # 0质量，1装备id，2名称，3数量，4部位
            info = [item['quality']+0.1, item['identity']['id'], item['name'], item['amount'], item['category']]
            items.append(info)
        elif item['identity']['source'] == 3:   # 装备卡
            # 0质量，1装备id，2名称，3数量，4部位
            info = [item['quality']+0.2, item['identity']['id'], item['name'], item['amount'], item['category']]
            items.append(info)
        else:
            pass
    avatars.sort()  # 排序，质量高的放后面，方便pop()
    items.sort(reverse=True)  # 排序，质量高的放前面
    items1 = list()
    items2 = list()
    items3 = list()
    items4 = list()
    items5 = list()
    items6 = list()
    for item in items:
        if item[4] == 1:
            if len(items1) < 4:
                for i in range(item[3]):
                    items1.append([item[1], item[0]])
                items1 = items1[:4]     # 取前四个
        elif item[4] == 2:
            if len(items2) < 4:
                for i in range(item[3]):
                    items2.append([item[1], item[0]])
                items2 = items2[:4]     # 取前四个
        elif item[4] == 3:
            if len(items3) < 4:
                for i in range(item[3]):
                    items3.append([item[1], item[0]])
                items3 = items3[:4]     # 取前四个
        elif item[4] == 4:
            if len(items4) < 4:
                for i in range(item[3]):
                    items4.append([item[1], item[0]])
                items4 = items4[:4]     # 取前四个
        elif item[4] == 5:
            if len(items5) < 4:
                for i in range(item[3]):
                    items5.append([item[1], item[0]])
                items5 = items5[:4]     # 取前四个
        elif item[4] == 6:
            if len(items6) < 4:
                for i in range(item[3]):
                    items6.append([item[1], item[0]])
                items6 = items6[:4]     # 取前四个
        else:
            pass
    prepared_items = [items1, items2, items3, items4, items5, items6]
    return avatars, prepared_items


def battle_create(avatars_battle, items_battle, times):
    global win
    global lose
    teams_count = len(avatars_battle)
    data = {
        "team": []
    }
    if is_wear != '0':
        for i in range(teams_count):
            structured = {
                "avatar": {
                    "source": 1,
                    "id": str(avatars_battle[i])
                },
                "items": [
                    {
                        "source": 2 if str(items_battle[0][i][1]).split(".")[1] == '1' else 3,
                        "id": str(items_battle[0][i][0]),
                        "category": 1
                    },
                    {
                        "source": 2 if str(items_battle[1][i][1]).split(".")[1] == '1' else 3,
                        "id": str(items_battle[1][i][0]),
                        "category": 2
                    },
                    {
                        "source": 2 if str(items_battle[2][i][1]).split(".")[1] == '1' else 3,
                        "id": str(items_battle[2][i][0]),
                        "category": 3
                    },
                    {
                        "source": 2 if str(items_battle[3][i][1]).split(".")[1] == '1' else 3,
                        "id": str(items_battle[3][i][0]),
                        "category": 4
                    },
                    {
                        "source": 2 if str(items_battle[4][i][1]).split(".")[1] == '1' else 3,
                        "id": str(items_battle[4][i][0]),
                        "category": 5
                    },
                    {
                        "source": 2 if str(items_battle[5][i][1]).split(".")[1] == '1' else 3,
                        "id": str(items_battle[5][i][0]),
                        "category": 6
                    },
                ]
            }
            data["team"].append(structured)
    else:
        for i in range(teams_count):
            structured = {
                "avatar": {
                    "source": 1,
                    "id": str(avatars_battle[i])
                },
                "items": []
            }
            data["team"].append(structured)
    battle_url = "https://app.starrynift.art/api-v2/game/battle/create"
    for i in range(times):
        try:
            res = requests.post(url=battle_url, data=json.dumps(data), headers=global_headers).json()
        except Exception as e:
            print(
                f"{Fore.RED}[-] {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Create battle failed. Caused by {e}.")
        if "errorCode" in res.keys():
            if res["errorCode"] == 5005:  # 对战次数到了
                print(
                    f"{Fore.YELLOW}[-] {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {res['message']} Team: {avatars_battle}")
                return
            elif res["errorCode"] == 5006:  # You need to wait at least 5 minutes to initiate a new battle.
                print(f"{Fore.RED}[-] {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {res['message']}")
                time.sleep(310)
            else:
                print(f"{Fore.RED}[-] {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {res}")
                exit()
        elif "statusCode" in res.keys():
            if res["statusCode"] == 429:  # ThrottlerException: Too Many Requests
                print(f"{Fore.RED}[-] {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {res['message']}")
                time.sleep(310)
            else:
                print(f"{Fore.RED}[-] {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {res}")
                exit()
        else:
            try:
                if res["evaluation"]["winner"] == res["side"]:
                    win += 1
                    print(
                        f"{Fore.GREEN}[+] {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Battle Win  | Odds:{str(round(win / (win + lose), 3) * 100)[:4]:4}% Opponent: {res['init']['players']['right']['name']} Team: {avatars_battle}")
                else:
                    lose += 1
                    print(
                        f"{Fore.RED}[-] {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Battle Lose | Odds:{str(round(win / (win + lose), 3) * 100)[:4]:4}% Opponent: {res['init']['players']['right']['name']} Team: {avatars_battle}")
                time.sleep(7)
            except Exception as e:
                print(res)
                exit()


if __name__ == '__main__':
    print(f"{Fore.YELLOW}*****\nStarryNift Auto Battle\nBy @19 From STARS GUILD 繁星公会\n*****\n\n")
    battle_count = int(input(f"{Fore.GREEN}[?] 出战人数(1-4): "))
    if battle_count not in [1, 2, 3, 4]:
        exit()
    is_wear = input(f"{Fore.GREEN}[?] 是否穿戴装备(0不穿，其他穿): ")
    is_unlimit = input(f"{Fore.GREEN}[?] 没有卡之后是否循环等待新的卡尝试对战(0不循环，其他循环): ")
    with open("./account.txt") as f:
        content = f.readlines()
    accounts = []
    for account in content:
        accounts.append([Web3.toChecksumAddress(account.strip().split("----")[0]), account.strip().split("----")[1]])
    for account in accounts:
        address = account[0]
        private_key = account[1]
        print(f"{Fore.GREEN}[+] Current Address: {address}")
        auth = do_sign(address, private_key)  # 获取签名token
        global_headers = {
            'Host': 'app.starrynift.art',
            'Connection': 'close',
            'Content-Length': '2',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
            'DNT': '1',
            'sec-ch-ua-mobile': '?0',
            'Authorization': auth,
            'Content-Type': 'application/json;charset=UTF-8',
            'Accept': 'application/json, text/plain, */*',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
            'sec-ch-ua-platform': '"macOS"',
            'Origin': 'https://app.starrynift.art',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://app.starrynift.art/battlegame/',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6',
            'Cookie': '_ga=GA1.1.2137279765.1638733403; __cf_bm=BXqcDSHyJQTLrLhPfv344PiDrn6wY0Z1_UwKEVod2g0-1639988756-0-AVkJROGWYN5JrS/EUe6+6ossza79TcvLywcF1dP+jrODWKnu00M+lEiIyDyt394XPUPPqe6q7gSfKOpciOa4fFiGYWlkOeVAg7LNYchWduxgbYP2Areo4vg3GQWQ/+kvGg==; _ga_B8C5YL5B0B=GS1.1.1639988598.217.1.1639988796.0'
        }

        win = 0
        lose = 0
        team_serial = 0

        while True:
            battle_teams = []
            avatars, items = battle_prepare()
            print(f"{Fore.GREEN}[+] {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Get Equipment Success.")
            min_times = float("inf")  # 无穷大
            while True:
                try:
                    avatar = avatars.pop()
                    if avatar[5] < 5:
                        battle_teams.append(avatar[2])
                        if 5 - avatar[5] < min_times:
                            min_times = 5 - avatar[5]
                except IndexError:
                    print(f"{Fore.YELLOW}[-] {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} No nft remains.")
                    break
                if len(battle_teams) == battle_count:
                    break
            if battle_teams:
                team_serial += 1
                print(
                    f"\n{Fore.YELLOW}[+] {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Team serial: {team_serial}")
                battle_create(battle_teams, items, min_times)
            if not len(avatars):
                if win + lose > 0:
                    msg = f"StarryNift Auto Battle\n" \
                          f"地址：{address}\n" \
                          f"数据：Win: {win}  Lose: {lose}  Rate:{round(win / (win + lose), 3) * 100}%"
                    print(msg)
                    time.sleep(60)
                if is_unlimit != '0':
                    print(
                        f"{Fore.YELLOW}[-] {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Sleep 10 minutes and wait new nfts.")
                    time.sleep(600)  # 没有卡了之后，暂停10分钟，再看
                    continue
                else:
                    break
            print(
                f"{Fore.YELLOW}[-] {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} One team battle done. Have a rest for 10 seconds.")
            time.sleep(10)
