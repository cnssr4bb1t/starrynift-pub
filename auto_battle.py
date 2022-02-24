#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: Kylin Zhang
@license: Apache Licence
@file: auto_battle.py
@time: 2022.01.15
@contact: cnssr4bb1t@gmail.com
"""
import pyfiglet
import argparse
from starry_util import *


def battle_prepare():
    preparation_url = "https://app.starrynift.art/api-v2/game/battle/preparation"
    data = json.dumps({})
    res = requests.post(url=preparation_url, data=data, headers=global_headers).json()
    avatars = list()
    items = list()
    for avatar in res['avatars']:
        if avatar['identity']['source'] == 1:   # 角色卡
            # 0质量，1重量，2token_id，3名称，4等级，5已战斗次数
            info = [avatar['quality'], avatar['weight'], avatar['identity']['id'], avatar['name'], avatar['level'], avatar['quota'][0]]
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
    avatars.sort(reverse=True)  # 排序，质量高的放前面
    items.sort(reverse=True)    # 排序，质量高的放前面
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
                    "id": str(avatars_battle[i][0])
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
                    "id": str(avatars_battle[i][0])
                },
                "items": []
            }
            data["team"].append(structured)
    battle_url = "https://app.starrynift.art/api-v2/game/battle/create"
    for i in range(times):
        try:
            res = requests.post(url=battle_url, data=json.dumps(data), headers=global_headers).json()
        except Exception as e:
            print(f"{STATUS_COLOR['FAIL']}[-] {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Create battle failed. Caused by {e}.{STATUS_COLOR['RESET']}")
        if "errorCode" in res.keys():
            if res["errorCode"] == 5005:    # 对战次数到了
                print(f"{STATUS_COLOR['WARNING']}[-] {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {res['message']} Team: {avatars_battle}{STATUS_COLOR['RESET']}")
                return
            elif res["errorCode"] == 5006:  # You need to wait at least 5 minutes to initiate a new battle.
                print(f"{STATUS_COLOR['FAIL']}[-] {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {res['message']}{STATUS_COLOR['RESET']}")
                time.sleep(310)
            else:
                print(f"{STATUS_COLOR['FAIL']}[-] {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {res}{STATUS_COLOR['RESET']}")
                exit()
        elif "statusCode" in res.keys():
            if res["statusCode"] == 429:    # ThrottlerException: Too Many Requests
                print(f"{STATUS_COLOR['FAIL']}[-] {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {res['message']}{STATUS_COLOR['RESET']}")
                time.sleep(310)
            else:
                print(f"{STATUS_COLOR['FAIL']}[-] {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {res}{STATUS_COLOR['RESET']}")
                exit()
        else:
            try:
                token_ids = []
                quality = []
                q = {
                    7: "SPR",
                    6: "UR",
                    5: "SSR",
                    4: "SR",
                    3: "R",
                    2: "N",
                    1: "L"
                }
                for avatar_meta in avatars_battle:
                    token_ids.append(avatar_meta[0])
                    quality.append(q[avatar_meta[1]])
                if res["evaluation"]["winner"] == res["side"]:
                    win += 1
                    print(f"{STATUS_COLOR['OK']}[+] {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Battle Win  | Odds:{str(round(win/(win+lose), 3)*100)[:4]:4}% Team: {token_ids} Rare: {quality}{STATUS_COLOR['RESET']}")
                else:
                    lose += 1
                    print(f"{STATUS_COLOR['FAIL']}[-] {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Battle Lose | Odds:{str(round(win/(win+lose), 3)*100)[:4]:4}% Team: {token_ids} Rare: {quality}{STATUS_COLOR['RESET']}")
                time.sleep(7)
            except Exception as e:
                print(res, e)
                exit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='StarryNift Auto Battle.')
    parser.add_argument('-u', '--user', default='account_1', help='current user for bot')
    parser.add_argument('-w', '--wear', default='1', help='wear items or not')
    parser.add_argument('-n', '--number', default=4, help='battle avater amount')
    parser.add_argument('-t', '--top', default=1, help='how many high quality nft battle once time')
    args = parser.parse_args()
    current_user = args.user
    is_wear = args.wear
    top = int(args.top)
    try:
        address = ACCOUNTS[current_user]['address']
        private_key = ACCOUNTS[current_user]['private_key']
    except Exception as e:
        print(f"User input or config error. Caused by: {e}")
        exit()
    banner = pyfiglet.Figlet(font='larry3d', width=160)
    print(banner.renderText('StarryNift'))
    print(banner.renderText('Auto Battle'))
    print(f"{STATUS_COLOR['INFO']}[+] {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Battle Address: {address}.{STATUS_COLOR['RESET']}")
    auth = do_sign(address, private_key)    # 获取签名token
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

    # 出战人数
    battle_count = int(args.number)

    team_serial = 0
    num = 0
    while True:
        avatars, items = battle_prepare()
        print(
            f"{STATUS_COLOR['OK']}[+] {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Get Equipment Success.{STATUS_COLOR['RESET']}")
        battle_teams = []
        min_times = float("inf")  # 无穷大
        while True:
            try:
                if num < top:
                    avatar = avatars.pop(0)
                    if avatar[5] < 5:
                        battle_teams.append([avatar[2], avatar[0]])
                        if 5-avatar[5] < min_times:
                            min_times = 5-avatar[5]
                        num += 1
                else:
                    avatar = avatars.pop(-1)
                    if avatar[5] < 5:
                        battle_teams.append([avatar[2], avatar[0]])
                        if 5-avatar[5] < min_times:
                            min_times = 5-avatar[5]
                        num += 1
            except IndexError:
                print(f"{STATUS_COLOR['WARNING']}[-] {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} No nft remains.{STATUS_COLOR['RESET']}")
                num = 0
                break
            if len(battle_teams) == battle_count:
                num = 0
                break
        if battle_teams:
            team_serial += 1
            print(f"\n{STATUS_COLOR['OK']}[+] {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Team serial: {team_serial}{STATUS_COLOR['RESET']}")
            battle_create(battle_teams, items, min_times)
        if not len(avatars):
            if win+lose > 0:
                msg = f"StarryNift Auto Battle\n" \
                      f"地址：{address}\n" \
                      f"数据：Win: {win}  Lose: {lose}  Rate:{round(win/(win+lose), 3)*100}%"
                print(msg)
            break
        print(f"{STATUS_COLOR['INFO']}[-] {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} One team battle done. Have a rest for 10 seconds.{STATUS_COLOR['RESET']}")
        time.sleep(12)
