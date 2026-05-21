# Project Proposal

## THÔNG TIN

### Nhóm

- Thành viên 1: 23703471 - Huỳnh Đăng Khoa
- Thành viên 2: 2370351 - Mai Văn Quân
- Thành viên 3: 23707921 - Bùi Quang Tuyến
- Thành viên 4: 23718591 - Nguyễn Hoàng Nam

### Git

Git repository: 

## MÔ TẢ DỰ ÁN

### Ý tưởng

Mini Shop là hệ thống thương mại điện tử (E-Commerce) đơn giản dành cho các cửa hàng công nghệ nhỏ. Ý tưởng xuất phát từ nhu cầu xây dựng một nền tảng bán hàng online hoàn chỉnh với đầy đủ quy trình: duyệt sản phẩm → thêm giỏ hàng → thanh toán → theo dõi đơn hàng.

**Tại sao chọn project này?**
- Thương mại điện tử là lĩnh vực thực tế, phổ biến, giúp rèn luyện nhiều kỹ năng fullstack.
- Bao gồm đầy đủ các nghiệp vụ: authentication, authorization, CRUD, state management, real-time interaction (chatbot).
- Project có thể mở rộng và ứng dụng thực tế.

**Điểm khác biệt:**
- Tích hợp AI Chatbot (OpenAI API) để tư vấn sản phẩm cho khách hàng — không chỉ là một trang bán hàng tĩnh.
- Triển khai CI/CD hoàn chỉnh với Docker + GitHub Actions.

### Chi tiết

**Nghiệp vụ hệ thống:**

1. **Quản lý tài khoản:** Người dùng đăng ký, đăng nhập. Hệ thống phân quyền thành 2 vai trò: Customer (khách hàng) và Admin (quản trị viên). Customer có thể cập nhật thông tin cá nhân, đổi mật khẩu.

2. **Duyệt & tìm kiếm sản phẩm:** Khách (kể cả chưa đăng nhập) có thể xem danh sách sản phẩm, tìm kiếm theo tên, lọc theo danh mục, xem chi tiết từng sản phẩm (mô tả, giá, tồn kho, danh mục).

3. **Giỏ hàng:** Customer thêm sản phẩm vào giỏ, cập nhật số lượng, xóa sản phẩm khỏi giỏ. Mỗi user có một giỏ hàng riêng (1-1).

4. **Đặt hàng (Checkout):** Customer điền thông tin giao hàng (tên, SĐT, địa chỉ, ghi chú) → hệ thống tạo đơn hàng từ giỏ → trừ tồn kho → xóa giỏ hàng. Mỗi đơn hàng có mã số riêng theo user (user_order_number).

5. **Quản lý đơn hàng:**
   - Customer: xem lịch sử đơn, chi tiết đơn, hủy đơn (nếu chưa giao), xác nhận đã nhận hàng.
        - Admin: xem tất cả đơn, cập nhật trạng thái (confirmed → shipping → delivered → cancelled), xem thống kê.

6. **Quản lý sản phẩm & danh mục (Admin):** Backend API đã có CRUD sản phẩm/danh mục; hiện frontend chưa có màn hình quản trị riêng cho phần này.

7. **Chatbot AI:** Khách hàng chat với AI chatbot (OpenAI) để được tư vấn sản phẩm dựa trên dữ liệu sản phẩm thực tế trong hệ thống.

8. **Thống kê (Admin):** Tổng đơn hàng, doanh thu, đơn theo trạng thái.

## PHÂN TÍCH & THIẾT KẾ

### 1. Actors & Use Cases

| Actor | Mô tả |
|-------|-------|
| **Guest** | Người dùng chưa đăng nhập |
| **Customer** | Khách hàng đã đăng nhập |
| **Admin** | Quản trị viên hệ thống |

**Use Cases chính:**

| # | Use Case | Actor | Mô tả |
|---|----------|-------|-------|
| UC01 | Xem danh sách sản phẩm | Guest, Customer | Duyệt sản phẩm với pagination, tìm kiếm, lọc danh mục |
| UC02 | Xem chi tiết sản phẩm | Guest, Customer | Xem đầy đủ thông tin sản phẩm |
| UC03 | Tìm kiếm sản phẩm | Guest, Customer | Tìm theo tên sản phẩm |
| UC04 | Lọc theo danh mục | Guest, Customer | Lọc sản phẩm theo danh mục |
| UC05 | Đăng ký tài khoản | Guest | Tạo tài khoản mới (email, mật khẩu, họ tên) |
| UC06 | Đăng nhập | Guest | Xác thực bằng email + mật khẩu → JWT |
| UC07 | Thêm vào giỏ hàng | Customer | Thêm sản phẩm với số lượng vào giỏ |
| UC08 | Xem giỏ hàng | Customer | Xem danh sách sản phẩm trong giỏ |
| UC09 | Cập nhật giỏ hàng | Customer | Thay đổi số lượng sản phẩm trong giỏ |
| UC10 | Xóa khỏi giỏ | Customer | Xóa sản phẩm khỏi giỏ hàng |
| UC11 | Đặt hàng (Checkout) | Customer | Tạo đơn hàng từ giỏ hàng |
| UC12 | Xem lịch sử đơn hàng | Customer | Danh sách đơn hàng đã đặt |
| UC13 | Xem chi tiết đơn hàng | Customer | Thông tin chi tiết 1 đơn hàng |
| UC14 | Hủy đơn hàng | Customer | Hủy đơn (nếu chưa giao) |
| UC15 | Xác nhận nhận hàng | Customer | Xác nhận đã nhận đơn hàng |
| UC16 | Cập nhật thông tin cá nhân | Customer | Sửa họ tên, SĐT, địa chỉ |
| UC17 | Chat với AI chatbot | Customer | Tư vấn sản phẩm qua OpenAI |
| UC18 | Đăng xuất | Customer | Xóa session đăng nhập |
| UC19 | Quản lý đơn hàng | Admin | Xem tất cả đơn, cập nhật trạng thái |
| UC20 | Xem thống kê | Admin | Thống kê doanh thu, số đơn hàng |

### 2. Database Schema (ERD)

**7 bảng chính:**

| Entity | Columns | Quan hệ |
|--------|---------|---------|
| **User** | id, email (UNIQUE), password_hash, full_name, phone, address, role, created_at, updated_at | 1-1 Cart, 1-N Order |
| **Category** | id, name (UNIQUE), description, image_url, created_at, updated_at | 1-N Product |
| **Product** | id, name, description, price, stock, image_url, category_id (FK), created_at, updated_at | N-1 Category, 1-N CartItem, 1-N OrderItem |
| **Cart** | id, user_id (FK, UNIQUE), created_at, updated_at | 1-1 User, 1-N CartItem |
| **CartItem** | id, cart_id (FK), product_id (FK), quantity | N-1 Cart, N-1 Product |
| **Order** | id, user_id (FK), user_order_number, total_amount, status, shipping_address, phone, customer_name, note, created_at, updated_at | N-1 User, 1-N OrderItem |
| **OrderItem** | id, order_id (FK), product_id (FK), quantity, price | N-1 Order, N-1 Product |

### 3. Kiến trúc hệ thống

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Frontend      │────▶|   Backend       │────▶│   Database      │
│   React + Vite  │     │   Flask API     │     │   SQLite / PG   │
└─────────────────┘     └─────────────────┘     └─────────────────┘
        │                       │
        └───────────────▶ AI Chatbot (OpenAI API)
```

- **Frontend:** React 18 + Vite 5 + TailwindCSS + Zustand (state) + React Router 6
- **Backend:** Python Flask 3.0 + SQLAlchemy ORM + Flask-Migrate + JWT Auth
- **Database:** SQLite (dev) / PostgreSQL (production)
- **DevOps:** Docker + Docker Compose + GitHub Actions CI/CD

### 4. Thiết kế giao diện (Wireframe)

Hệ thống gồm **16 trang**:

| # | Trang | Mô tả |
|---|-------|-------|
| 1 | HomePage | Trang chủ: banner, danh mục, sản phẩm nổi bật |
| 2 | ProductsPage | Danh sách sản phẩm (pagination, filter, search) |
| 3 | ProductDetailPage | Chi tiết sản phẩm + thêm vào giỏ |
| 4 | LoginPage | Đăng nhập |
| 5 | RegisterPage | Đăng ký tài khoản |
| 6 | CartPage | Giỏ hàng |
| 7 | CheckoutPage | Thanh toán (điền thông tin giao hàng) |
| 8 | OrdersPage | Lịch sử đơn hàng |
| 9 | OrderDetailPage | Chi tiết đơn hàng |
| 10 | ProfilePage | Thông tin cá nhân |
| 11 | AdminOrdersPage | Quản lý đơn hàng (Admin) |
| 12 | AdminShippedPage | Lịch sử giao hàng (Admin) |
| 13 | ContactPage | Trang liên hệ |
| 14 | GuidePage | Hướng dẫn mua hàng |
| 15 | ReturnPolicyPage | Chính sách đổi trả |
| 16 | WarrantyPolicyPage | Chính sách bảo hành |

### 5. API Endpoints

| Nhóm | Method | Endpoint | Mô tả |
|------|--------|----------|-------|
| Auth | POST | /api/auth/register | Đăng ký |
| Auth | POST | /api/auth/login | Đăng nhập → JWT |
| Users | GET | /api/users/profile | Lấy thông tin user |
| Users | PUT | /api/users/profile | Cập nhật thông tin |
| Products | GET | /api/products/ | Danh sách (pagination, search, filter) |
| Products | GET | /api/products/:id | Chi tiết |
| Products | POST | /api/products/ | Thêm (Admin) |
| Products | PUT | /api/products/:id | Sửa (Admin) |
| Products | DELETE | /api/products/:id | Xóa (Admin) |
| Categories | GET | /api/categories/ | Danh sách danh mục |
| Categories | POST | /api/categories/ | Thêm (Admin) |
| Categories | PUT | /api/categories/:id | Sửa (Admin) |
| Categories | DELETE | /api/categories/:id | Xóa (Admin) |
| Cart | GET | /api/cart/ | Xem giỏ hàng |
| Cart | POST | /api/cart/add | Thêm vào giỏ |
| Cart | DELETE | /api/cart/remove/:id | Xóa khỏi giỏ |
| Orders | GET | /api/orders/ | Đơn hàng của user |
| Orders | GET | /api/orders/:id | Chi tiết đơn |
| Orders | POST | /api/orders/checkout | Đặt hàng |
| Orders | POST | /api/orders/:id/cancel | Hủy đơn |
| Orders | POST | /api/orders/:id/confirm-delivery | Xác nhận nhận hàng |
| Orders | GET | /api/orders/admin/all | Tất cả đơn (Admin) |
| Orders | PUT | /api/orders/admin/:id/status | Cập nhật trạng thái (Admin) |
| Orders | GET | /api/orders/admin/stats | Thống kê (Admin) |
| Chatbot | POST | /api/chatbot/chat | Chat AI tư vấn |

*Ghi chú: Một số endpoint Admin (CRUD sản phẩm/danh mục, quản lý user) đang sẵn sàng ở backend API, nhưng chưa có màn hình quản trị riêng trên frontend hiện tại.*

### 6. Tech Stack

| Layer | Công nghệ |
|-------|-----------|
| Frontend | React 18, Vite 5, TailwindCSS, Zustand, React Router 6 |
| Backend | Python 3.11+, Flask 3.0, SQLAlchemy, Flask-Migrate |
| Database | SQLite (dev) / PostgreSQL 15 (prod) |
| Auth | JWT (Flask-JWT-Extended) |
| DevOps | Docker, Docker Compose, GitHub Actions CI/CD |
| Innovation | OpenAI API — Chatbot tư vấn sản phẩm |
| Testing | Pytest (unit), Playwright (E2E) |

## KẾ HOẠCH

### MVP

**Chức năng MVP (Hoàn thành trước 12.04.2026):**

1. ✅ Authentication: Đăng ký, đăng nhập, phân quyền (Customer/Admin)
2. ✅ API quản lý sản phẩm: CRUD sản phẩm + danh mục (Admin)
3. ✅ Duyệt sản phẩm: Xem, tìm kiếm, lọc danh mục (Guest/Customer)
4. ✅ Giỏ hàng: Thêm, sửa, xóa sản phẩm trong giỏ
5. ✅ Đặt hàng: Checkout từ giỏ hàng → tạo đơn
6. ✅ Xem đơn hàng: Lịch sử đơn, chi tiết đơn
7. ✅ Quản lý đơn hàng (Admin): Cập nhật trạng thái
8. ✅ Hồ sơ cá nhân: Xem, cập nhật thông tin

**Kế hoạch kiểm thử MVP:**

| Loại test | Công cụ | Phạm vi |
|-----------|---------|---------|
| Unit test | Pytest | Models (User, Product, Category, Cart, Order), API endpoints |
| E2E test | Playwright | Login flow, Checkout flow |
| Manual test | Browser | Toàn bộ UI flows |

**Chức năng dự trù phase tiếp theo:**
- AI Chatbot tư vấn sản phẩm
- Hủy đơn hàng, xác nhận nhận hàng
- Docker deployment + CI/CD
- Trang thông tin (Liên hệ, Hướng dẫn, Chính sách)

### Beta Version

**Kết quả kiểm thử:**

| Loại | Số test | Kết quả |
|------|---------|---------|
| Unit test (Pytest) | 40+ tests | ✅ All passed |
| E2E test (Playwright) | 2 specs (login, checkout) | ✅ All passed |
| API test | 25 endpoints | ✅ All functional |

**Tính năng đã hoàn thành (Beta):**

- ✅ Toàn bộ MVP features
- ✅ AI Chatbot tư vấn sản phẩm (OpenAI API)
- ✅ Hủy đơn, xác nhận nhận hàng (Customer)
- ✅ Docker + Docker Compose deployment
- ✅ GitHub Actions CI/CD pipeline
- ✅ 6 trang thông tin phụ (Contact, Guide, Return Policy, Warranty Policy)
- ✅ Tài liệu thiết kế đầy đủ (Use Case, Class Diagram, DB Schema, Wireframe, Deployment)

**Thời hạn hoàn thành:** 

## CÂU HỎI

- (Không có câu hỏi)

---
