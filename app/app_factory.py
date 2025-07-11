from flask import Flask
from config import Config

def create_app(config_class=Config):
    """应用工厂函数"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # 注册蓝图
    from views import api, web
    app.register_blueprint(api.bp)
    app.register_blueprint(web.bp)
    
    return app 