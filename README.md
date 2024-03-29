# serverBot

使用钉钉机器人通过idrac监控服务器的状态，实现以下功能：

1. 通过钉钉信息查询服务器状态
2. 通过钉钉信息开关机
3. 设置温度与功耗的限制，超出限制自动钉钉提醒

> 注：项目仅在idrac8上进行验证。

# 安装

```shell
chmod +x ./install.sh
sudo ./install.sh
```

# 启动

需要自行准备好钉钉机器人的client_id、client_secret、webhook，需要在idrac上为钉钉机器人添加具有上述操作权限的专用账号。然后配置conf/conf.ini，例如：

```ini
[dingtalk]
client_id = xxx
client_secret = xxx
webhook = https://xxx
at_user_phone = 13211111111

[idrac]
host = 192.168.1.11
user = serverBot
password = serverBotPassword

[threshold]
temperature_limit = 80
power_limit = 600
```

然后执行serverBot：

```shell
nohup python3 serverBot.py &
```

# 使用

@钉钉机器人，发送下面的指令通过钉钉机器人完成相应任务：

* help：查看指令
* status：查看serverBot的运行状态
* info: 查询服务器信息
* startup：打开服务器电源
* shutdown：关闭服务器电源

如`@钉钉机器人 info`查看服务器信息。

当服务器温度或功耗超出阈值时，钉钉机器人会自动发送提醒。