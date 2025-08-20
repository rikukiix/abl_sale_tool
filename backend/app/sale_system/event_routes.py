from flask import request, jsonify
from datetime import datetime
from . import sale_bp
from .. import db
from ..models import Event

VALID_STATUSES = ["未进行", "进行中", "已结束"]

# --- 展会管理 API ---

# API: 获取所有展会列表 (已升级，按数据库字段筛选)
# 路径: GET /sale/api/events?status=进行中
@sale_bp.route('/api/events', methods=['GET'])
def get_events():
    status_filter = request.args.get('status')
    query = Event.query

    if status_filter in VALID_STATUSES:
        # 直接根据数据库中的 status 字段进行过滤
        query = query.filter(Event.status == status_filter)

    events = query.order_by(Event.date.desc()).all()
    return jsonify([event.to_dict() for event in events]), 200

# API: 创建新展会
@sale_bp.route('/api/events', methods=['POST'])
def create_event():
    data = request.get_json()
    if not data or not 'name' in data or not 'date' in data:
        return jsonify(error="Missing required fields: name and date"), 400

    try:
        new_event = Event(
            name=data['name'],
            date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
            location=data.get('location', ''),
            vendor_password=data.get('vendor_password')
            # status 会自动使用模型中定义的默认值 '未进行'
        )
        db.session.add(new_event)
        db.session.commit()
        return jsonify(new_event.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify(error=str(e)), 500

# 【新增】 API: 更新指定展会的状态
# 路径: PUT /sale/api/events/<int:event_id>/status
@sale_bp.route('/api/events/<int:event_id>/status', methods=['PUT'])
def update_event_status(event_id):
    data = request.get_json()
    new_status = data.get('status')

    if not new_status or new_status not in VALID_STATUSES:
        return jsonify(error=f"Invalid or missing status. Must be one of: {', '.join(VALID_STATUSES)}"), 400

    event = Event.query.get_or_404(event_id)
    
    event.status = new_status
    db.session.commit()

    #加入调试用的输出
    print(f"更新展会 {event_id} 状态为 {new_status}")

    
    return jsonify(event.to_dict()), 200
@sale_bp.route('/api/events/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    event = Event.query.get_or_404(event_id)
    data = request.get_json()
    if not data:
        return jsonify(error="Request body cannot be empty"), 400
    
    try:
        if 'name' in data:
            event.name = data['name']
        if 'date' in data:
            event.date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        if 'location' in data:
            event.location = data['location']
        if 'vendor_password' in data:
            # 允许将密码设置为空字符串来清除它
            event.vendor_password = data['vendor_password']
        db.session.commit()
        return jsonify(event.to_dict()), 200
    except (ValueError, TypeError):
        return jsonify(error="Invalid data format."), 400
    except Exception as e:
        db.session.rollback()
        return jsonify(error=str(e)), 500