# Testing Evidence - Mini Shop

## 1. Tong quan

- Backend tests: 41 test case (pytest).
- E2E tests: 2 test case (Playwright).
- Muc tieu: xac thuc cac luong chinh auth, cart, checkout, order, admin.

## 2. Backend tests

- Thu muc: `backend/tests/`
- Files:
  - `test_basic.py`
  - `test_models_api.py`
  - `test_checkout_name.py`

Chay test:

```bash
cd backend
pytest -q
```

Nhom testcase chinh:

- Model behavior: User, Product, Order, Category.
- Auth API: register, login, me.
- Product/Category API: list, detail, filter, search.
- Cart API: add/get/remove.
- Order API: checkout, cancel, list/detail, admin status/update/stats.
- Rule checks: admin khong checkout; don moi mac dinh confirmed; can cancel chi khi confirmed.

## 3. E2E tests

- Thu muc: `tests/e2e/`
- Files:
  - `login.spec.js`
  - `checkout.spec.js`

Chay test:

```bash
cd tests/e2e
npm install
npx playwright test
```

Luot test:

- `admin can login`
- `customer can checkout with explicit name and see it in order detail`

## 4. Ket qua mong doi de dua vao bao cao

- Tat ca backend tests pass.
- E2E login va checkout pass.
- Neu moi truong docker khong co pytest, co the dung smoke test API de chung minh flow checkout + payment_method.
