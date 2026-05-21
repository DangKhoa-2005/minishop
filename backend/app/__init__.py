"""
Mini Shop Backend - Flask Application Factory
"""
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate
from sqlalchemy import inspect, text

from config import config

# Initialize extensions
db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()


def _sync_orders_schema_and_data(app):
    """Ensure legacy orders schema/data matches current business rules."""
    try:
        inspector = inspect(db.engine)
        if 'orders' not in inspector.get_table_names():
            return

        columns = {col['name'] for col in inspector.get_columns('orders')}
        if 'payment_method' not in columns:
            db.session.execute(
                text("ALTER TABLE orders ADD COLUMN payment_method VARCHAR(50) NOT NULL DEFAULT 'cod'")
            )
            app.logger.info("Added missing column orders.payment_method")

        if db.engine.dialect.name != 'sqlite':
            db.session.execute(
                text("ALTER TABLE orders ALTER COLUMN status SET DEFAULT 'confirmed'")
            )

        # Business rule sync: pending is removed; normalize any legacy rows.
        db.session.execute(
            text("UPDATE orders SET status = 'confirmed' WHERE status = 'pending'")
        )
        db.session.commit()
    except Exception as exc:
        db.session.rollback()
        app.logger.warning(f"Could not sync orders schema/data: {exc}")


def create_app(config_name=None):
    """Application factory pattern"""
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    CORS(app, resources={
        r"/api/*": {
            "origins": [
                "http://localhost:5173",
                "http://127.0.0.1:5173",
                "http://localhost:3000",
                "http://127.0.0.1:3000",
                "http://localhost:8081",
                "http://127.0.0.1:8081"
            ],
            "methods": ["GET", "POST", "PUT", "DELETE", "PATCH"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.products import products_bp
    from app.routes.categories import categories_bp
    from app.routes.cart import cart_bp
    from app.routes.orders import orders_bp
    from app.routes.users import users_bp
    from app.routes.chatbot import chatbot_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(products_bp, url_prefix='/api/products')
    app.register_blueprint(categories_bp, url_prefix='/api/categories')
    app.register_blueprint(cart_bp, url_prefix='/api/cart')
    app.register_blueprint(orders_bp, url_prefix='/api/orders')
    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(chatbot_bp, url_prefix='/api/chatbot')
    
    # Health check endpoint
    @app.route('/api/health')
    def health_check():
        return {'status': 'healthy', 'message': 'Mini Shop API is running!'}
    
    # Create database tables
    with app.app_context():
        db.create_all()
        _sync_orders_schema_and_data(app)
    
    return app
