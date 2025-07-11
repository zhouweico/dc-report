import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """基础配置类"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    
    # 数据库配置
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_PORT = int(os.environ.get('DB_PORT', 5432))
    DB_NAME = os.environ.get('DB_NAME', 'dependencycheck')
    DB_USER = os.environ.get('DB_USER', 'dcuser')
    DB_PASS = os.environ.get('DB_PASS', 'dcpass')
    
    # Gunicorn 配置
    GUNICORN_WORKERS = int(os.environ.get('GUNICORN_WORKERS', 4))
    GUNICORN_WORKER_CLASS = os.environ.get('GUNICORN_WORKER_CLASS', 'gevent')
    GUNICORN_TIMEOUT = int(os.environ.get('GUNICORN_TIMEOUT', 300))
    GUNICORN_BIND = os.environ.get('GUNICORN_BIND', '0.0.0.0:5001')

class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True

class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False

class TestingConfig(Config):
    """测试环境配置"""
    TESTING = True
    DB_NAME = os.environ.get('TEST_DB_NAME', 'dependencycheck_test')

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
} 