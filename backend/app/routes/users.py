"""
User Routes
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import User

users_bp = Blueprint('users', __name__)


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


@users_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get current user profile"""
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({
            'success': False,
            'message': 'Người dùng không tồn tại'
        }), 404
    
    return jsonify({
        'success': True,
        'data': user.to_dict()
    }), 200


@users_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """
    Update current user profile
    ---
    Request Body:
        - full_name: string (optional)
        - phone: string (optional)
        - address: string (optional)
    """
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({
            'success': False,
            'message': 'Người dùng không tồn tại'
        }), 404
    
    data = request.get_json()
    
    if 'full_name' in data:
        if not data['full_name']:
            return jsonify({
                'success': False,
                'message': 'Họ tên không được để trống'
            }), 400
        user.full_name = data['full_name']
    
    if 'phone' in data:
        user.phone = data['phone']
    
    if 'address' in data:
        user.address = data['address']
    
    try:
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Cập nhật thông tin thành công',
            'data': user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Lỗi: {str(e)}'
        }), 500


# Admin routes

@users_bp.route('/admin/all', methods=['GET'])
@admin_required
def admin_get_all_users():
    """Get all users (Admin only)"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    search = request.args.get('search', '')
    role = request.args.get('role')
    
    query = User.query
    
    if search:
        search_term = f'%{search}%'
        query = query.filter(
            db.or_(
                User.email.ilike(search_term),
                User.full_name.ilike(search_term)
            )
        )
    
    if role:
        query = query.filter_by(role=role)
    
    query = query.order_by(User.created_at.desc())
    
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'success': True,
        'data': {
            'users': [u.to_dict() for u in pagination.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': pagination.total,
                'pages': pagination.pages
            }
        }
    }), 200


@users_bp.route('/admin/<int:user_id>', methods=['GET'])
@admin_required
def admin_get_user(user_id):
    """Get user by ID (Admin only)"""
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({
            'success': False,
            'message': 'Người dùng không tồn tại'
        }), 404
    
    return jsonify({
        'success': True,
        'data': user.to_dict()
    }), 200


@users_bp.route('/admin/<int:user_id>/role', methods=['PUT'])
@admin_required
def admin_update_user_role(user_id):
    """
    Update user role (Admin only)
    ---
    Request Body:
        - role: string (required) - 'customer' or 'admin'
    """
    data = request.get_json()
    new_role = data.get('role')
    
    if new_role not in ['customer', 'admin']:
        return jsonify({
            'success': False,
            'message': 'Role không hợp lệ. Cho phép: customer, admin'
        }), 400
    
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({
            'success': False,
            'message': 'Người dùng không tồn tại'
        }), 404
    
    # Prevent self-demotion
    current_user_id = int(get_jwt_identity())
    if user.id == current_user_id and new_role == 'customer':
        return jsonify({
            'success': False,
            'message': 'Bạn không thể tự hạ cấp chính mình'
        }), 400
    
    try:
        user.role = new_role
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Đã cập nhật role thành {new_role}',
            'data': user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Lỗi: {str(e)}'
        }), 500


@users_bp.route('/admin/stats', methods=['GET'])
@admin_required
def admin_get_user_stats():
    """Get user statistics (Admin only)"""
    from sqlalchemy import func
    
    total_users = User.query.count()
    total_customers = User.query.filter_by(role='customer').count()
    total_admins = User.query.filter_by(role='admin').count()
    
    return jsonify({
        'success': True,
        'data': {
            'total_users': total_users,
            'total_customers': total_customers,
            'total_admins': total_admins
        }
    }), 200
