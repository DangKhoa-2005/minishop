# 📊 Database Schema - Mini Shop

## 1. Entity Relationship Diagram (ERD)

```
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│     users       │       │    categories   │       │    products     │
├─────────────────┤       ├─────────────────┤       ├─────────────────┤
│ id (PK)         │       │ id (PK)         │       │ id (PK)         │
│ email           │       │ name            │       │ name            │
│ password_hash   │       │ description     │       │ description     │
│ full_name       │       │ image_url       │       │ price           │
│ phone           │       │ created_at      │       │ stock           │
│ address         │       │ updated_at      │       │ image_url       │
│ role            │       └────────┬────────┘       │ category_id(FK) │──┐
│ created_at      │                │                │ created_at      │  │
│ updated_at      │                │                │ updated_at      │  │
└────────┬────────┘                │                └─────────────────┘  │
         │                         │                         ▲           │
         │                         └─────────────────────────┼───────────┘
         │                                                   │
         ▼                                                   │
┌─────────────────┐       ┌─────────────────┐               │
│     carts       │       │   cart_items    │               │
├─────────────────┤       ├─────────────────┤               │
│ id (PK)         │◀──────│ id (PK)         │               │
│ user_id (FK)    │       │ cart_id (FK)    │               │
│ created_at      │       │ product_id (FK) │───────────────┘
│ updated_at      │       │ quantity        │
└─────────────────┘       │ created_at      │
         │                └─────────────────┘
         │
         │
         ▼
┌─────────────────┐       ┌─────────────────┐
│     orders      │       │   order_items   │
├─────────────────┤       ├─────────────────┤
│ id (PK)         │◀──────│ id (PK)         │
│ user_id (FK)    │       │ order_id (FK)   │
│ user_order_number│      │ product_id (FK) │
│ total_amount    │       │ quantity        │
│ status          │       │ price           │
│ shipping_address│       │ created_at      │
│ phone           │       └─────────────────┘
│ payment_method  │
│ customer_name   │
│ note            │
│ created_at      │
│ updated_at      │
└─────────────────┘
```

---

## 2. Chi tiết các bảng

### 2.1. Bảng `users` (Người dùng)

| Cột | Kiểu dữ liệu | Ràng buộc | Mô tả |
|-----|--------------|-----------|-------|
| id | SERIAL | PRIMARY KEY | ID tự tăng |
| email | VARCHAR(255) | UNIQUE, NOT NULL | Email đăng nhập |
| password_hash | VARCHAR(255) | NOT NULL | Mật khẩu đã hash |
| full_name | VARCHAR(100) | NOT NULL | Họ và tên |
| phone | VARCHAR(20) | NULL | Số điện thoại |
| address | TEXT | NULL | Địa chỉ |
| role | VARCHAR(20) | DEFAULT 'customer' | Vai trò: 'customer', 'admin' |
| created_at | TIMESTAMP | DEFAULT NOW() | Ngày tạo |
| updated_at | TIMESTAMP | DEFAULT NOW() | Ngày cập nhật |

**Indexes:**
- `idx_users_email` ON email

---

### 2.2. Bảng `categories` (Danh mục)

| Cột | Kiểu dữ liệu | Ràng buộc | Mô tả |
|-----|--------------|-----------|-------|
| id | SERIAL | PRIMARY KEY | ID tự tăng |
| name | VARCHAR(100) | UNIQUE, NOT NULL | Tên danh mục |
| description | TEXT | NULL | Mô tả |
| image_url | VARCHAR(500) | NULL | Ảnh danh mục |
| created_at | TIMESTAMP | DEFAULT NOW() | Ngày tạo |
| updated_at | TIMESTAMP | DEFAULT NOW() | Ngày cập nhật |

---

### 2.3. Bảng `products` (Sản phẩm)

| Cột | Kiểu dữ liệu | Ràng buộc | Mô tả |
|-----|--------------|-----------|-------|
| id | SERIAL | PRIMARY KEY | ID tự tăng |
| name | VARCHAR(200) | NOT NULL | Tên sản phẩm |
| description | TEXT | NULL | Mô tả chi tiết |
| price | DECIMAL(12,2) | NOT NULL | Giá (VND) |
| stock | INTEGER | DEFAULT 0 | Số lượng tồn kho |
| image_url | VARCHAR(500) | NULL | URL ảnh sản phẩm |
| category_id | INTEGER | FOREIGN KEY | Liên kết danh mục |
| created_at | TIMESTAMP | DEFAULT NOW() | Ngày tạo |
| updated_at | TIMESTAMP | DEFAULT NOW() | Ngày cập nhật |

**Foreign Keys:**
- `fk_products_category` REFERENCES categories(id) ON DELETE SET NULL

**Indexes:**
- `idx_products_category` ON category_id
- `idx_products_name` ON name

---

### 2.4. Bảng `carts` (Giỏ hàng)

| Cột | Kiểu dữ liệu | Ràng buộc | Mô tả |
|-----|--------------|-----------|-------|
| id | SERIAL | PRIMARY KEY | ID tự tăng |
| user_id | INTEGER | FOREIGN KEY, UNIQUE | Mỗi user có 1 giỏ |
| created_at | TIMESTAMP | DEFAULT NOW() | Ngày tạo |
| updated_at | TIMESTAMP | DEFAULT NOW() | Ngày cập nhật |

**Foreign Keys:**
- `fk_carts_user` REFERENCES users(id) ON DELETE CASCADE

---

### 2.5. Bảng `cart_items` (Chi tiết giỏ hàng)

| Cột | Kiểu dữ liệu | Ràng buộc | Mô tả |
|-----|--------------|-----------|-------|
| id | SERIAL | PRIMARY KEY | ID tự tăng |
| cart_id | INTEGER | FOREIGN KEY | Liên kết giỏ hàng |
| product_id | INTEGER | FOREIGN KEY | Liên kết sản phẩm |
| quantity | INTEGER | NOT NULL, CHECK > 0 | Số lượng |
| created_at | TIMESTAMP | DEFAULT NOW() | Ngày thêm |

**Foreign Keys:**
- `fk_cart_items_cart` REFERENCES carts(id) ON DELETE CASCADE
- `fk_cart_items_product` REFERENCES products(id) ON DELETE CASCADE

**Unique Constraint:**
- (cart_id, product_id) - Mỗi sản phẩm chỉ có 1 dòng trong giỏ

---

### 2.6. Bảng `orders` (Đơn hàng)

| Cột | Kiểu dữ liệu | Ràng buộc | Mô tả |
|-----|--------------|-----------|-------|
| id | SERIAL | PRIMARY KEY | ID tự tăng |
| user_id | INTEGER | FOREIGN KEY | Người đặt hàng |
| user_order_number | INTEGER | NULL | Số thứ tự đơn theo từng user |
| total_amount | DECIMAL(12,2) | NOT NULL | Tổng tiền |
| status | VARCHAR(50) | DEFAULT 'confirmed' | Trạng thái |
| shipping_address | TEXT | NOT NULL | Địa chỉ giao hàng |
| phone | VARCHAR(20) | NOT NULL | SĐT nhận hàng |
| payment_method | VARCHAR(50) | DEFAULT 'cod' | Phương thức thanh toán |
| customer_name | VARCHAR(255) | NULL | Tên người nhận |
| note | TEXT | NULL | Ghi chú |
| created_at | TIMESTAMP | DEFAULT NOW() | Ngày đặt |
| updated_at | TIMESTAMP | DEFAULT NOW() | Ngày cập nhật |

**Trạng thái đơn hàng (status):**
- `confirmed` - Đã xác nhận
- `shipping` - Đang giao hàng
- `delivered` - Đã giao hàng
- `cancelled` - Đã hủy

**Phương thức thanh toán (payment_method):**
- `cod` - Thanh toán khi nhận hàng
- `bank_transfer` - Chuyển khoản ngân hàng
- `e_wallet` - Ví điện tử

**Foreign Keys:**
- `fk_orders_user` REFERENCES users(id) ON DELETE SET NULL

**Indexes:**
- `idx_orders_user` ON user_id
- `idx_orders_status` ON status

---

### 2.7. Bảng `order_items` (Chi tiết đơn hàng)

| Cột | Kiểu dữ liệu | Ràng buộc | Mô tả |
|-----|--------------|-----------|-------|
| id | SERIAL | PRIMARY KEY | ID tự tăng |
| order_id | INTEGER | FOREIGN KEY | Liên kết đơn hàng |
| product_id | INTEGER | FOREIGN KEY | Liên kết sản phẩm |
| quantity | INTEGER | NOT NULL | Số lượng |
| price | DECIMAL(12,2) | NOT NULL | Giá tại thời điểm đặt |
| created_at | TIMESTAMP | DEFAULT NOW() | Ngày tạo |

**Foreign Keys:**
- `fk_order_items_order` REFERENCES orders(id) ON DELETE CASCADE
- `fk_order_items_product` REFERENCES products(id) ON DELETE SET NULL

---

## 3. SQL Script tạo Database

```sql
-- Tạo database
CREATE DATABASE mini_shop;

-- Sử dụng database
\c mini_shop;

-- Bảng users
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    address TEXT,
    role VARCHAR(20) DEFAULT 'customer',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);

-- Bảng categories
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    image_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Bảng products
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    price DECIMAL(12, 2) NOT NULL,
    stock INTEGER DEFAULT 0,
    image_url VARCHAR(500),
    category_id INTEGER REFERENCES categories(id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_products_name ON products(name);

-- Bảng carts
CREATE TABLE carts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Bảng cart_items
CREATE TABLE cart_items (
    id SERIAL PRIMARY KEY,
    cart_id INTEGER REFERENCES carts(id) ON DELETE CASCADE,
    product_id INTEGER REFERENCES products(id) ON DELETE CASCADE,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(cart_id, product_id)
);

-- Bảng orders
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    user_order_number INTEGER,
    total_amount DECIMAL(12, 2) NOT NULL,
    status VARCHAR(50) DEFAULT 'confirmed',
    shipping_address TEXT NOT NULL,
    phone VARCHAR(20) NOT NULL,
    payment_method VARCHAR(50) NOT NULL DEFAULT 'cod',
    customer_name VARCHAR(255),
    note TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_orders_user ON orders(user_id);
CREATE INDEX idx_orders_status ON orders(status);

-- Bảng order_items
CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(id) ON DELETE CASCADE,
    product_id INTEGER REFERENCES products(id) ON DELETE SET NULL,
    quantity INTEGER NOT NULL,
    price DECIMAL(12, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Trigger cập nhật updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_categories_updated_at BEFORE UPDATE ON categories
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_products_updated_at BEFORE UPDATE ON products
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_carts_updated_at BEFORE UPDATE ON carts
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_orders_updated_at BEFORE UPDATE ON orders
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
```

---

## 4. Sample Data

```sql
-- Insert categories
INSERT INTO categories (name, description) VALUES
('Điện thoại', 'Điện thoại di động các loại'),
('Laptop', 'Máy tính xách tay'),
('Phụ kiện', 'Phụ kiện điện tử'),
('Tablet', 'Máy tính bảng');

-- Insert products
INSERT INTO products (name, description, price, stock, category_id) VALUES
('iPhone 15 Pro Max', 'iPhone 15 Pro Max 256GB Titan', 34990000, 50, 1),
('Samsung Galaxy S24 Ultra', 'Samsung Galaxy S24 Ultra 512GB', 32990000, 30, 1),
('MacBook Pro M3', 'MacBook Pro 14 inch M3 Pro', 49990000, 20, 2),
('Dell XPS 15', 'Dell XPS 15 Core i7 RTX 4060', 42990000, 15, 2),
('AirPods Pro 2', 'AirPods Pro 2nd Generation', 5990000, 100, 3),
('iPad Pro M4', 'iPad Pro 11 inch M4 256GB', 24990000, 25, 4);

-- Insert admin user (password: admin123)
INSERT INTO users (email, password_hash, full_name, role) VALUES
('admin@minishop.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.dVeP2mTqY6.h.G', 'Admin', 'admin');
```
