# serverBot

使用钉钉机器人通过idrac监控服务器的状态，实现以下功能：

1. 通过钉钉查询服务器状态
2. 通过钉钉开关机
3. 设置温度与功耗的限制，超出限制钉钉提醒

# 安装

```python
pip install -r requirements.txt
```

# 服务搭建

需要自行准备好钉钉机器人的client_id、client_secret、webhook，需要在dirac上为钉钉机器人添加具有上述操作权限的专用账号。执行下面的命令开启服务：

```python
python3 serverBot.py 
--host '<idrac地址>' 
--user '<idrac账户用户名>' 
--password '<idrac账户密码>' 
--client_id '<client_id>' 
--client_secret '<client_secret>' 
--webhook '<webhook>' 
--atUserPhone '<钉钉用户手机号，用于@>'
--temperatureLimit <温度限制>
--powerLimit <功耗限制>
```

使用示例：

```python
python3 serverBot.py 
--host '192.168.8.8' 
--user 'serverBot' 
--password 'serverBotPassword' 
--client_id '123456' 
--client_secret '123456' 
--webhook 'http://webhook' 
--atUserPhone '13211111111'
--temperatureLimit 80
--powerLimit 500
```

# 使用

@钉钉机器人，发送下面的指令通过钉钉机器人完成相应任务：

* help：查看指令
* status：查看serverBot的运行状态
* info: 查询服务器信息
* startup：打开服务器电源
* shutdown：关闭服务器电源

当服务器温度或功耗超出阈值时，钉钉机器人会自动发送提醒。