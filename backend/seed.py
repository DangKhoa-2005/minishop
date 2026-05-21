"""Seed database with sample data"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User, Category, Product

app = create_app()

with app.app_context():
    # Drop and recreate all tables
    print("Dropping all tables...")
    db.drop_all()
    print("Creating all tables...")
    db.create_all()
    
    print("Seeding database...")
    
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
        Category(name='Điện thoại', description='Điện thoại di động các loại', image_url='https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400'),
        Category(name='Laptop', description='Máy tính xách tay', image_url='https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=400'),
        Category(name='Phụ kiện', description='Phụ kiện điện tử', image_url='https://images.unsplash.com/photo-1583394838336-acd977736f90?w=400'),
        Category(name='Tablet', description='Máy tính bảng', image_url='https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=400'),
        Category(name='Đồng hồ thông minh', description='Smartwatch các loại', image_url='https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400'),
    ]
    for cat in categories:
        db.session.add(cat)
    
    db.session.flush()
    
    # Create sample products with curated image URLs matching each product
    products = [
        # Điện thoại (category_id=1)
        Product(
            name='iPhone 15 Pro Max 256GB',
            description='iPhone 15 Pro Max với chip A17 Pro, camera 48MP, màn hình Super Retina XDR 6.7 inch. Thiết kế titan cao cấp, nhẹ và bền.',
            price=34990000,
            stock=50,
            image_url='https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/iphone-15-pro-finish-select-202309-6-7inch-naturaltitanium?wid=400&fmt=jpeg',
            category_id=1
        ),
        Product(
            name='iPhone 15 Pro 128GB',
            description='iPhone 15 Pro với chip A17 Pro, camera 48MP, màn hình 6.1 inch. Action Button mới.',
            price=28990000,
            stock=45,
            image_url='https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/iphone-15-pro-finish-select-202309-6-1inch-bluetitanium?wid=400&fmt=jpeg',
            category_id=1
        ),
        Product(
            name='iPhone 15 128GB',
            description='iPhone 15 với Dynamic Island, camera 48MP, chip A16 Bionic mạnh mẽ.',
            price=22990000,
            stock=60,
            image_url='https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/iphone-15-finish-select-202309-6-1inch-blue?wid=400&fmt=jpeg',
            category_id=1
        ),
        Product(
            name='Samsung Galaxy S24 Ultra',
            description='Galaxy S24 Ultra với S Pen, camera 200MP, màn hình Dynamic AMOLED 2X 6.8 inch, chip Snapdragon 8 Gen 3.',
            price=33990000,
            stock=30,
            image_url='https://images.unsplash.com/photo-1678685888221-cda773a3dcdb?w=400&h=400&fit=crop',
            category_id=1
        ),
        Product(
            name='Samsung Galaxy S24+',
            description='Galaxy S24+ với màn hình 6.7 inch, camera 50MP, AI Galaxy thông minh.',
            price=26990000,
            stock=35,
            image_url='https://images.unsplash.com/photo-1610945415295-d9bbf067e59c?w=400&h=400&fit=crop',
            category_id=1
        ),
        Product(
            name='Samsung Galaxy Z Fold5',
            description='Điện thoại gập cao cấp, màn hình chính 7.6 inch, chip Snapdragon 8 Gen 2.',
            price=41990000,
            stock=20,
            image_url='https://images.unsplash.com/photo-1628744448840-55bdb2497bd4?w=400&h=400&fit=crop',
            category_id=1
        ),
        Product(
            name='Xiaomi 14 Ultra',
            description='Xiaomi 14 Ultra với camera Leica, Snapdragon 8 Gen 3, sạc nhanh 90W.',
            price=29990000,
            stock=25,
            image_url='https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=400&h=400&fit=crop',
            category_id=1
        ),
        Product(
            name='OPPO Find X7 Ultra',
            description='OPPO Find X7 Ultra với camera periscope kép, màn hình LTPO 120Hz.',
            price=27990000,
            stock=22,
            image_url='https://images.unsplash.com/photo-1574944985070-8f3ebc6b79d2?w=400&h=400&fit=crop',
            category_id=1
        ),
        
        # Laptop (category_id=2)
        Product(
            name='MacBook Pro 14 M3 Pro',
            description='MacBook Pro 14 inch với chip M3 Pro, 18GB RAM, 512GB SSD. Màn hình Liquid Retina XDR.',
            price=52990000,
            stock=20,
            image_url='https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/mbp14-spacegray-select-202310?wid=400&fmt=jpeg',
            category_id=2
        ),
        Product(
            name='MacBook Air 15 M3',
            description='MacBook Air 15 inch mỏng nhẹ với chip M3, 8GB RAM, 256GB SSD.',
            price=32990000,
            stock=30,
            image_url='https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/mba15-midnight-select-202306?wid=400&fmt=jpeg',
            category_id=2
        ),
        Product(
            name='MacBook Air 13 M3',
            description='MacBook Air 13 inch với chip M3, thiết kế siêu mỏng, pin 18 giờ.',
            price=27990000,
            stock=40,
            image_url='https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/mba13-starlight-select-202402?wid=400&fmt=jpeg',
            category_id=2
        ),
        Product(
            name='Dell XPS 15 9530',
            description='Dell XPS 15 với Intel Core i7-13700H, 16GB RAM, 512GB SSD, RTX 4050.',
            price=45990000,
            stock=15,
            image_url='https://images.unsplash.com/photo-1593642702821-c8da6771f0c6?w=400&h=400&fit=crop',
            category_id=2
        ),
        Product(
            name='Dell XPS 13 Plus',
            description='Dell XPS 13 Plus với Intel Core i7, màn hình OLED 3.5K, thiết kế premium.',
            price=38990000,
            stock=18,
            image_url='https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=400&h=400&fit=crop',
            category_id=2
        ),
        Product(
            name='ASUS ROG Zephyrus G14',
            description='Laptop gaming ASUS ROG với AMD Ryzen 9, RTX 4060, màn hình 165Hz.',
            price=42990000,
            stock=12,
            image_url='https://images.unsplash.com/photo-1603302576837-37561b2e2302?w=400&h=400&fit=crop',
            category_id=2
        ),
        Product(
            name='HP Spectre x360 14',
            description='Laptop 2-in-1 cao cấp HP với màn hình OLED, Intel Core i7 Gen 13.',
            price=39990000,
            stock=14,
            image_url='https://images.unsplash.com/photo-1544731612-de7f96afe55f?w=400&h=400&fit=crop',
            category_id=2
        ),
        Product(
            name='Lenovo ThinkPad X1 Carbon',
            description='ThinkPad X1 Carbon Gen 11, Intel Core i7, 16GB RAM, bàn phím huyền thoại.',
            price=43990000,
            stock=16,
            image_url='https://images.unsplash.com/photo-1525547719571-a2d4ac8945e2?w=400&h=400&fit=crop',
            category_id=2
        ),
        
        # Phụ kiện (category_id=3)
        Product(
            name='AirPods Pro 2 USB-C',
            description='AirPods Pro thế hệ 2 với chip H2, chống ồn chủ động, cổng USB-C.',
            price=6490000,
            stock=100,
            image_url='https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/MQD83?wid=400&fmt=jpeg',
            category_id=3
        ),
        Product(
            name='AirPods Max',
            description='Tai nghe over-ear cao cấp Apple với âm thanh không gian, chống ồn tuyệt vời.',
            price=12990000,
            stock=25,
            image_url='https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/airpods-max-select-silver-202011?wid=400&fmt=jpeg',
            category_id=3
        ),
        Product(
            name='Sony WH-1000XM5',
            description='Tai nghe chống ồn hàng đầu Sony, pin 30 giờ, âm thanh Hi-Res.',
            price=8490000,
            stock=40,
            image_url='https://images.unsplash.com/photo-1618366712010-f4ae9c647dcb?w=400&h=400&fit=crop',
            category_id=3
        ),
        Product(
            name='Samsung Galaxy Buds2 Pro',
            description='Tai nghe true wireless Samsung với ANC, âm thanh 24bit Hi-Fi.',
            price=4490000,
            stock=60,
            image_url='https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=400&h=400&fit=crop',
            category_id=3
        ),
        Product(
            name='Apple Magic Keyboard',
            description='Bàn phím không dây Apple với Touch ID, thiết kế mỏng nhẹ.',
            price=4290000,
            stock=50,
            image_url='https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/MK2C3?wid=400&fmt=jpeg',
            category_id=3
        ),
        Product(
            name='Logitech MX Master 3S',
            description='Chuột không dây cao cấp Logitech, cảm biến 8000 DPI, sạc USB-C.',
            price=2790000,
            stock=70,
            image_url='https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=400&h=400&fit=crop',
            category_id=3
        ),
        Product(
            name='Anker PowerCore 26800mAh',
            description='Sạc dự phòng dung lượng cao, hỗ trợ sạc nhanh PD 45W.',
            price=1290000,
            stock=80,
            image_url='https://images.unsplash.com/photo-1609091839311-d5365f9ff1c5?w=400&h=400&fit=crop',
            category_id=3
        ),
        Product(
            name='Apple MagSafe Charger',
            description='Bộ sạc không dây MagSafe 15W cho iPhone 12 trở lên.',
            price=1190000,
            stock=90,
            image_url='https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/MHXH3?wid=400&fmt=jpeg',
            category_id=3
        ),
        
        # Tablet (category_id=4)
        Product(
            name='iPad Pro 12.9 M4 256GB',
            description='iPad Pro 12.9 inch với chip M4, màn hình Ultra Retina XDR, hỗ trợ Apple Pencil Pro.',
            price=35990000,
            stock=20,
            image_url='https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=400&h=400&fit=crop',
            category_id=4
        ),
        Product(
            name='iPad Pro 11 M4 256GB',
            description='iPad Pro 11 inch với chip M4, màn hình Liquid Retina, siêu mỏng nhẹ.',
            price=28990000,
            stock=25,
            image_url='https://images.unsplash.com/photo-1585790050230-5dd28404ccb9?w=400&h=400&fit=crop',
            category_id=4
        ),
        Product(
            name='iPad Air 13 M2',
            description='iPad Air 13 inch với chip M2, màn hình Liquid Retina, hỗ trợ Apple Pencil.',
            price=22990000,
            stock=30,
            image_url='https://images.unsplash.com/photo-1542751110-97427bbecf20?w=400&h=400&fit=crop',
            category_id=4
        ),
        Product(
            name='iPad 10.9 (Gen 10)',
            description='iPad thế hệ 10 với chip A14 Bionic, màn hình 10.9 inch, USB-C.',
            price=12990000,
            stock=50,
            image_url='https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/ipad-10th-gen-finish-select-202212-blue-wifi?wid=400&fmt=jpeg',
            category_id=4
        ),
        Product(
            name='Samsung Galaxy Tab S9 Ultra',
            description='Galaxy Tab S9 Ultra 14.6 inch, Snapdragon 8 Gen 2, S Pen đi kèm.',
            price=31990000,
            stock=18,
            image_url='https://images.unsplash.com/photo-1611532736597-de2d4265fba3?w=400&h=400&fit=crop',
            category_id=4
        ),
        Product(
            name='Samsung Galaxy Tab S9+',
            description='Galaxy Tab S9+ 12.4 inch, màn hình AMOLED 120Hz, chip Snapdragon 8 Gen 2.',
            price=24990000,
            stock=22,
            image_url='https://images.unsplash.com/photo-1561154464-82e9adf32764?w=400&h=400&fit=crop',
            category_id=4
        ),
        
        # Đồng hồ thông minh (category_id=5)
        Product(
            name='Apple Watch Ultra 2',
            description='Apple Watch Ultra 2 với GPS + Cellular, vỏ Titan, pin 36 giờ.',
            price=21990000,
            stock=25,
            image_url='https://images.unsplash.com/photo-1551816230-ef5deaed4a26?w=400&h=400&fit=crop',
            category_id=5
        ),
        Product(
            name='Apple Watch Series 9',
            description='Apple Watch Series 9 GPS 45mm, chip S9, Double Tap mới.',
            price=11990000,
            stock=40,
            image_url='https://images.unsplash.com/photo-1434493789847-2f02dc6ca35d?w=400&h=400&fit=crop',
            category_id=5
        ),
        Product(
            name='Apple Watch SE 2',
            description='Apple Watch SE thế hệ 2, GPS 44mm, chip S8, giá tốt nhất.',
            price=7490000,
            stock=50,
            image_url='https://images.unsplash.com/photo-1617043786394-f977fa12eddf?w=400&h=400&fit=crop',
            category_id=5
        ),
        Product(
            name='Samsung Galaxy Watch6 Classic',
            description='Galaxy Watch6 Classic 47mm với vòng bezel xoay, Wear OS.',
            price=10990000,
            stock=30,
            image_url='https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?w=400&h=400&fit=crop',
            category_id=5
        ),
        Product(
            name='Samsung Galaxy Watch6',
            description='Galaxy Watch6 44mm, màn hình Super AMOLED, đo sức khỏe toàn diện.',
            price=7990000,
            stock=35,
            image_url='https://images.unsplash.com/photo-1579586337278-3befd40fd17a?w=400&h=400&fit=crop',
            category_id=5
        ),
        Product(
            name='Garmin Fenix 7 Pro',
            description='Đồng hồ thể thao cao cấp Garmin, GPS đa băng tần, pin 22 ngày.',
            price=18990000,
            stock=15,
            image_url='https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&h=400&fit=crop',
            category_id=5
        ),
    ]
    
    for product in products:
        db.session.add(product)
    
    db.session.commit()
    print("=" * 50)
    print("Database seeded successfully!")
    print("=" * 50)
    print(f"Created {len(categories)} categories")
    print(f"Created {len(products)} products")
    print("-" * 50)
    print("Test accounts:")
    print("  Admin: admin@minishop.com / admin123")
    print("  Customer: customer@example.com / 123456")
    print("=" * 50)
