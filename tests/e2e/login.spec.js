const { test, expect } = require('@playwright/test');

test('admin can login', async ({ page, baseURL }) => {
  // Attach listeners to capture console, requests and responses for debugging
  page.on('console', msg => console.log('PAGE CONSOLE:', msg.type(), msg.text()));
  page.on('request', req => console.log('PAGE REQUEST:', req.method(), req.url()));
  page.on('requestfailed', req => console.log('PAGE REQUEST FAILED:', req.method(), req.url(), req.failure()?.errorText));
  page.on('response', resp => console.log('PAGE RESPONSE:', resp.status(), resp.url()));

  await page.goto('/login');

  // Fill form
  await page.fill('input[name="email"]', 'admin@minishop.com');
  await page.fill('input[name="password"]', 'admin123');

  // Debug checks before clicking login
  const pageLocation = await page.evaluate(() => ({ href: location.href, origin: location.origin }));
  console.log('PAGE LOCATION:', pageLocation);

  // Try a direct fetch to the relative API endpoint to see if it is reachable
  const fetchResult = await page.evaluate(async () => {
    try {
      const resp = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: 'admin@minishop.com', password: 'admin123' })
      });
      const text = await resp.text();
      return { ok: resp.ok, status: resp.status, text };
    } catch (e) {
      return { error: String(e) };
    }
  });
  console.log('DIRECT FETCH RESULT:', fetchResult);

  // Click login and wait for the API response (increase timeout to 60s)
  try {
    await Promise.all([
      page.waitForResponse(resp => resp.url().includes('/api/auth/login') && resp.status() === 200, { timeout: 60000 }),
      page.click('button:has-text("Đăng nhập")')
    ]);
  } catch (err) {
    console.error('Login request did not complete:', err.message);
    // Take a screenshot to help debug
    await page.screenshot({ path: 'test-failure-login.png', fullPage: true });
    throw err;
  }

  // Wait for localStorage token
  const token = await page.evaluate(() => localStorage.getItem('access_token'));
  console.log('LOCALSTORAGE access_token:', token);
  expect(token).toBeTruthy();

  // The logout button is inside a hover-dropdown; hover the parent .group to reveal it, then assert
  await page.hover('.group');
  // extra wait to allow CSS transition
  await page.waitForSelector('text=Đăng xuất', { state: 'visible', timeout: 5000 });
  await expect(page.locator('text=Đăng xuất')).toBeVisible({ timeout: 5000 });
});
