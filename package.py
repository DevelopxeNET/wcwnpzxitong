#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
项目打包脚本
"""
import os
import shutil
import zipfile
from datetime import datetime

# 项目名称
PROJECT_NAME = "logistics_voucher_system"

# 需要打包的文件和目录
INCLUDE_FILES = [
    'app.py',
    'config.py',
    'wsgi.py',
    'gunicorn_config.py',
    'requirements.txt',
    'start.sh',
    'start.bat',
    '.env.example',
    '.gitignore',
    'DEPLOY.md',
    '宝塔部署说明.txt',  # 宝塔面板部署指南
    'templates/',
    'create_logistics_table.py',  # 建表脚本
    'fix_all_status.py'  # 状态修复脚本
]

# 排除的文件
EXCLUDE_PATTERNS = [
    '__pycache__',
    '*.pyc',
    '*.log',
    'logs/',
    '.env',
    'test_*.py',
    'check_*.py',
    'insert_*.py',
    'modify_*.py',
    'update_*.py',
    'API使用说明.txt'
]

def should_exclude(file_path):
    """判断文件是否应该排除"""
    for pattern in EXCLUDE_PATTERNS:
        if pattern in file_path:
            return True
    return False

def create_package():
    """创建部署包"""
    # 生成时间戳
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    package_name = f"{PROJECT_NAME}_{timestamp}.zip"
    
    print(f"开始打包项目...")
    print(f"包名: {package_name}")
    print("="*80)
    
    # 创建临时目录
    temp_dir = f"temp_{PROJECT_NAME}"
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)
    
    # 复制文件
    for item in INCLUDE_FILES:
        src = item
        dst = os.path.join(temp_dir, item)
        
        if os.path.isfile(src):
            # 复制文件
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)
            print(f"✓ 已添加: {item}")
        elif os.path.isdir(src):
            # 复制目录
            shutil.copytree(src, dst, ignore=shutil.ignore_patterns(*EXCLUDE_PATTERNS))
            print(f"✓ 已添加: {item} (目录)")
        else:
            print(f"✗ 跳过: {item} (不存在)")
    
    # 创建logs目录
    logs_dir = os.path.join(temp_dir, 'logs')
    os.makedirs(logs_dir, exist_ok=True)
    with open(os.path.join(logs_dir, '.gitkeep'), 'w') as f:
        f.write('')
    print(f"✓ 已创建: logs/ (目录)")
    
    # 创建zip文件
    print("\n正在压缩文件...")
    with zipfile.ZipFile(package_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, temp_dir)
                zipf.write(file_path, arcname)
    
    # 清理临时目录
    shutil.rmtree(temp_dir)
    
    # 显示结果
    file_size = os.path.getsize(package_name) / 1024 / 1024
    print("\n" + "="*80)
    print(f"✓ 打包完成!")
    print(f"文件名: {package_name}")
    print(f"大小: {file_size:.2f} MB")
    print(f"位置: {os.path.abspath(package_name)}")
    print("="*80)
    print("\n部署方式:")
    print("="*80)
    print("\n■ 宝塔面板部署 (推荐):")
    print("-"*80)
    print("1. 上传压缩包到服务器 /www/wwwroot/ 目录")
    print("2. 在宝塔面板中解压")
    print("3. 进入目录安装依赖: pip install -r requirements.txt")
    print("4. 配置环境: cp .env.example .env && vim .env")
    print("5. 初始化数据库: python create_logistics_table.py")
    print("6. 在宝塔【Python项目管理器】中添加项目")
    print("7. 配置Nginx反向代理")
    print("\n📚 详细部署步骤请查看: 宝塔部署说明.txt")
    print("\n■ 命令行部署:")
    print("-"*80)
    print("1. 将压缩包上传到服务器")
    print("2. 解压: unzip " + package_name)
    print("3. 进入目录: cd " + PROJECT_NAME)
    print("4. 查看部署文档: cat DEPLOY.md")
    print("5. 安装依赖: pip install -r requirements.txt")
    print("6. 配置环境: cp .env.example .env && vim .env")
    print("7. 初始化数据库: python create_logistics_table.py")
    print("8. 启动服务: ./start.sh")
    print("="*80)

if __name__ == '__main__':
    try:
        create_package()
    except Exception as e:
        print(f"\n✗ 打包失败: {e}")
        import traceback
        traceback.print_exc()
