# Hướng dẫn chạy dự án Mini Shop từng bước (Step-by-step)

Chào bạn, để chạy dự án **Mini Shop Clean** trên máy tính của bạn, bạn có thể chọn 1 trong 2 cách sau: **Sử dụng Docker (Cách dễ nhất)** hoặc **Chạy thủ công từng phần (Backend riêng, Frontend riêng)**.

---

## Cách 1: Chạy bằng Docker Compose (Khuyên dùng)

Cách này rất nhanh gọn nếu máy bạn đã cài sẵn **Docker** và **Docker Compose**.

**Bước 1:** Đảm bảo bạn đang đứng ở thư mục gốc của dự án (`mini-shop-clean`).

**Bước 2:** Chạy lệnh sau để build và khởi động tất cả các container (Backend, Frontend, Database, v.v.):
```bash
docker-compose up --build
```
*(Lưu ý: Bạn cũng có thể dùng file cấu hình trong thư mục deploy bằng lệnh `docker-compose -f deploy/docker-compose.clean.yml up -d`)*

**Bước 3:** Chờ một lát để quá trình cài đặt hoàn tất. Sau đó bạn có thể truy cập:
- Frontend (Giao diện web): [http://localhost:8081](http://localhost:8081)
- Backend API: [http://localhost:5002](http://localhost:5002)

---

## Cách 2: Chạy thủ công (Manual Setup)

Nếu bạn không dùng Docker, hãy làm theo các bước dưới đây để chạy Server (Backend) và Web (Frontend) độc lập.

### Phần A: Chạy Backend (Flask / Python)

**Bước 1: Mở terminal và di chuyển vào thư mục backend**
```bash
cd backend
```

**Bước 2: (Tuỳ chọn nhưng khuyên dùng) Tạo môi trường ảo (Virtual Environment)**
```bash
python -m venv venv
```
Kích hoạt môi trường ảo:
- Trên Windows: `venv\Scripts\activate`
- Trên Mac/Linux: `source venv/bin/activate`

**Bước 3: Cài đặt các thư viện cần thiết**
```bash
pip install -r requirements.txt
```

**Bước 4: Cấu hình biến môi trường**
- Tại thư mục `backend`, copy file `.env.example` thành file `.env` (hoặc đổi tên).
- Mở file `.env` lên và điền các thông số cần thiết (như JWT_SECRET_KEY, OPENAI_API_KEY nếu có chức năng chatbot).

**Bước 5: Khởi tạo Database và dữ liệu mẫu**
```bash
python seed.py
```
*(Lệnh này sẽ tạo database SQLite và nạp một số dữ liệu ban đầu cho danh mục, sản phẩm, users...)*

Tuỳ thuộc vào dự án, bạn cũng có thể cần chạy migration:
```bash
flask db upgrade
```

**Bước 6: Khởi động Server API**
```bash
python run.py
```
-> Lúc này Backend của bạn đã chạy thành công tại địa chỉ `http://localhost:5000`. Hãy giữ terminal này luôn mở.

---

### Phần B: Chạy Frontend (React / Vite)

**Bước 1: Mở một terminal mới và di chuyển vào thư mục frontend**
```bash
cd frontend
```

**Bước 2: Cài đặt các thư viện (Node Modules)**
Đảm bảo máy bạn đã cài NodeJS. Chạy lệnh:
```bash
npm install
```

**Bước 3: Cấu hình URL kết nối tới Backend**
- Tại thư mục `frontend`, copy file `.env.example` thành `.env`.
- Cấu hình biến môi trường trỏ tới domain của Backend (ví dụ `VITE_API_URL=http://localhost:5000/api`).

**Bước 4: Khởi động giao diện Web**
```bash
npm run dev
```
-> Web của bạn sẽ chạy lên (thường tại `http://localhost:5173`). Bạn có thể mở link này trên trình duyệt để sử dụng hệ thống.

---

### Tóm tắt tài khoản Test mặc định (Nếu file seed.py có tạo)
- **Admin**: `admin@minishop.com` / `admin123`
- **Khách hàng**: `user@minishop.com` / `user123`
*(Bạn có thể xem chi tiết trong file `backend/seed.py` để lấy account test)*

Chúc bạn chạy dự án thành công!
