export default async function run(page, ui) {
  // Fill a typical Dell i5 notebook
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

  await page.click('#result ~ * button, button.primary');
  // Click Estimate Price by text
  await page.getByText('Estimate Price').click();
  await page.waitForTimeout(600);

  const priceText = await page.evaluate(() => {
    const el = document.getElementById('price-display');
    return el ? el.textContent : 'NOT FOUND';
  });
  const rangeText = await page.evaluate(() => {
    const el = document.getElementById('range-display');
    return el ? el.textContent : 'NOT FOUND';
  });
  const resultDisplay = await page.evaluate(() => {
    return document.getElementById('result').style.display;
  });

  return { priceText, rangeText, resultDisplay };
}
