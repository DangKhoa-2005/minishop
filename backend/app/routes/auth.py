"""
Authentication Routes
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity
)
from app import db
from app.models import User, Cart

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user
    ---
    Request Body:
        - email: string (required)
        - password: string (required)
        - full_name: string (required)
        - phone: string (optional)
    """
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['email', 'password', 'full_name']
    for field in required_fields:
        if not data.get(field):
            return jsonify({
                'success': False,
                'message': f'{field} là bắt buộc'
            }), 400
    
    # Check if email exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({
            'success': False,
            'message': 'Email đã được sử dụng'
        }), 400
    
    # Validate password length
    if len(data['password']) < 6:
        return jsonify({
            'success': False,
            'message': 'Mật khẩu phải có ít nhất 6 ký tự'
        }), 400
    
    # Create new user
    user = User(
        email=data['email'],
        full_name=data['full_name'],
        phone=data.get('phone'),
        role='customer'
    )
    user.set_password(data['password'])
    
    try:
        db.session.add(user)
        db.session.flush()  # Get user ID
        
        # Create cart for user
        cart = Cart(user_id=user.id)
        db.session.add(cart)
        
        db.session.commit()
        
        # Generate tokens
        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))
        
        return jsonify({
            'success': True,
            'message': 'Đăng ký thành công',
            'data': {
                'user': user.to_dict(),
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Lỗi: {str(e)}'
        }), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login user
    ---
    Request Body:
        - email: string (required)
        - password: string (required)
    """
    data = request.get_json()
    
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({
            'success': False,
            'message': 'Email và mật khẩu là bắt buộc'
        }), 400
    
    # Find user
    user = User.query.filter_by(email=email).first()
    
    if not user or not user.check_password(password):
        return jsonify({
            'success': False,
            'message': 'Email hoặc mật khẩu không đúng'
        }), 401
    
    # Generate tokens
    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))
    
    return jsonify({
        'success': True,
        'message': 'Đăng nhập thành công',
        'data': {
            'user': user.to_dict(),
            'access_token': access_token,
            'refresh_token': refresh_token
        }
    }), 200


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current logged in user"""
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


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Refresh access token"""
    user_id = get_jwt_identity()
    access_token = create_access_token(identity=str(user_id))
    
    return jsonify({
        'success': True,
        'data': {
            'access_token': access_token
        }
    }), 200


@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    """
    Change user password
    ---
    Request Body:
        - current_password: string (required)
        - new_password: string (required)
    """
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({
            'success': False,
            'message': 'Người dùng không tồn tại'
        }), 404
    
    data = request.get_json()
    current_password = data.get('current_password')
    new_password = data.get('new_password')
    
    if not current_password or not new_password:
        return jsonify({
            'success': False,
            'message': 'Cần nhập mật khẩu hiện tại và mật khẩu mới'
        }), 400
    
    if not user.check_password(current_password):
        return jsonify({
            'success': False,
            'message': 'Mật khẩu hiện tại không đúng'
        }), 400
    
    if len(new_password) < 6:
        return jsonify({
            'success': False,
            'message': 'Mật khẩu mới phải có ít nhất 6 ký tự'
        }), 400
    
    user.set_password(new_password)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Đổi mật khẩu thành công'
    }), 200
