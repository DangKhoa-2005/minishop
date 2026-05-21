"""
Cart Routes
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Cart, CartItem, Product

cart_bp = Blueprint('cart', __name__)


@cart_bp.route('', methods=['GET'])
@jwt_required()
def get_cart():
    """Get current user's cart"""
    user_id = int(get_jwt_identity())
    
    cart = Cart.query.filter_by(user_id=user_id).first()
    
    if not cart:
        # Create empty cart if not exists
        cart = Cart(user_id=user_id)
        db.session.add(cart)
        db.session.commit()
    
    return jsonify({
        'success': True,
        'data': cart.to_dict()
    }), 200


@cart_bp.route('/add', methods=['POST'])
@jwt_required()
def add_to_cart():
    """
    Add product to cart
    ---
    Request Body:
        - product_id: int (required)
        - quantity: int (optional, default: 1)
    """
    user_id = int(get_jwt_identity())
    data = request.get_json()
    
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)
    
    if not product_id:
        return jsonify({
            'success': False,
            'message': 'product_id là bắt buộc'
        }), 400
    
    if quantity < 1:
        return jsonify({
            'success': False,
            'message': 'Số lượng phải lớn hơn 0'
        }), 400
    
    # Check product exists and in stock
    product = Product.query.get(product_id)
    if not product:
        return jsonify({
            'success': False,
            'message': 'Sản phẩm không tồn tại'
        }), 404
    
    if not product.is_in_stock(quantity):
        return jsonify({
            'success': False,
            'message': f'Sản phẩm chỉ còn {product.stock} trong kho'
        }), 400
    
    # Get or create cart
    cart = Cart.query.filter_by(user_id=user_id).first()
    if not cart:
        cart = Cart(user_id=user_id)
        db.session.add(cart)
        db.session.flush()
    
    # Check if product already in cart
    cart_item = CartItem.query.filter_by(
        cart_id=cart.id,
        product_id=product_id
    ).first()
    
    if cart_item:
        # Update quantity
        new_quantity = cart_item.quantity + quantity
        if not product.is_in_stock(new_quantity):
            return jsonify({
                'success': False,
                'message': f'Không đủ hàng. Tối đa có thể thêm {product.stock - cart_item.quantity}'
            }), 400
        cart_item.quantity = new_quantity
    else:
        # Add new item
        cart_item = CartItem(
            cart_id=cart.id,
            product_id=product_id,
            quantity=quantity
        )
        db.session.add(cart_item)
    
    try:
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Đã thêm vào giỏ hàng',
            'data': cart.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Lỗi: {str(e)}'
        }), 500


@cart_bp.route('/update/<int:item_id>', methods=['PUT'])
@jwt_required()
def update_cart_item(item_id):
    """
    Update cart item quantity
    ---
    Request Body:
        - quantity: int (required)
    """
    user_id = int(get_jwt_identity())
    data = request.get_json()
    
    quantity = data.get('quantity')
    
    if quantity is None or quantity < 1:
        return jsonify({
            'success': False,
            'message': 'Số lượng phải lớn hơn 0'
        }), 400
    
    # Get cart and verify ownership
    cart = Cart.query.filter_by(user_id=user_id).first()
    if not cart:
        return jsonify({
            'success': False,
            'message': 'Giỏ hàng không tồn tại'
        }), 404
    
    # Get cart item
    cart_item = CartItem.query.filter_by(
        id=item_id,
        cart_id=cart.id
    ).first()
    
    if not cart_item:
        return jsonify({
            'success': False,
            'message': 'Sản phẩm không có trong giỏ hàng'
        }), 404
    
    # Check stock
    if not cart_item.product.is_in_stock(quantity):
        return jsonify({
            'success': False,
            'message': f'Sản phẩm chỉ còn {cart_item.product.stock} trong kho'
        }), 400
    
    cart_item.quantity = quantity
    
    try:
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Đã cập nhật giỏ hàng',
            'data': cart.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Lỗi: {str(e)}'
        }), 500


@cart_bp.route('/remove/<int:item_id>', methods=['DELETE'])
@jwt_required()
def remove_from_cart(item_id):
    """Remove item from cart"""
    user_id = int(get_jwt_identity())
    
    # Get cart and verify ownership
    cart = Cart.query.filter_by(user_id=user_id).first()
    if not cart:
        return jsonify({
            'success': False,
            'message': 'Giỏ hàng không tồn tại'
        }), 404
    
    # Get cart item
    cart_item = CartItem.query.filter_by(
        id=item_id,
        cart_id=cart.id
    ).first()
    
    if not cart_item:
        return jsonify({
            'success': False,
            'message': 'Sản phẩm không có trong giỏ hàng'
        }), 404
    
    try:
        db.session.delete(cart_item)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Đã xóa khỏi giỏ hàng',
            'data': cart.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Lỗi: {str(e)}'
        }), 500


@cart_bp.route('/clear', methods=['DELETE'])
@jwt_required()
def clear_cart():
    """Clear all items from cart"""
    user_id = int(get_jwt_identity())
    
    cart = Cart.query.filter_by(user_id=user_id).first()
    if not cart:
        return jsonify({
            'success': False,
            'message': 'Giỏ hàng không tồn tại'
        }), 404
    
    try:
        cart.clear()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Đã xóa toàn bộ giỏ hàng',
            'data': cart.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Lỗi: {str(e)}'
        }), 500
