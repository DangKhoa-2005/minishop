"""
Order Routes
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Order, OrderItem, Cart, User

orders_bp = Blueprint('orders', __name__)


def admin_required(fn):
    """Decorator to require admin role"""
    from functools import wraps
    
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        if not user or not user.is_admin():
            return jsonify({
                'success': False,
                'message': 'Bạn không có quyền thực hiện hành động này'
            }), 403
        return fn(*args, **kwargs)
    return wrapper


@orders_bp.route('', methods=['GET'])
@jwt_required()
def get_orders():
    """Get current user's orders"""
    user_id = int(get_jwt_identity())
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    status = request.args.get('status')
    
    query = Order.query.filter_by(user_id=user_id)
    
    if status:
        query = query.filter_by(status=status)
    
    query = query.order_by(Order.created_at.desc())
    
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'success': True,
        'data': {
            'orders': [o.to_dict() for o in pagination.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': pagination.total,
                'pages': pagination.pages
            }
        }
    }), 200


@orders_bp.route('/<int:order_id>', methods=['GET'])
@jwt_required()
def get_order(order_id):
    """Get single order by ID"""
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    
    order = Order.query.get(order_id)
    
    if not order:
        return jsonify({
            'success': False,
            'message': 'Đơn hàng không tồn tại'
        }), 404
    
    # Check if user owns the order or is admin
    if order.user_id != user_id and not user.is_admin():
        return jsonify({
            'success': False,
            'message': 'Bạn không có quyền xem đơn hàng này'
        }), 403
    
    return jsonify({
        'success': True,
        'data': order.to_dict()
    }), 200


@orders_bp.route('/checkout', methods=['POST'])
@jwt_required()
def checkout():
    """
    Create order from cart (Checkout)
    ---
    Request Body:
        - shipping_address: string (required)
        - phone: string (required)
        - note: string (optional)
        - payment_method: string (optional, default: cod)
    """
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    # Prevent admins from performing a regular checkout as a customer
    if user and user.is_admin():
        return jsonify({
            'success': False,
            'message': 'Bạn không có quyền thực hiện hành động này (admin không thể checkout)'
        }), 403
    data = request.get_json() or {}
    
    shipping_address = data.get('shipping_address')
    phone = data.get('phone')
    note = data.get('note')
    payment_method = data.get('payment_method', Order.PAYMENT_METHOD_COD)
    name = data.get('name')  # optional customer name (useful for guest orders or explicit name)

    if isinstance(payment_method, str):
        payment_method = payment_method.strip().lower()

    if payment_method not in Order.VALID_PAYMENT_METHODS:
        return jsonify({
            'success': False,
            'message': 'Phương thức thanh toán không hợp lệ'
        }), 400

    # Require a name for the order: either provided explicitly or available on the user profile
    if not (name or (user and user.full_name)):
        return jsonify({
            'success': False,
            'message': 'Tên người nhận là bắt buộc'
        }), 400

    # Determine final customer name: prefer explicit name from payload, otherwise fall back to user's full name
    customer_name = name.strip() if isinstance(name, str) and name.strip() else (user.full_name if user and user.full_name else None)
    
    if not shipping_address:
        return jsonify({
            'success': False,
            'message': 'Địa chỉ giao hàng là bắt buộc'
        }), 400
    
    if not phone:
        return jsonify({
            'success': False,
            'message': 'Số điện thoại là bắt buộc'
        }), 400
    
    # Get user's cart
    cart = Cart.query.filter_by(user_id=user_id).first()
    
    if not cart or cart.items.count() == 0:
        return jsonify({
            'success': False,
            'message': 'Giỏ hàng trống'
        }), 400
    
    # Validate stock for all items
    for cart_item in cart.items:
        if not cart_item.product:
            return jsonify({
                'success': False,
                'message': 'Có sản phẩm không còn tồn tại'
            }), 400
        
        if not cart_item.product.is_in_stock(cart_item.quantity):
            return jsonify({
                'success': False,
                'message': f'Sản phẩm "{cart_item.product.name}" chỉ còn {cart_item.product.stock} trong kho'
            }), 400
    
    try:
        # Create order
        status = Order.STATUS_CONFIRMED

        # Calculate per-user order number
        max_num = db.session.query(db.func.max(Order.user_order_number)).filter_by(user_id=user_id).scalar()
        user_order_number = (max_num or 0) + 1

        order = Order(
            user_id=user_id,
            user_order_number=user_order_number,
            customer_name=customer_name,
            total_amount=cart.get_total(),
            shipping_address=shipping_address,
            phone=phone,
            payment_method=payment_method,
            note=note,
            status=status
        )
        db.session.add(order)
        db.session.flush()

        if status == Order.STATUS_CONFIRMED:
            try:
                print(f"[orders] AUTO_CONFIRM enabled: created order id={order.id} user_id={user_id} status=confirmed")
            except Exception:
                # Safe print fallback
                print("[orders] AUTO_CONFIRM enabled: created order (print encoding error)")
        
        # Create order items and reduce stock
        for cart_item in cart.items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=cart_item.product_id,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )
            db.session.add(order_item)
            
            # Reduce stock
            cart_item.product.reduce_stock(cart_item.quantity)
        
        # Clear cart
        cart.clear()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Đặt hàng thành công',
            'data': order.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Lỗi: {str(e)}'
        }), 500


@orders_bp.route('/<int:order_id>/cancel', methods=['POST'])
@jwt_required()
def cancel_order(order_id):
    """Cancel an order"""
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)

    order = Order.query.get(order_id)

    if not order:
        return jsonify({
            'success': False,
            'message': 'Đơn hàng không tồn tại'
        }), 404

    if order.user_id != user_id and not user.is_admin():
        return jsonify({
            'success': False,
            'message': 'Bạn không có quyền hủy đơn hàng này'
        }), 403
    
    if not order.can_cancel():
        return jsonify({
            'success': False,
            'message': f'Không thể hủy đơn hàng ở trạng thái "{order.get_status_display()}"'
        }), 400
    
    try:
        # Restore stock
        for item in order.items:
            if item.product:
                item.product.stock += item.quantity
        
        order.status = Order.STATUS_CANCELLED
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Đã hủy đơn hàng',
            'data': order.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Lỗi: {str(e)}'
        }), 500


@orders_bp.route('/<int:order_id>/confirm-delivery', methods=['POST'])
@jwt_required()
def confirm_delivery(order_id):
    """Allow customer to confirm delivery when order is in shipping state"""
    user_id = int(get_jwt_identity())
    order = Order.query.get(order_id)

    if not order:
        return jsonify({
            'success': False,
            'message': 'Đơn hàng không tồn tại'
        }), 404

    if order.user_id != user_id:
        return jsonify({
            'success': False,
            'message': 'Bạn không có quyền thực hiện hành động này'
        }), 403

    if order.status != Order.STATUS_SHIPPING:
        return jsonify({
            'success': False,
            'message': 'Chỉ có thể xác nhận khi đơn đang ở trạng thái "Đang giao"'
        }), 400

    try:
        order.status = Order.STATUS_DELIVERED
        db.session.commit()
        return jsonify({
            'success': True,
            'message': 'Xác nhận đã nhận hàng thành công',
            'data': order.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Lỗi: {str(e)}'
        }), 500


# Admin routes

@orders_bp.route('/admin/all', methods=['GET'])
@admin_required
def admin_get_all_orders():
    """Get all orders (Admin only)"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    status = request.args.get('status')
    
    query = Order.query
    
    if status:
        # Support comma-separated statuses (e.g. 'shipping,delivered')
        status_list = [s.strip() for s in status.split(',') if s.strip()]
        if len(status_list) == 1:
            query = query.filter_by(status=status_list[0])
        else:
            query = query.filter(Order.status.in_(status_list))
    
    query = query.order_by(Order.created_at.desc())
    
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'success': True,
        'data': {
            'orders': [o.to_dict() for o in pagination.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': pagination.total,
                'pages': pagination.pages
            }
        }
    }), 200


@orders_bp.route('/admin/<int:order_id>/status', methods=['PUT'])
@admin_required
def admin_update_order_status(order_id):
    """
    Update order status (Admin only)
    ---
    Request Body:
        - status: string (required) - confirmed, shipping, delivered, cancelled
    """
    data = request.get_json()
    new_status = data.get('status')
    
    if new_status not in Order.VALID_STATUSES:
        return jsonify({
            'success': False,
            'message': f'Trạng thái không hợp lệ. Cho phép: {", ".join(Order.VALID_STATUSES)}'
        }), 400
    
    order = Order.query.get(order_id)
    
    if not order:
        return jsonify({
            'success': False,
            'message': 'Đơn hàng không tồn tại'
        }), 404
    
    try:
        # If cancelling, restore stock
        if new_status == Order.STATUS_CANCELLED and order.status != Order.STATUS_CANCELLED:
            for item in order.items:
                if item.product:
                    item.product.stock += item.quantity
        
        order.status = new_status
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Đã cập nhật trạng thái thành "{order.get_status_display()}"',
            'data': order.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Lỗi: {str(e)}'
        }), 500


@orders_bp.route('/admin/stats', methods=['GET'])
@admin_required
def admin_get_order_stats():
    """Get order statistics (Admin only)"""
    from sqlalchemy import func
    
    # Total orders by status
    status_counts = db.session.query(
        Order.status,
        func.count(Order.id)
    ).group_by(Order.status).all()
    
    # Total revenue (delivered orders)
    total_revenue = db.session.query(
        func.sum(Order.total_amount)
    ).filter(Order.status == Order.STATUS_DELIVERED).scalar() or 0
    
    # Total orders
    total_orders = Order.query.count()
    
    return jsonify({
        'success': True,
        'data': {
            'total_orders': total_orders,
            'total_revenue': float(total_revenue),
            'by_status': {status: count for status, count in status_counts}
        }
    }), 200
