"""
Unit Tests for Mini Shop Backend
Tests: Models, Authentication, Products, Cart, Orders
"""
import pytest
import json
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import User, Category, Product, Cart, CartItem, Order, OrderItem


@pytest.fixture
def app():
    """Create application for testing"""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['JWT_SECRET_KEY'] = 'test-secret-key'
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Test client"""
    return app.test_client()


@pytest.fixture
def sample_data(app):
    """Create sample data for tests"""
    with app.app_context():
        # Create admin user
        admin = User(email='admin@test.com', full_name='Admin User', role='admin')
        admin.set_password('admin123')
        db.session.add(admin)

        # Create customer user
        customer = User(email='customer@test.com', full_name='Customer User', 
                       phone='0901234567', address='123 Test St', role='customer')
        customer.set_password('123456')
        db.session.add(customer)
        db.session.flush()

        # Create cart for customer
        cart = Cart(user_id=customer.id)
        db.session.add(cart)

        # Create category
        category = Category(name='Điện thoại', description='Smartphones')
        db.session.add(category)
        db.session.flush()

        # Create products
        product1 = Product(name='iPhone 15', description='Apple iPhone 15', 
                          price=22990000, stock=10, category_id=category.id)
        product2 = Product(name='Samsung S24', description='Samsung Galaxy S24', 
                          price=25990000, stock=5, category_id=category.id)
        product3 = Product(name='Out of Stock Phone', description='No stock', 
                          price=999000, stock=0, category_id=category.id)
        db.session.add_all([product1, product2, product3])
        db.session.commit()

        return {
            'admin': admin,
            'customer': customer,
            'category': category,
            'product1': product1,
            'product2': product2,
            'product3': product3,
            'cart': cart
        }


def get_auth_token(client, email, password):
    """Helper to get JWT token"""
    response = client.post('/api/auth/login', 
        data=json.dumps({'email': email, 'password': password}),
        content_type='application/json')
    data = response.get_json()
    return data['data']['access_token']


# ==================== MODEL TESTS ====================

class TestUserModel:
    """Test User model"""

    def test_set_and_check_password(self, app):
        with app.app_context():
            user = User(email='test@test.com', full_name='Test')
            user.set_password('mypassword')
            assert user.check_password('mypassword') is True
            assert user.check_password('wrongpassword') is False

    def test_is_admin(self, app):
        with app.app_context():
            admin = User(email='a@test.com', full_name='A', role='admin')
            customer = User(email='c@test.com', full_name='C', role='customer')
            assert admin.is_admin() is True
            assert customer.is_admin() is False

    def test_to_dict(self, app, sample_data):
        with app.app_context():
            user = User.query.filter_by(email='customer@test.com').first()
            d = user.to_dict()
            assert d['email'] == 'customer@test.com'
            assert d['full_name'] == 'Customer User'
            assert d['role'] == 'customer'
            assert 'password_hash' not in d


class TestProductModel:
    """Test Product model"""

    def test_is_in_stock(self, app, sample_data):
        with app.app_context():
            p = Product.query.filter_by(name='iPhone 15').first()
            assert p.is_in_stock(1) is True
            assert p.is_in_stock(10) is True
            assert p.is_in_stock(11) is False

    def test_reduce_stock(self, app, sample_data):
        with app.app_context():
            p = Product.query.filter_by(name='iPhone 15').first()
            assert p.reduce_stock(3) is True
            assert p.stock == 7
            assert p.reduce_stock(100) is False
            assert p.stock == 7  # unchanged

    def test_out_of_stock(self, app, sample_data):
        with app.app_context():
            p = Product.query.filter_by(name='Out of Stock Phone').first()
            assert p.is_in_stock() is False
            d = p.to_dict()
            assert d['in_stock'] is False

    def test_to_dict_with_category(self, app, sample_data):
        with app.app_context():
            p = Product.query.filter_by(name='iPhone 15').first()
            d = p.to_dict(include_category=True)
            assert d['name'] == 'iPhone 15'
            assert d['category']['name'] == 'Điện thoại'
            assert d['price'] == 22990000.0


class TestOrderModel:
    """Test Order model"""

    def test_order_status_constants(self):
        assert Order.STATUS_CONFIRMED == 'confirmed'
        assert Order.STATUS_DELIVERED == 'delivered'
        assert len(Order.VALID_STATUSES) == 4

    def test_can_cancel(self, app, sample_data):
        with app.app_context():
            order_confirmed = Order(user_id=1, total_amount=100, status='confirmed',
                                  shipping_address='Test', phone='0123')
            order_shipping = Order(user_id=1, total_amount=100, status='shipping',
                                 shipping_address='Test', phone='0123')
            assert order_confirmed.can_cancel() is True
            assert order_shipping.can_cancel() is False

    def test_get_status_display(self, app):
        with app.app_context():
            order = Order(user_id=1, total_amount=100, status='confirmed',
                         shipping_address='Test', phone='0123')
            assert order.get_status_display() == 'Đã xác nhận'
            order.status = 'delivered'
            assert order.get_status_display() == 'Đã giao hàng'


class TestCategoryModel:
    """Test Category model"""

    def test_to_dict(self, app, sample_data):
        with app.app_context():
            cat = Category.query.filter_by(name='Điện thoại').first()
            d = cat.to_dict()
            assert d['name'] == 'Điện thoại'
            assert d['product_count'] == 3


# ==================== API TESTS ====================

class TestHealthAPI:
    """Test health endpoint"""

    def test_health_check(self, client):
        response = client.get('/api/health')
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'healthy'


class TestAuthAPI:
    """Test authentication endpoints"""

    def test_register_success(self, client, app):
        response = client.post('/api/auth/register',
            data=json.dumps({
                'email': 'new@test.com',
                'password': '123456',
                'full_name': 'New User'
            }),
            content_type='application/json')
        assert response.status_code == 201
        data = response.get_json()
        assert data['success'] is True
        assert 'access_token' in data['data']

    def test_register_duplicate_email(self, client, sample_data):
        response = client.post('/api/auth/register',
            data=json.dumps({
                'email': 'customer@test.com',
                'password': '123456',
                'full_name': 'Dup User'
            }),
            content_type='application/json')
        assert response.status_code == 400

    def test_register_short_password(self, client):
        response = client.post('/api/auth/register',
            data=json.dumps({
                'email': 'new@test.com',
                'password': '123',
                'full_name': 'New User'
            }),
            content_type='application/json')
        assert response.status_code == 400

    def test_register_missing_fields(self, client):
        response = client.post('/api/auth/register',
            data=json.dumps({'email': 'x@test.com'}),
            content_type='application/json')
        assert response.status_code == 400

    def test_login_success(self, client, sample_data):
        response = client.post('/api/auth/login',
            data=json.dumps({
                'email': 'customer@test.com',
                'password': '123456'
            }),
            content_type='application/json')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['data']['user']['email'] == 'customer@test.com'

    def test_login_wrong_password(self, client, sample_data):
        response = client.post('/api/auth/login',
            data=json.dumps({
                'email': 'customer@test.com',
                'password': 'wrongpassword'
            }),
            content_type='application/json')
        assert response.status_code == 401

    def test_login_nonexistent_user(self, client):
        response = client.post('/api/auth/login',
            data=json.dumps({
                'email': 'nobody@test.com',
                'password': '123456'
            }),
            content_type='application/json')
        assert response.status_code == 401

    def test_get_current_user(self, client, sample_data):
        token = get_auth_token(client, 'customer@test.com', '123456')
        response = client.get('/api/auth/me',
            headers={'Authorization': f'Bearer {token}'})
        assert response.status_code == 200
        data = response.get_json()
        assert data['data']['email'] == 'customer@test.com'

    def test_get_current_user_no_token(self, client):
        response = client.get('/api/auth/me')
        assert response.status_code == 401


class TestProductsAPI:
    """Test products endpoints"""

    def test_get_products(self, client, sample_data):
        response = client.get('/api/products')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert len(data['data']['products']) == 3

    def test_get_products_pagination(self, client, sample_data):
        response = client.get('/api/products?per_page=1&page=1')
        assert response.status_code == 200
        data = response.get_json()
        assert len(data['data']['products']) == 1
        assert data['data']['pagination']['total'] == 3

    def test_get_products_by_category(self, client, sample_data):
        with client.application.app_context():
            cat = Category.query.first()
            response = client.get(f'/api/products?category_id={cat.id}')
            assert response.status_code == 200
            data = response.get_json()
            assert len(data['data']['products']) == 3

    def test_get_product_detail(self, client, sample_data):
        with client.application.app_context():
            product = Product.query.filter_by(name='iPhone 15').first()
            response = client.get(f'/api/products/{product.id}')
            assert response.status_code == 200
            data = response.get_json()
            assert data['data']['name'] == 'iPhone 15'

    def test_get_product_not_found(self, client):
        response = client.get('/api/products/99999')
        assert response.status_code == 404

    def test_search_products(self, client, sample_data):
        response = client.get('/api/products?search=iPhone')
        assert response.status_code == 200
        data = response.get_json()
        assert len(data['data']['products']) >= 1
        assert 'iPhone' in data['data']['products'][0]['name']


class TestCategoriesAPI:
    """Test categories endpoints"""

    def test_get_categories(self, client, sample_data):
        response = client.get('/api/categories')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert len(data['data']) >= 1


class TestCartAPI:
    """Test cart endpoints"""

    def test_get_empty_cart(self, client, sample_data):
        token = get_auth_token(client, 'customer@test.com', '123456')
        response = client.get('/api/cart',
            headers={'Authorization': f'Bearer {token}'})
        assert response.status_code == 200
        data = response.get_json()
        assert data['data']['item_count'] == 0

    def test_add_to_cart(self, client, sample_data):
        token = get_auth_token(client, 'customer@test.com', '123456')
        with client.application.app_context():
            product = Product.query.filter_by(name='iPhone 15').first()
            response = client.post('/api/cart/add',
                data=json.dumps({'product_id': product.id, 'quantity': 2}),
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'})
            assert response.status_code in [200, 201]
            data = response.get_json()
            assert data['success'] is True

    def test_add_to_cart_no_auth(self, client, sample_data):
        response = client.post('/api/cart/add',
            data=json.dumps({'product_id': 1, 'quantity': 1}),
            content_type='application/json')
        assert response.status_code == 401


class TestOrdersAPI:
    """Test orders endpoints"""

    def test_checkout_success(self, client, sample_data):
        token = get_auth_token(client, 'customer@test.com', '123456')
        with client.application.app_context():
            # Add item to cart first
            product = Product.query.filter_by(name='iPhone 15').first()
            client.post('/api/cart/add',
                data=json.dumps({'product_id': product.id, 'quantity': 1}),
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'})

            # Checkout
            response = client.post('/api/orders/checkout',
                data=json.dumps({
                    'shipping_address': '123 Test Street',
                    'phone': '0901234567'
                }),
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'})
            assert response.status_code == 201
            data = response.get_json()
            assert data['success'] is True
            assert data['data']['status'] == 'confirmed'
            assert data['data']['payment_method'] == 'cod'

    def test_checkout_with_bank_transfer(self, client, sample_data):
        token = get_auth_token(client, 'customer@test.com', '123456')
        with client.application.app_context():
            product = Product.query.filter_by(name='Samsung S24').first()
            client.post('/api/cart/add',
                data=json.dumps({'product_id': product.id, 'quantity': 1}),
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'})

            response = client.post('/api/orders/checkout',
                data=json.dumps({
                    'shipping_address': '456 Test Street',
                    'phone': '0901234567',
                    'payment_method': 'bank_transfer'
                }),
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'})

            assert response.status_code == 201
            data = response.get_json()
            assert data['success'] is True
            assert data['data']['payment_method'] == 'bank_transfer'

    def test_checkout_empty_cart(self, client, sample_data):
        token = get_auth_token(client, 'customer@test.com', '123456')
        response = client.post('/api/orders/checkout',
            data=json.dumps({
                'shipping_address': '123 Test Street',
                'phone': '0901234567'
            }),
            content_type='application/json',
            headers={'Authorization': f'Bearer {token}'})
        assert response.status_code == 400

    def test_get_orders(self, client, sample_data):
        token = get_auth_token(client, 'customer@test.com', '123456')
        response = client.get('/api/orders',
            headers={'Authorization': f'Bearer {token}'})
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True

    def test_user_order_number_increments(self, client, sample_data):
        """Test that user_order_number increments per user"""
        token = get_auth_token(client, 'customer@test.com', '123456')
        with client.application.app_context():
            product = Product.query.filter_by(name='iPhone 15').first()

            # First order
            client.post('/api/cart/add',
                data=json.dumps({'product_id': product.id, 'quantity': 1}),
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'})
            resp1 = client.post('/api/orders/checkout',
                data=json.dumps({'shipping_address': 'Addr 1', 'phone': '0123'}),
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'})
            order1 = resp1.get_json()['data']

            # Second order
            client.post('/api/cart/add',
                data=json.dumps({'product_id': product.id, 'quantity': 1}),
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'})
            resp2 = client.post('/api/orders/checkout',
                data=json.dumps({'shipping_address': 'Addr 2', 'phone': '0123'}),
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'})
            order2 = resp2.get_json()['data']

            assert order1['user_order_number'] == 1
            assert order2['user_order_number'] == 2


class TestAdminAPI:
    """Test admin-only endpoints"""

    def test_admin_get_orders(self, client, sample_data):
        token = get_auth_token(client, 'admin@test.com', 'admin123')
        response = client.get('/api/orders/admin/all',
            headers={'Authorization': f'Bearer {token}'})
        assert response.status_code == 200

    def test_customer_cannot_access_admin(self, client, sample_data):
        token = get_auth_token(client, 'customer@test.com', '123456')
        response = client.get('/api/orders/admin/all',
            headers={'Authorization': f'Bearer {token}'})
        assert response.status_code == 403
