#!/bin/bash

# echo "openid = ${APP_OPENID}"
# 安装必须组件
# pip install -r /docker/requirements.txt

# apt update
# apt install -y --no-install-recommends cron

# apt install -y rsyslog
# service rsyslog start

# rm -rf /var/lib/apt/lists/*
# apt clean

chown root:root /etc/cron.d/crontab
chmod 0644 /etc/cron.d/crontab
# touch /var/log/cron.log

# 运行API入口脚本
python /home/app/main.py
# env >> /etc/default/locale
cron && tail -f /var/log/cron.log