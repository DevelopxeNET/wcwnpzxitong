import os

class Config:
    """基础配置"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here-change-in-production'
    
    # 数据库配置
    DB_HOST = os.environ.get('DB_HOST', '192.168.1.88')
    DB_PORT = int(os.environ.get('DB_PORT', 3306))
    DB_USER = os.environ.get('DB_USER', 'wcwnpz')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'm5fApGzkabe4zNFY')
    DB_NAME = os.environ.get('DB_NAME', 'wcwnpz')
    DB_CHARSET = 'utf8mb4'

class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    TESTING = False

# 配置字典
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
