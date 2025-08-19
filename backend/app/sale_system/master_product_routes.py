import os
import time
from flask import request, jsonify, current_app
from sqlalchemy.exc import IntegrityError
from werkzeug.utils import secure_filename
from . import sale_bp
from .. import db
from ..models import MasterProduct
from PIL import Image
# --- 配置 ---
# 定义允许上传的文件扩展名
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    """检查文件名是否具有允许的扩展名"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# --- 全局主商品管理 API ---
def process_and_save_image(file_stream):
    """
    一个辅助函数，用于处理图片：压缩、转换为 WebP 并保存。
    返回新文件的 URL 路径。
    """
    try:
        # 使用 Pillow 打开图片流
        img = Image.open(file_stream)
        
        # 为了安全，移除可能有害的 EXIF 数据并转换为 RGB
        img = img.convert("RGB")

        # 生成基于时间戳的唯一文件名，后缀直接定为 .webp
        timestamp = int(time.time() * 1000)
        output_filename = f"{timestamp}.webp"
        save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], output_filename)

        # 保存为 WebP 格式，quality 是压缩质量（1-100），60 是一个很好的平衡点
        img.save(save_path, 'webp', quality=60)
        
        return f"/uploads/{output_filename}"

    except Exception as e:
        print(f"Image processing error: {e}")
        return None

# 1. 修改 GET /master-products：默认只返回活跃商品，但提供一个参数可查看所有
@sale_bp.route('/api/master-products', methods=['GET'])
def get_master_products():
    show_all = request.args.get('all', 'false').lower() == 'true'
    query = MasterProduct.query
    if not show_all:
        query = query.filter_by(is_active=True)
    products = query.order_by(MasterProduct.product_code).all()
    return jsonify([p.to_dict() for p in products])

# 2. 【核心改动】删除 delete_master_product 函数，替换为以下函数
@sale_bp.route('/api/master-products/<int:mp_id>/status', methods=['PUT'])
def update_master_product_status(mp_id):
    mp = MasterProduct.query.get_or_404(mp_id)
    data = request.get_json()
    
    if 'is_active' not in data or not isinstance(data['is_active'], bool):
        return jsonify(error="Invalid request: 'is_active' (boolean) is required."), 400
        
    mp.is_active = data['is_active']
    db.session.commit()
    return jsonify(mp.to_dict()), 200

# API: 创建一个新的主商品 (支持文件上传)
@sale_bp.route('/api/master-products', methods=['POST'])
def create_master_product():
    """创建一个新的主商品"""
    # 检查请求中是否包含 form 数据
    if 'product_code' not in request.form:
        print("Request is not multipart/form-data or missing fields.")
        return jsonify(error="Request is not multipart/form-data or missing fields."), 400

    data = request.form
    required = ['product_code', 'name', 'default_price']
    if not all(field in data for field in required):
        print(f"Missing required fields: {', '.join(required)}")
        return jsonify(error=f"Missing required fields: {', '.join(required)}"), 400

    image_url = None
    # 检查是否有文件部分 'image'
    if 'image' in request.files:
        file = request.files['image']
        if file and file.filename != '' and allowed_file(file.filename):
            # 【核心改动】使用新的图片处理函数
            image_url = process_and_save_image(file.stream)
            if not image_url:
                return jsonify(error="Image processing failed."), 500

    try:
        new_mp = MasterProduct(
            product_code=data['product_code'],
            name=data['name'],
            default_price=float(data['default_price']),
            image_url=image_url
        )
        db.session.add(new_mp)
        db.session.commit()
        return jsonify(new_mp.to_dict()), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify(error=f"Product code '{data['product_code']}' already exists."), 409
    except (ValueError, TypeError):
        return jsonify(error="Invalid data type for price."), 400
    except Exception as e:
        db.session.rollback()
        return jsonify(error=str(e)), 500


# API: 更新一个主商品 (支持文件上传)
@sale_bp.route('/api/master-products/<int:mp_id>', methods=['PUT'])
def update_master_product(mp_id):
    """更新一个已存在的主商品"""
    mp = MasterProduct.query.get_or_404(mp_id)
    data = request.form

    # 检查是否有新图片上传
    if 'image' in request.files:
        file = request.files['image']
        if file and file.filename != '' and allowed_file(file.filename):
            # 删除旧图片以节省空间
            if mp.image_url:
                # 从 URL 路径中提取文件名
                old_filename = os.path.basename(mp.image_url)
                old_image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], old_filename)
                if os.path.exists(old_image_path):
                    try:
                        os.remove(old_image_path)
                    except OSError as e:
                        print(f"Error deleting file {old_image_path}: {e}")
            # 【核心改動】使用新的图片处理函数保存新图片
            mp.image_url = process_and_save_image(file.stream)
            if not mp.image_url:
                return jsonify(error="Image processing failed."), 500
            

    try:
        # 更新文本字段
        if 'product_code' in data: mp.product_code = data['product_code']
        if 'name' in data: mp.name = data['name']
        if 'default_price' in data: mp.default_price = float(data['default_price'])
        
        db.session.commit()
        return jsonify(mp.to_dict()), 200
    except IntegrityError:
        db.session.rollback()
        return jsonify(error=f"Product code '{data.get('product_code')}' already exists."), 409
    except (ValueError, TypeError):
        return jsonify(error="Invalid data type for price."), 400
    except Exception as e:
        db.session.rollback()
        return jsonify(error=str(e)), 500


