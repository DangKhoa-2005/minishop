# 📐 Class Diagram - Mini Shop

## 1. Tổng quan

Class Diagram mô tả cấu trúc các lớp (class) trong hệ thống Mini Shop, bao gồm các thuộc tính, phương thức và quan hệ giữa các lớp.

## 2. Class Diagram (PlantUML)

```plantuml
@startuml MiniShop Class Diagram

skinparam classAttributeIconSize 0
skinparam class {
    BackgroundColor #f8f9fa
    BorderColor #343a40
    ArrowColor #495057
}

' ==================== MODELS ====================

class User {
    - id : Integer <<PK>>
    - email : String(255) <<UNIQUE>>
    - password_hash : String(255)
    - full_name : String(100)
    - phone : String(20)
    - address : Text
    - role : String(20)
    - created_at : DateTime
    - updated_at : DateTime
    --
    + set_password(password: str) : void
    + check_password(password: str) : bool
    + is_admin() : bool
    + to_dict() : dict
}

class Category {
    - id : Integer <<PK>>
    - name : String(100) <<UNIQUE>>
    - description : Text
    - image_url : String(500)
    - created_at : DateTime
    - updated_at : DateTime
    --
    + to_dict(include_products: bool) : dict
}

class Product {
    - id : Integer <<PK>>
    - name : String(200)
    - description : Text
    - price : Numeric(12,2)
    - stock : Integer
    - image_url : String(500)
    - category_id : Integer <<FK>>
    - created_at : DateTime
    - updated_at : DateTime
    --
    + is_in_stock(quantity: int) : bool
    + reduce_stock(quantity: int) : bool
    + to_dict(include_category: bool) : dict
}

class Cart {
    - id : Integer <<PK>>
    - user_id : Integer <<FK, UNIQUE>>
    - created_at : DateTime
    - updated_at : DateTime
    --
    + get_total() : float
    + get_item_count() : int
    + clear() : void
    + to_dict() : dict
}

class CartItem {
    - id : Integer <<PK>>
    - cart_id : Integer <<FK>>
    - product_id : Integer <<FK>>
    - quantity : Integer
    - created_at : DateTime
    --
    + get_subtotal() : float
    + to_dict() : dict
}

class Order {
    - id : Integer <<PK>>
    - user_id : Integer <<FK>>
    - user_order_number : Integer
    - total_amount : Numeric(12,2)
    - status : String(50)
    - shipping_address : Text
    - phone : String(20)
    - payment_method : String(50)
    - customer_name : String(255)
    - note : Text
    - created_at : DateTime
    - updated_at : DateTime
    --
    + {static} STATUS_CONFIRMED : str = "confirmed"
    + {static} STATUS_SHIPPING : str = "shipping"
    + {static} STATUS_DELIVERED : str = "delivered"
    + {static} STATUS_CANCELLED : str = "cancelled"
    + {static} PAYMENT_METHOD_COD : str = "cod"
    + {static} PAYMENT_METHOD_BANK_TRANSFER : str = "bank_transfer"
    + {static} PAYMENT_METHOD_E_WALLET : str = "e_wallet"
    --
    + get_status_display() : str
    + get_payment_method_display() : str
    + can_cancel() : bool
    + to_dict(include_items: bool) : dict
}

class OrderItem {
    - id : Integer <<PK>>
    - order_id : Integer <<FK>>
    - product_id : Integer <<FK>>
    - quantity : Integer
    - price : Numeric(12,2)
    - created_at : DateTime
    --
    + get_subtotal() : float
    + to_dict() : dict
}

' ==================== RELATIONSHIPS ====================

User "1" -- "0..1" Cart : has >
User "1" -- "0..*" Order : places >

Category "1" -- "0..*" Product : contains >

Cart "1" -- "0..*" CartItem : has >
CartItem "0..*" -- "1" Product : references >

Order "1" -- "1..*" OrderItem : contains >
OrderItem "0..*" -- "1" Product : references >

@enduml
```

## 3. Mô tả chi tiết

### 3.1. Quan hệ giữa các class

| Quan hệ | Loại | Mô tả |
|---------|------|-------|
| User → Cart | 1:1 | Mỗi user có 1 giỏ hàng |
| User → Order | 1:N | Mỗi user có nhiều đơn hàng |
| Category → Product | 1:N | Mỗi danh mục có nhiều sản phẩm |
| Cart → CartItem | 1:N | Giỏ hàng chứa nhiều mục |
| CartItem → Product | N:1 | Mỗi mục giỏ hàng tham chiếu 1 sản phẩm |
| Order → OrderItem | 1:N | Đơn hàng chứa nhiều sản phẩm |
| OrderItem → Product | N:1 | Mỗi mục đơn hàng tham chiếu 1 sản phẩm |

### 3.2. Design Patterns sử dụng

| Pattern | Áp dụng | Mô tả |
|---------|---------|-------|
| **Factory Pattern** | `create_app()` | Flask Application Factory |
| **Repository Pattern** | SQLAlchemy Models | Truy xuất dữ liệu qua ORM |
| **Blueprint Pattern** | Flask Blueprints | Tổ chức routes theo module |
| **DTO Pattern** | `to_dict()` methods | Chuyển đổi model → JSON |
| **Decorator Pattern** | `@jwt_required`, `@admin_required` | Xác thực và phân quyền |

### 3.3. Bảng tổng hợp Classes

| Class | Thuộc tính | Phương thức | Vai trò |
|-------|-----------|-------------|---------|
| User | 9 | 4 | Quản lý người dùng & xác thực |
| Category | 6 | 1 | Phân loại sản phẩm |
| Product | 9 | 3 | Quản lý sản phẩm |
| Cart | 4 | 4 | Giỏ hàng người dùng |
| CartItem | 5 | 2 | Mục trong giỏ hàng |
| Order | 12 | 4 | Đơn đặt hàng |
| OrderItem | 6 | 2 | Mục trong đơn hàng |

## 4. Sơ đồ ASCII

```
┌──────────────────────┐
│        User          │
├──────────────────────┤
│ - id: Integer        │
│ - email: String      │        ┌──────────────────────┐
│ - password_hash: Str │        │      Category        │
│ - full_name: String  │        ├──────────────────────┤
│ - phone: String      │        │ - id: Integer        │
│ - address: Text      │        │ - name: String       │
│ - role: String       │        │ - description: Text  │
├──────────────────────┤        │ - image_url: String  │
│ + set_password()     │        ├──────────────────────┤
│ + check_password()   │        │ + to_dict()          │
│ + is_admin()         │        └──────────┬───────────┘
│ + to_dict()          │                   │ 1:N
└──┬────────────┬──────┘                   ▼
   │ 1:1        │ 1:N          ┌──────────────────────┐
   ▼            ▼              │      Product         │
┌────────┐  ┌────────────┐    ├──────────────────────┤
│  Cart  │  │   Order    │    │ - id: Integer        │
├────────┤  ├────────────┤    │ - name: String       │
│ - id   │  │ - id       │    │ - price: Numeric     │
│ - uid  │  │ - uid      │    │ - stock: Integer     │
├────────┤  │ - status   │    │ - category_id: FK    │
│+total()│  │ - total    │    ├──────────────────────┤
│+clear()│  │ - payment  │    │ + is_in_stock()      │
│+to_dict│  ├────────────┤    │ + reduce_stock()     │
└──┬─────┘  │+can_cancel │    │ + to_dict()          │
    │ 1:N    │+to_dict()  │    └──────────────────────┘
    ▼        └──┬─────────┘
┌────────┐     │ 1:N                    ▲
│CartItem│     ▼                        │ N:1
├────────┤  ┌────────────┐              │
│- cart  │  │ OrderItem  │──────────────┘
│- prod  │  ├────────────┤
│- qty   │  │ - order_id │
├────────┤  │ - prod_id  │
│+sub()  │  │ - quantity │
└────────┘  │ - price    │
            └────────────┘
```
