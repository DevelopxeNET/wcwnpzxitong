#!/bin/bash

# 启动脚本

# 创建日志目录
mkdir -p logs

# 设置环境变量
export FLASK_ENV=production

# 启动 Gunicorn
gunicorn -c gunicorn_config.py wsgi:app

echo "服务已启动,访问地址: http://0.0.0.0:5000"
