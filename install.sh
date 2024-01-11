#!/bin/bash

# 安装依赖模块
pip3 install -r requirements.txt

# 安装并启动supervisor
apt-get install -y supervisor
supervisord -c /etc/supervisor/supervisord.conf

# 创建 Supervisor 配置文件
if [ ! -d "/etc/supervisor/conf.d" ]; then
    sudo mkdir -p /etc/supervisor/conf.d
fi
cat <<EOF > /etc/supervisor/conf.d/serverBot.conf
[program:serverBot]
command=/usr/bin/python3 $(pwd)/serverBot.py
autostart=true
autorestart=true
stderr_logfile=/var/log/serverBot.err.log
stdout_logfile=/var/log/serverBot.out.log
EOF

# 重新加载 Supervisor 配置并更新
sudo supervisorctl reread
sudo supervisorctl update