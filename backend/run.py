"""
Mini Shop Backend - Entry Point
"""
import os
from app import create_app, db
from app.models import User, Category, Product

app = create_app()


@app.cli.command('init-db')
def init_db():
    """Initialize database with sample data"""
    with app.app_context():
        db.create_all()
        
        # Check if data exists
        if User.query.first():
            print("Database already has data. Skipping...")
            return
        
        # Create admin user
        admin = User(
            email='admin@minishop.com',
            full_name='Admin',
            role='admin'
        )
        admin.set_password('admin123')
        db.session.add(admin)
        
        # Create sample customer
        customer = User(
            email='customer@example.com',
            full_name='Nguyễn Văn A',
            phone='0901234567',
            address='123 Đường ABC, Quận 1, TP.HCM',
            role='customer'
        )
        customer.set_password('123456')
        db.session.add(customer)
        
        # Create categories
        categories = [
            Category(name='Điện thoại', description='Điện thoại di động các loại'),
            Category(name='Laptop', description='Máy tính xách tay'),
            Category(name='Phụ kiện', description='Phụ kiện điện tử'),
            Category(name='Tablet', description='Máy tính bảng'),
        ]
        for cat in categories:
            db.session.add(cat)
        
        db.session.flush()
        
        # Create sample products
        products = [
            Product(
                name='iPhone 15 Pro Max 256GB',
                description='iPhone 15 Pro Max với chip A17 Pro, camera 48MP, màn hình Super Retina XDR 6.7 inch',
                price=34990000,
                stock=50,
                category_id=categories[0].id,
                image_url='https://via.placeholder.com/400x400?text=iPhone+15+Pro+Max'
            ),
            Product(
                name='Samsung Galaxy S24 Ultra',
                description='Samsung Galaxy S24 Ultra 512GB, màn hình Dynamic AMOLED 2X, camera 200MP',
                price=32990000,
                stock=30,
                category_id=categories[0].id,
                image_url='https://via.placeholder.com/400x400?text=Galaxy+S24+Ultra'
            ),
            Product(
                name='Xiaomi 14 Ultra',
                description='Xiaomi 14 Ultra 512GB, camera Leica, Snapdragon 8 Gen 3',
                price=24990000,
                stock=25,
                category_id=categories[0].id,
                image_url='https://via.placeholder.com/400x400?text=Xiaomi+14+Ultra'
            ),
            Product(
                name='MacBook Pro 14 M3 Pro',
                description='MacBook Pro 14 inch M3 Pro, 18GB RAM, 512GB SSD, màn hình Liquid Retina XDR',
                price=49990000,
                stock=20,
                category_id=categories[1].id,
                image_url='https://via.placeholder.com/400x400?text=MacBook+Pro+M3'
            ),
            Product(
                name='Dell XPS 15',
                description='Dell XPS 15 Core i7-13700H, RTX 4060, 16GB RAM, 512GB SSD',
                price=42990000,
                stock=15,
                category_id=categories[1].id,
                image_url='https://via.placeholder.com/400x400?text=Dell+XPS+15'
            ),
            Product(
                name='ASUS ROG Zephyrus G14',
                description='ASUS ROG Zephyrus G14 AMD Ryzen 9, RTX 4070, 32GB RAM, 1TB SSD',
                price=45990000,
                stock=10,
                category_id=categories[1].id,
                image_url='https://via.placeholder.com/400x400?text=ROG+Zephyrus+G14'
            ),
            Product(
                name='AirPods Pro 2',
                description='AirPods Pro 2nd Generation với chip H2, Active Noise Cancellation',
                price=5990000,
                stock=100,
                category_id=categories[2].id,
                image_url='https://via.placeholder.com/400x400?text=AirPods+Pro+2'
            ),
            Product(
                name='Samsung Galaxy Buds3 Pro',
                description='Samsung Galaxy Buds3 Pro, ANC, 360 Audio, IP57',
                price=4990000,
                stock=80,
                category_id=categories[2].id,
                image_url='https://via.placeholder.com/400x400?text=Galaxy+Buds3+Pro'
            ),
            Product(
                name='Apple Watch Series 9',
                description='Apple Watch Series 9 GPS 45mm, chip S9 SiP, màn hình Always-On Retina',
                price=10990000,
                stock=40,
                category_id=categories[2].id,
                image_url='https://via.placeholder.com/400x400?text=Apple+Watch+S9'
            ),
            Product(
                name='iPad Pro M4 11 inch',
                description='iPad Pro 11 inch M4, 256GB, màn hình Ultra Retina XDR, Face ID',
                price=24990000,
                stock=25,
                category_id=categories[3].id,
                image_url='https://via.placeholder.com/400x400?text=iPad+Pro+M4'
            ),
            Product(
                name='Samsung Galaxy Tab S9 Ultra',
                description='Samsung Galaxy Tab S9 Ultra 512GB, màn hình 14.6 inch Dynamic AMOLED 2X',
                price=28990000,
                stock=20,
                category_id=categories[3].id,
                image_url='https://via.placeholder.com/400x400?text=Galaxy+Tab+S9+Ultra'
            ),
            Product(
                name='Xiaomi Pad 6S Pro',
                description='Xiaomi Pad 6S Pro 256GB, màn hình 12.4 inch 3K, Snapdragon 8 Gen 2',
                price=12990000,
                stock=35,
                category_id=categories[3].id,
                image_url='https://via.placeholder.com/400x400?text=Xiaomi+Pad+6S+Pro'
            ),
        ]
        
        for product in products:
            db.session.add(product)
        
        db.session.commit()
        
        print("Database initialized successfully!")
        print(f"Admin: admin@minishop.com / admin123")
        print(f"Customer: customer@example.com / 123456")
        print(f"Created {len(categories)} categories and {len(products)} products")


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    # Disable the reloader so the process stays in foreground for testing
    app.run(host='0.0.0.0', port=port, debug=True, use_reloader=False)
