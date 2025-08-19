# --- backend/app/__init__.py ---


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from flask_cors import CORS
from config import Config
import os
from flask import send_from_directory

# 1. 在全局作用域创建扩展实例
db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=Config):
    # 3. 创建 Flask app 实例
    app = Flask(__name__)
    app.config.from_object(config_class)

    # ... (静态文件和文件夹配置) ...
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    # 4. 在 app 上下文中初始化扩展
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    # 5. 【关键】在函数内部导入并注册蓝图
    #    这样做可以避免循环导入
    from .sale_system import sale_bp
    app.register_blueprint(sale_bp, url_prefix='/sale')
    
    # 6. 返回完全配置好的 app 实例
    return app

# 7. 模型导入放在文件末尾
from . import models