import os

# 获取项目根目录的路径
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # 设置一个密钥，用于保护 session 和其他安全相关的事务
    UPLOAD_FOLDER = os.path.join(basedir, 'static', 'uploads')
    STATIC_FOLDER = os.path.join(basedir, 'static')
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a-hard-to-guess-string'

    ADMIN_PASSWORD=os.environ.get('ADMIN_PASSWORD') or '1919810'
    VENDOR_PASSWORD=os.environ.get('VENDOR_PASSWORD') or '114514'

    # 数据库配置
    # 设置 SQLAlchemy 数据库的 URI
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    
    # 关闭 SQLAlchemy 的事件通知系统，以节省资源
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 文件上传配置
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))   # 16MB 最大文件大小
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}