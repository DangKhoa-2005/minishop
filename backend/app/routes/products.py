"""
Product Routes
"""
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Product, Category, User

products_bp = Blueprint('products', __name__)


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


@products_bp.route('', methods=['GET'])
def get_products():
    """
    Get all products with pagination and filters
    ---
    Query Parameters:
        - page: int (default: 1)
        - per_page: int (default: 12)
        - category_id: int (optional)
        - search: string (optional)
        - min_price: float (optional)
        - max_price: float (optional)
        - sort_by: string (optional) - 'price_asc', 'price_desc', 'newest', 'name'
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', current_app.config.get('ITEMS_PER_PAGE', 12), type=int)
    category_id = request.args.get('category_id', type=int)
    search = request.args.get('search', '')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    sort_by = request.args.get('sort_by', 'newest')
    
    # Build query
    query = Product.query
    
    # Filter by category
    if category_id:
        query = query.filter(Product.category_id == category_id)
    
    # Search by name or description
    if search:
        search_term = f'%{search}%'
        query = query.filter(
            db.or_(
                Product.name.ilike(search_term),
                Product.description.ilike(search_term)
            )
        )
    
    # Filter by price range
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)
    
    # Sort
    if sort_by == 'price_asc':
        query = query.order_by(Product.price.asc())
    elif sort_by == 'price_desc':
        query = query.order_by(Product.price.desc())
    elif sort_by == 'name':
        query = query.order_by(Product.name.asc())
    else:  # newest
        query = query.order_by(Product.created_at.desc())
    
    # Paginate
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'success': True,
        'data': {
            'products': [p.to_dict() for p in pagination.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': pagination.total,
                'pages': pagination.pages,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            }
        }
    }), 200


@products_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Get single product by ID"""
    product = Product.query.get(product_id)
    
    if not product:
        return jsonify({
            'success': False,
            'message': 'Sản phẩm không tồn tại'
        }), 404
    
    return jsonify({
        'success': True,
        'data': product.to_dict()
    }), 200


@products_bp.route('', methods=['POST'])
@admin_required
def create_product():
    """
    Create a new product (Admin only)
    ---
    Request Body:
        - name: string (required)
        - description: string (optional)
        - price: float (required)
        - stock: int (optional, default: 0)
        - image_url: string (optional)
        - category_id: int (optional)
    """
    data = request.get_json()
    
    # Validate required fields
    if not data.get('name'):
        return jsonify({
            'success': False,
            'message': 'Tên sản phẩm là bắt buộc'
        }), 400
    
    if not data.get('price'):
        return jsonify({
            'success': False,
            'message': 'Giá sản phẩm là bắt buộc'
        }), 400
    
    try:
        price = float(data['price'])
        if price < 0:
            raise ValueError
    except (ValueError, TypeError):
        return jsonify({
            'success': False,
            'message': 'Giá không hợp lệ'
        }), 400
    
    # Validate category if provided
    if data.get('category_id'):
        category = Category.query.get(data['category_id'])
        if not category:
            return jsonify({
                'success': False,
                'message': 'Danh mục không tồn tại'
            }), 400
    
    # Create product
    product = Product(
        name=data['name'],
        description=data.get('description'),
        price=price,
        stock=data.get('stock', 0),
        image_url=data.get('image_url'),
        category_id=data.get('category_id')
    )
    
    try:
        db.session.add(product)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Tạo sản phẩm thành công',
            'data': product.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Lỗi: {str(e)}'
        }), 500


@products_bp.route('/<int:product_id>', methods=['PUT'])
@admin_required
def update_product(product_id):
    """Update a product (Admin only)"""
    product = Product.query.get(product_id)
    
    if not product:
        return jsonify({
            'success': False,
            'message': 'Sản phẩm không tồn tại'
        }), 404
    
    data = request.get_json()
    
    # Update fields
    if 'name' in data:
        product.name = data['name']
    if 'description' in data:
        product.description = data['description']
    if 'price' in data:
        try:
            price = float(data['price'])
            if price < 0:
                raise ValueError
            product.price = price
        except (ValueError, TypeError):
            return jsonify({
                'success': False,
                'message': 'Giá không hợp lệ'
            }), 400
    if 'stock' in data:
        product.stock = int(data['stock'])
    if 'image_url' in data:
        product.image_url = data['image_url']
    if 'category_id' in data:
        if data['category_id']:
            category = Category.query.get(data['category_id'])
            if not category:
                return jsonify({
                    'success': False,
                    'message': 'Danh mục không tồn tại'
                }), 400
        product.category_id = data['category_id']
    
    try:
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Cập nhật sản phẩm thành công',
            'data': product.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Lỗi: {str(e)}'
        }), 500


@products_bp.route('/<int:product_id>', methods=['DELETE'])
@admin_required
def delete_product(product_id):
    """Delete a product (Admin only)"""
    product = Product.query.get(product_id)
    
    if not product:
        return jsonify({
            'success': False,
            'message': 'Sản phẩm không tồn tại'
        }), 404
    
    try:
        db.session.delete(product)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Xóa sản phẩm thành công'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Lỗi: {str(e)}'
        }), 500
