from flask import request, jsonify
from . import sale_bp
from .. import db
from ..models import Order, OrderItem, Product, Event

VALID_ORDER_STATUSES = ['pending', 'completed', 'cancelled']
from ..models import Order, OrderItem, Product, Event

# --- 订单处理 API ---

# API: 获取指定展会的订单列表
# 路径: GET /sale/api/events/<int:event_id>/orders?status=pending
@sale_bp.route('/api/events/<int:event_id>/orders', methods=['GET'])
def get_orders_for_event(event_id):
    Event.query.get_or_404(event_id)
    status_filter = request.args.get('status')
    query = Order.query.filter_by(event_id=event_id)
    if status_filter in VALID_ORDER_STATUSES:
        query = query.filter_by(status=status_filter)
    orders = query.order_by(Order.timestamp.desc()).all()
    return jsonify([o.to_dict() for o in orders])

# API: 更新订单状态 (摊主操作)
# 【核心改动】API: 更新指定展会下的特定订单状态
@sale_bp.route('/api/events/<int:event_id>/orders/<int:order_id>/status', methods=['PUT'])
def update_order_status_for_event(event_id, order_id):
    data = request.get_json()
    new_status = data.get('status')

    if not new_status or new_status not in VALID_ORDER_STATUSES:
        return jsonify(error=f"Invalid status."), 400

    # 查询订单时，确保它同时匹配 order_id 和 event_id
    order = Order.query.filter_by(id=order_id, event_id=event_id).first_or_404()
    
    order.status = new_status
    db.session.commit()
    
    return jsonify(order.to_dict())
# 【新增】API: 顾客创建新订单 (替代 WebSocket)
@sale_bp.route('/api/events/<int:event_id>/orders', methods=['POST'])
def create_order(event_id):
    data = request.get_json()
    items = data.get('items')

    if not isinstance(items, list) or not items:
        return jsonify(error="Invalid order data: Missing or empty items."), 400

    try:
        # 后端的库存验证和订单创建逻辑，与之前 events.py 中的几乎完全一样
        total_amount = 0
        for item in items:
            product = Product.query.get(item.get('product_id'))
            if not product or product.event_id != event_id or item.get('quantity') > product.current_stock:
                return jsonify(error=f"Product '{product.master_product.name if product else ''}' is invalid or out of stock."), 400
            total_amount += product.price * item.get('quantity')

        new_order = Order(event_id=event_id, total_amount=round(total_amount, 2), status='pending')
        db.session.add(new_order)
        db.session.flush()

        for item in items:
            db.session.add(OrderItem(order_id=new_order.id, **item))
        
        db.session.commit()
        return jsonify(new_order.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        print(f"Order creation error: {e}")
        return jsonify(error="An internal server error occurred."), 500