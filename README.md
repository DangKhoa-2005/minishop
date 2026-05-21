# Mini Shop - E-Commerce Platform

## Thông tin dự án

**Đề tài:** Hệ thống E-Commerce đơn giản  
**Môn học:** Application Development  
**Nhóm:** 4 thành viên

---

## Mô tả

Mini Shop là một nền tảng thương mại điện tử cho phép:

**Khách hàng:**
- Đăng ký, đăng nhập tài khoản
- Xem danh sách sản phẩm, tìm kiếm, lọc theo danh mục
- Thêm sản phẩm vào giỏ hàng, đặt hàng (COD/chuyển khoản/ví điện tử)
- Theo dõi đơn hàng, xác nhận đã nhận hàng
- Chat với AI chatbot để được tư vấn sản phẩm

**Admin:**
- UI hiện có: Dashboard thống kê, Quản lý đơn hàng, Lịch sử giao hàng
- API hiện có: CRUD sản phẩm, CRUD danh mục, quản lý user

### Phạm vi triển khai hiện tại (04/2026)

| Hạng mục | Trạng thái |
|----------|------------|
| Guest/Customer flow | Hoàn thiện UI + API |
| Admin Orders/Stats flow | Hoàn thiện UI + API |
| Admin Product/Category/User management | Có API, chưa có trang UI quản trị riêng |

---

## Kiến trúc hệ thống

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Frontend      │────▶│   Backend       │────▶│   Database      │
│   React + Vite  │     │   Flask API     │     │   SQLite / PG   │
└─────────────────┘     └─────────────────┘     └─────────────────┘
        │                       │
        └───────────────▶ AI Chatbot (OpenAI API)
```

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| **Frontend** | React 18, Vite 5, TailwindCSS, Zustand, React Router 6 |
| **Backend** | Python 3.11+, Flask 3.0, SQLAlchemy, Flask-Migrate |
| **Database** | SQLite (dev) / PostgreSQL 15 (production) |
| **Authentication** | JWT (Flask-JWT-Extended) |
| **State Management** | Zustand |
| **DevOps** | Docker, Docker Compose, GitHub Actions CI/CD |
| **Innovation** | OpenAI API — Chatbot tư vấn sản phẩm |

---

## Cấu trúc thư mục

```
mini-shop-clean/
├── backend/                   # Flask API server
│   ├── app/
│   │   ├── __init__.py        # Flask factory (create_app)
│   │   ├── models/            # SQLAlchemy models
│   │   │   ├── user.py
│   │   │   ├── product.py
│   │   │   ├── category.py
│   │   │   ├── cart.py
│   │   │   └── order.py
│   │   └── routes/            # API blueprints
│   │       ├── auth.py
│   │       ├── products.py
│   │       ├── categories.py
│   │       ├── cart.py
│   │       ├── orders.py
│   │       ├── users.py
│   │       └── chatbot.py
│   ├── tests/                 # Unit tests (pytest)
│   ├── migrations/            # Alembic migrations
│   ├── config.py              # Flask config
│   ├── run.py                 # Dev entry point
│   ├── wsgi.py                # Production WSGI entry
│   ├── seed.py                # Database seeder
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/                  # React SPA
│   ├── src/
│   │   ├── components/        # Reusable UI (Header, Footer, Chatbot, ...)
│   │   ├── pages/             # Page components (17 pages)
│   │   ├── services/          # Axios API client
│   │   └── store/             # Zustand state management
│   ├── vite.config.js
│   ├── tailwind.config.js
│   ├── Dockerfile
│   └── package.json
│
├── docs/                      # Tài liệu phân tích & thiết kế
│   ├── use-case-diagram.md
│   ├── class-diagram.md
│   ├── database-schema.md
│   ├── wireframe.md
│   └── deployment.md
│
├── deploy/                    # Deployment configs
│   ├── docker-compose.clean.yml
│   └── Makefile
│
├── tests/e2e/                 # End-to-end tests (Playwright)
│   ├── login.spec.js
│   └── checkout.spec.js
│
├── .github/workflows/ci.yml  # CI/CD pipeline
├── docker-compose.yml         # Docker Compose (chính)
└── README.md
```

---

## Phân chia công việc

| Thành viên | Vai trò | Công việc |
|------------|---------|-----------|
| **#1** | Backend Developer | User Authentication, Profile Management |
| **#2** | Backend Developer | Product Management, Category, Search |
| **#3** | Frontend Developer | UI/UX, React Components, State Management |
| **#4** | DevOps + AI | Docker, CI/CD, Chatbot AI Integration |

---

## Hướng dẫn cài đặt

### Yêu cầu
- Python 3.11+
- Node.js 18+
- Docker & Docker Compose (nếu chạy bằng Docker)

### Cách 1: Chạy với Docker (Khuyến nghị)
```bash
docker-compose up --build
```

Hoặc dùng bản clean (cổng riêng, không conflict):
```bash
docker-compose -f deploy/docker-compose.clean.yml up --build
```

### Cách 2: Chạy thủ công

**Backend:**
```bash
cd backend
pip install -r requirements.txt
python seed.py          # Tạo dữ liệu mẫu
python run.py           # Chạy server → http://localhost:5000
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev             # Chạy dev server → http://localhost:5173
```

### Tài khoản mẫu (sau khi seed)

| Email | Mật khẩu | Vai trò |
|-------|-----------|---------|
| `admin@minishop.com` | `admin123` | Admin |
| `customer@example.com` | `123456` | Customer |

---

## Database Schema

| Entity | Columns |
|--------|---------|
| **User** | id, email, password_hash, full_name, phone, address, role, created_at, updated_at |
| **Category** | id, name, description, image_url, created_at, updated_at |
| **Product** | id, name, description, price, stock, image_url, category_id (FK), created_at, updated_at |
| **Cart** | id, user_id (FK, unique), created_at, updated_at |
| **CartItem** | id, cart_id (FK), product_id (FK), quantity |
| **Order** | id, user_id (FK), user_order_number, total_amount, status, shipping_address, phone, payment_method, customer_name, note, created_at, updated_at |
| **OrderItem** | id, order_id (FK), product_id (FK), quantity, price |

Chi tiết: xem [docs/database-schema.md](docs/database-schema.md)

---

## API Endpoints

### Auth (`/api/auth`)
| Method | Endpoint | Mô tả |
|--------|----------|-------|
| POST | `/register` | Đăng ký tài khoản |
| POST | `/login` | Đăng nhập, trả về JWT |

### Users (`/api/users`)
| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET | `/profile` | Lấy thông tin user (JWT) |
| PUT | `/profile` | Cập nhật thông tin user (JWT) |

### Products (`/api/products`)
| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET | `/` | Danh sách sản phẩm (pagination, search, filter) |
| GET | `/:id` | Chi tiết sản phẩm |
| POST | `/` | Thêm sản phẩm (Admin) |
| PUT | `/:id` | Sửa sản phẩm (Admin) |
| DELETE | `/:id` | Xóa sản phẩm (Admin) |

### Categories (`/api/categories`)
| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET | `/` | Danh sách danh mục |
| GET | `/:id` | Chi tiết danh mục |
| POST | `/` | Thêm danh mục (Admin) |
| PUT | `/:id` | Sửa danh mục (Admin) |
| DELETE | `/:id` | Xóa danh mục (Admin) |

### Cart (`/api/cart`)
| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET | `/` | Xem giỏ hàng (JWT) |
| POST | `/add` | Thêm sản phẩm vào giỏ (JWT) |
| DELETE | `/remove/:id` | Xóa khỏi giỏ (JWT) |

### Orders (`/api/orders`)
| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET | `/` | Danh sách đơn hàng của user (JWT) |
| GET | `/:id` | Chi tiết đơn hàng (JWT) |
| POST | `/checkout` | Tạo đơn hàng từ giỏ (JWT) |
| POST | `/:id/cancel` | Hủy đơn hàng (JWT) |
| POST | `/:id/confirm-delivery` | Xác nhận đã nhận hàng (JWT) |
| GET | `/admin/all` | Tất cả đơn hàng (Admin) |
| PUT | `/admin/:id/status` | Cập nhật trạng thái (Admin) |
| GET | `/admin/stats` | Thống kê đơn hàng (Admin) |

### Chatbot (`/api/chatbot`)
| Method | Endpoint | Mô tả |
|--------|----------|-------|
| POST | `/chat` | Chat với AI tư vấn sản phẩm |

---

## Tài liệu thiết kế

| Tài liệu | File |
|-----------|------|
| Use Case Diagram | [docs/use-case-diagram.md](docs/use-case-diagram.md) |
| Class Diagram | [docs/class-diagram.md](docs/class-diagram.md) |
| Database Schema | [docs/database-schema.md](docs/database-schema.md) |
| Wireframe | [docs/wireframe.md](docs/wireframe.md) |
| Deployment Guide | [docs/deployment.md](docs/deployment.md) |
| Testing Evidence | [docs/testing-evidence.md](docs/testing-evidence.md) |
| Demo Info | [docs/demo-info.md](docs/demo-info.md) |
| AI Usage Log | [docs/ai-usage-log.md](docs/ai-usage-log.md) |
| References | [docs/references.md](docs/references.md) |
| Submission Assets Checklist | [docs/submission-assets-checklist.md](docs/submission-assets-checklist.md) |

---

## Checklist tiêu chí đánh giá

- [x] **Analysis & Design** — Use Case, Wireframe, Database Schema, Class Diagram
- [x] **Implementation** — Flask + React, 41 backend tests, 2 E2E tests
- [x] **Teamwork** — Git workflow, commit history
- [ ] **Presentation** — đang hoàn thiện báo cáo cuối kỳ
- [x] **Deployment** — Docker, Docker Compose, GitHub Actions CI/CD
- [x] **Innovation** — AI Chatbot tư vấn sản phẩm (OpenAI)

---

## License

MIT License
