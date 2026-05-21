const { test, expect } = require('@playwright/test');

test('customer can checkout with explicit name and see it in order detail', async ({ page }) => {
  // Login via API to get token
  const loginResp = await page.request.post('/api/auth/login', {
    data: { email: 'customer@example.com', password: '123456' }
  });
  expect(loginResp.ok()).toBeTruthy();
  const loginBody = await loginResp.json();
  const token = loginBody.data.access_token;
  // Add product to cart via API
  const addResp = await page.request.post('/api/cart/add', {
    data: { product_id: 1, quantity: 1 },
    headers: { Authorization: `Bearer ${token}` }
  });
  expect(addResp.ok()).toBeTruthy();

  // Set token in localStorage so app will be authenticated
  await page.addInitScript(token => {
    localStorage.setItem('access_token', token);
  }, token);

  // Go to checkout page
  await page.goto('/checkout');

  // Fill fields (name, address, phone)
  await page.fill('input[name="name"]', 'Huỳnh Đăng Khoa');
  await page.fill('textarea[name="shipping_address"]', 'Some test address 789');
  await page.fill('input[name="phone"]', '0901111222');

  // Submit and wait for navigation to orders/:id
  await Promise.all([
    page.waitForURL(/\/orders\/\d+/),
    page.click('button:has-text("Xác nhận đặt hàng")')
  ]);

  // Verify order detail shows the provided name
  await page.waitForSelector('text=Người nhận', { timeout: 5000 });
  const recipient = await page.locator('text=Người nhận').locator('..').locator('.font-medium').textContent();
  expect(recipient).toContain('Huỳnh Đăng Khoa');
});