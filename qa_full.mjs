// Full end-to-end QA: 3 realistic laptop configs + screenshot
export default async function run(page, ui) {
  const results = [];

  // ── Config 1: Dell i5 Notebook (budget/mid-range) ──────────────────────────
  await page.selectOption('#company',  'Dell');
  await page.selectOption('#type',     'Notebook');
  await page.selectOption('#ram',      '8');
  await page.fill('#storage',          '512');
  await page.selectOption('#ssd',      '1');
  await page.fill('#screen',           '15.6');
  await page.selectOption('#res',      '1920x1080');
  await page.selectOption('#ips',      '1');
  await page.selectOption('#cpu-tier', '2');
  await page.fill('#cpu-freq',         '2.5');
  await page.selectOption('#gpu',      '0');
  await page.selectOption('#os',       'Windows 10');
  await page.fill('#weight',           '1.8');

  await page.getByText('Estimate Price').click();
  await page.waitForTimeout(400);

  const p1 = await page.evaluate(() => document.getElementById('price-display').textContent);
  const r1 = await page.evaluate(() => document.getElementById('range-display').textContent);
  results.push({ config: 'Dell i5 Notebook 8GB/512SSD/FHD/Win10', price: p1, range: r1 });

  // ── Config 2: Apple Ultrabook (high-end) ───────────────────────────────────
  await page.getByText('Reset').click();
  await page.waitForTimeout(200);

  await page.selectOption('#company',  'Apple');
  await page.selectOption('#type',     'Ultrabook');
  await page.selectOption('#ram',      '16');
  await page.fill('#storage',          '512');
  await page.selectOption('#ssd',      '1');
  await page.fill('#screen',           '13.3');
  await page.selectOption('#res',      '2560x1600');
  await page.selectOption('#ips',      '1');
  await page.selectOption('#cpu-tier', '3');
  await page.fill('#cpu-freq',         '2.3');
  await page.selectOption('#gpu',      '0');
  await page.selectOption('#os',       'macOS');
  await page.fill('#weight',           '1.37');

  await page.getByText('Estimate Price').click();
  await page.waitForTimeout(400);

  const p2 = await page.evaluate(() => document.getElementById('price-display').textContent);
  const r2 = await page.evaluate(() => document.getElementById('range-display').textContent);
  results.push({ config: 'Apple MacBook Pro 16GB/512SSD/Retina/macOS', price: p2, range: r2 });

  // ── Config 3: MSI Gaming Laptop (RTX, i7) ─────────────────────────────────
  await page.getByText('Reset').click();
  await page.waitForTimeout(200);

  await page.selectOption('#company',  'MSI');
  await page.selectOption('#type',     'Gaming');
  await page.selectOption('#ram',      '16');
  await page.fill('#storage',          '1024');
  await page.selectOption('#ssd',      '1');
  await page.fill('#screen',           '15.6');
  await page.selectOption('#res',      '1920x1080');
  await page.selectOption('#ips',      '1');
  await page.selectOption('#cpu-tier', '3');
  await page.fill('#cpu-freq',         '2.8');
  await page.selectOption('#gpu',      '3');
  await page.selectOption('#os',       'Windows 10');
  await page.fill('#weight',           '2.7');

  await page.getByText('Estimate Price').click();
  await page.waitForTimeout(400);

  const p3 = await page.evaluate(() => document.getElementById('price-display').textContent);
  const r3 = await page.evaluate(() => document.getElementById('range-display').textContent);
  results.push({ config: 'MSI Gaming i7/16GB/1TB SSD/RTX/Win10', price: p3, range: r3 });

  // ── Structural checks ──────────────────────────────────────────────────────
  const resultVisible    = await page.evaluate(() => document.getElementById('result').style.display !== 'none');
  const hasDisclaimer    = await page.evaluate(() => document.querySelector('.disclaimer') !== null);
  const hasSourceBar     = await page.evaluate(() => document.querySelector('.source-bar') !== null);
  const hasMetrics       = await page.evaluate(() => document.querySelector('.metrics') !== null);
  const hasBarChart      = await page.evaluate(() => document.querySelectorAll('.bar-row').length > 0);
  const disclaimerText   = await page.evaluate(() => document.querySelector('.disclaimer').textContent.trim().substring(0, 80));
  const sourceText       = await page.evaluate(() => document.querySelector('.source-bar .text').textContent.trim().substring(0, 80));

  // ── Screenshot ─────────────────────────────────────────────────────────────
  // Scroll to top first so the whole page is captured
  await page.evaluate(() => window.scrollTo(0, 0));
  await page.waitForTimeout(200);
  await page.screenshot({ path: 'screenshot_result.png', fullPage: true });

  return {
    predictions: results,
    checks: {
      resultVisible,
      hasDisclaimer,
      hasSourceBar,
      hasMetrics,
      hasBarChart,
      disclaimerText,
      sourceText,
    }
  };
}
