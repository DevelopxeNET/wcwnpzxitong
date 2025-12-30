@echo off
REM Windows 启动脚本

REM 创建日志目录
if not exist logs mkdir logs

REM 设置环境变量
set FLASK_ENV=production

REM 启动 Gunicorn
gunicorn -c gunicorn_config.py wsgi:app

echo 服务已启动,访问地址: http://0.0.0.0:5000
pause
