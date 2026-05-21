# Demo Info - Mini Shop

## 1. Local demo URLs

- Frontend: http://localhost:8080
- Backend health: http://localhost:5001/api/health

Neu chay compose mac dinh:

- Frontend: http://localhost
- Backend: http://localhost:5000

## 2. Tai khoan demo

| Email | Password | Role |
|-------|----------|------|
| admin@minishop.com | admin123 | admin |
| customer@example.com | 123456 | customer |

## 3. Demo script (goi y)

1. Dang nhap customer.
2. Them san pham vao gio.
3. Checkout voi 1 trong 3 payment method (cod/bank_transfer/e_wallet).
4. Mo chi tiet don, kiem tra thong tin payment_method.
5. Dang xuat, dang nhap admin.
6. Vao dashboard xem thong ke.
7. Vao quan ly don, cap nhat trang thai sang shipping/delivered.

## 4. Luu y cho buoi bao ve

- Luong trang thai hien tai: confirmed -> shipping -> delivered/cancelled.
- Admin UI hien tai tap trung vao order operations + stats.
- Trong demo hien tai, don hang do tai khoan admin quan ly truc tiep.
- CRUD product/category/user da co API, chua co trang admin UI rieng.
