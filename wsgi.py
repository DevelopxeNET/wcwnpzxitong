"""
WSGI入口文件 - 用于生产环境部署
"""
import os
from app import app

# 设置生产环境
os.environ['FLASK_ENV'] = 'production'

if __name__ == "__main__":
    app.run()
