# StarryNift Auto Battle


StarryNift 自动对战刷经验辅助工具，解放你的时间。
>@author: 19 From STARS GUILD 繁星公会

>Ps: StarryNift元宇宙游戏仍处于相当早期阶段，多点耐心。

>**购买自动占地脚本，联系wx: kylin_turing**

#### 需要注意的事情
1. 不要开全局代理/系统VPN，会报错闪退。
2. 假如你出战的人数为N，需要你的装备整体套数至少能凑出来N套，否则请通过参数取消使用装备，比如你只有2个法器，但是选择了3个人出战并且需要穿装备，则会报错，**我不是很想改这个逻辑**，请手动改出战人数或者不使用装备。
3. 假如你选择了出战人数为N，这一轮对战的实际可用的nft小于N，同样会执行，只不过是以实际数量来进行的。
4. 运行脚本的时候，不需要开浏览器，也不需要访问starrynift官网，运行就完事了。
5. 至于安全性问题，没必要解释，这个脚本很简单，不收钱，开源，安全问题自己看代码。


## Mac / Linux
#### 文档结构
```
$ tree starrynift-pub
starrynift-pub
├── LICENSE
├── README.md
├── auto_battle.py
├── config.py
└── starry_util.py
```

需要 Python 3.6 以上，并pip安装相关依赖包，现阶段可能需要的有：
```
pyfiglet, web3, requests
```
#### 配置钱包
编辑`config.py`
```
# 这里添加账户
ACCOUNTS = {
    "account_1": {
        "address": "",
        "private_key": ""
    },
}
```
在`address`和`private_key`后面写自己的钱包地址和私钥，并可以改`account_1`这个账户名，执行的时候可以通过命令行参数指定参与对战的账户。如果有多个地址，在后面增加，如：
```
ACCOUNTS = {
    "account_1": {
        "address": "",
        "private_key": ""
    },
    "account_2": {
        "address": "",
        "private_key": ""
    },
    "account_3": {
        "address": "",
        "private_key": ""
    },
}
```
#### 使用auto battle
目前脚本支持的参数：

- -u 或 --user
    - 参与对战的账户名，是在config里面配置的名字，默认不输入的话为 account_1
- -w 或 --wear
    - 是否穿戴装备，有的人是迷信不穿装备胜率更高的，默认穿戴，输入值为 0 的话则不穿装备
- -n 或 --number
    - 出战人数，1-4人都可以，默认为2，因为我觉得2个出战胜率更高一点，但是整体时间会被拉长，不过脚本执行时间不是问题。

命令执行参考：
```
# Kylin账户对战，出战人数4，不穿装备
python3 auto_battle.py -u Kylin -n 4 -w 0

# Kylin账户对战，出战人数3，默认穿装备
python3 auto_battle.py -u Kylin -n 3

# 默认账户account_1对战，出战人数4，默认穿装备
python3 auto_battle.py -n 4
```
> 如果你要持续循环对战，类似windows版本的第三个参数，使用`crontab`做定时任务就可以了。
![image](https://user-images.githubusercontent.com/5326766/149612989-688abc78-afa2-442c-bd2b-09135b7eab27.png)


## Windows10 / 11（Windows7不支持）
> exe 根据 auto_battle_for_windows.py 用 pyinstaller 打包的，同样开源。
如果你在windows下会用脚本，那可以直接跑py文件，不用exe。

使用编译打包好的 exe程序，看这里下载 https://github.com/cnssr4bb1t/starrynift-pub/releases
下载zip压缩包。
#### 配置钱包
在`auto_battle.exe`程序相同目录下创建`account.txt` (现在压缩包里面自带了一个account.txt，直接改就行了)，里面内容为：
```
地址----私钥
```
比如
```
0xE7Ef07FC17C6a71AB1a59d2f3eB3B332053CBfCA----0xbalabalabalabalabalabalabalabalabalabalabalabala
```
如果有多个账号，可以写多行，程序执行的时候会按照顺序去尝试对战。
然后双击 `auto_battle.exe` 运行，简单输入参数之后，就可以去做别的事情了：）
![image](https://user-images.githubusercontent.com/5326766/149615304-2b91e4a1-2b21-42a4-935a-33ad1bf23ae2.png)

#### 常见问题
> 出现解决不了的闪退问题的话，拍视频，找到闪退报错的那一帧，截图微信发给我看看。

1. 如果出现`Caused by HTTPSConnectionPool(host='app.starrynift.art', port=443): Max retries exceeded with url: /api/user/challenge (Caused by SSLError(SSLEOFError(8, 'EOF occurred in violation of protocol (_ssl.c:997)'))).` 这种错误提示，大概率是网络问题，检查一下你是不是开了全局代理，关掉它。
2. 可能导致闪退的问题：`account.txt`文件内容没有写对
