from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from config import Config
import os

# 在全局作用域创建扩展实例
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    # 创建 Flask app 实例
    app = Flask(__name__, static_folder=config_class.STATIC_FOLDER)
    app.config.from_object(config_class)

    # 创建上传目录
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    
    # 创建子目录
    for subdir in ['products', 'qrcodes', 'events', 'temp']:
        subdir_path = os.path.join(app.config['UPLOAD_FOLDER'], subdir)
        if not os.path.exists(subdir_path):
            os.makedirs(subdir_path)

    # 静态文件路由
    @app.route('/static/<path:filename>')
    def static_files(filename):
        return send_from_directory(app.config['STATIC_FOLDER'], filename)
    
    @app.route('/uploads/<path:filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    # 初始化扩展
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    # 注册蓝图
    from .sale_system import sale_bp
    app.register_blueprint(sale_bp, url_prefix='/sale')
    
    return app

# 模型导入放在文件末尾
from . import models