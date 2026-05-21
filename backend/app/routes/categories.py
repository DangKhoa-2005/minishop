"""
Category Routes
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Category, User

categories_bp = Blueprint('categories', __name__)


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


@categories_bp.route('', methods=['GET'])
def get_categories():
    """Get all categories"""
    include_products = request.args.get('include_products', 'false').lower() == 'true'
    
    categories = Category.query.order_by(Category.name).all()
    
    return jsonify({
        'success': True,
        'data': [c.to_dict(include_products=include_products) for c in categories]
    }), 200


@categories_bp.route('/<int:category_id>', methods=['GET'])
def get_category(category_id):
    """Get single category by ID"""
    include_products = request.args.get('include_products', 'false').lower() == 'true'
    
    category = Category.query.get(category_id)
    
    if not category:
        return jsonify({
            'success': False,
            'message': 'Danh mục không tồn tại'
        }), 404
    
    return jsonify({
        'success': True,
        'data': category.to_dict(include_products=include_products)
    }), 200


@categories_bp.route('', methods=['POST'])
@admin_required
def create_category():
    """
    Create a new category (Admin only)
    ---
    Request Body:
        - name: string (required)
        - description: string (optional)
        - image_url: string (optional)
    """
    data = request.get_json()
    
    if not data.get('name'):
        return jsonify({
            'success': False,
            'message': 'Tên danh mục là bắt buộc'
        }), 400
    
    # Check if name exists
    if Category.query.filter_by(name=data['name']).first():
        return jsonify({
            'success': False,
            'message': 'Tên danh mục đã tồn tại'
        }), 400
    
    category = Category(
        name=data['name'],
        description=data.get('description'),
        image_url=data.get('image_url')
    )
    
    try:
        db.session.add(category)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Tạo danh mục thành công',
            'data': category.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Lỗi: {str(e)}'
        }), 500


@categories_bp.route('/<int:category_id>', methods=['PUT'])
@admin_required
def update_category(category_id):
    """Update a category (Admin only)"""
    category = Category.query.get(category_id)
    
    if not category:
        return jsonify({
            'success': False,
            'message': 'Danh mục không tồn tại'
        }), 404
    
    data = request.get_json()
    
    # Check for duplicate name
    if 'name' in data and data['name'] != category.name:
        if Category.query.filter_by(name=data['name']).first():
            return jsonify({
                'success': False,
                'message': 'Tên danh mục đã tồn tại'
            }), 400
        category.name = data['name']
    
    if 'description' in data:
        category.description = data['description']
    if 'image_url' in data:
        category.image_url = data['image_url']
    
    try:
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Cập nhật danh mục thành công',
            'data': category.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Lỗi: {str(e)}'
        }), 500


@categories_bp.route('/<int:category_id>', methods=['DELETE'])
@admin_required
def delete_category(category_id):
    """Delete a category (Admin only)"""
    category = Category.query.get(category_id)
    
    if not category:
        return jsonify({
            'success': False,
            'message': 'Danh mục không tồn tại'
        }), 404
    
    try:
        db.session.delete(category)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Xóa danh mục thành công'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Lỗi: {str(e)}'
        }), 500
