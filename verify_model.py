import csv, json, math

# 1. Verify dataset
with open('laptop_price.csv', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))
rows = [{k.strip().lstrip('\ufeff'): v for k,v in r.items()} for r in rows]
prices = [float(r['Price']) for r in rows]
print(f"Dataset: {len(rows)} rows")
print(f"Price range: Rs.{min(prices):.0f} - Rs.{max(prices):.0f} INR")
print(f"Columns: {list(rows[0].keys())}")
print()

# 2. Verify model_coeffs.json
with open('model_coeffs.json') as f:
    m = json.load(f)
print(f"Model: {m['model']}")
print(f"Rows used: {m['rows_used']}, Features: {m['features']}")
print(f"Test R2: {m['test_r2']}, MAPE: {m['test_mape_pct']}%")
print(f"Num coefficients: {len(m['coefficients'])}")
print(f"Intercept: {m['coefficients']['intercept']}")
print()

# 3. Manual prediction check: Dell Notebook, 8GB RAM, 512 SSD, 15.6in, FHD, i5, 2.5GHz, Integrated GPU, Win10, 1.8kg
coeffs = m['coefficients']
ram = 8; stor = 512; screen = 15.6; pix = 1920*1080
ips = 1; freq = 2.5; ctier = 2; gtier = 0; ssd = 1; wt = 1.8

log_price = (
    coeffs['intercept'] +
    math.log2(ram)     * coeffs['log2_ram'] +
    math.log2(stor)    * coeffs['log2_storage'] +
    screen             * coeffs['screen_size'] +
    math.log(pix)      * coeffs['log_pixels'] +
    ips                * coeffs['ips_flag'] +
    freq               * coeffs['cpu_freq_ghz'] +
    ctier              * coeffs['cpu_tier'] +
    gtier              * coeffs['gpu_tier'] +
    ssd                * coeffs['ssd_flag'] +
    wt                 * coeffs['weight_kg'] +
    1                  * coeffs['company_Dell'] +     # Dell
    1                  * coeffs['type_Notebook'] +    # Notebook
    1                  * coeffs['os_Windows_10']      # Windows 10
)
price = math.exp(log_price)
print(f"Manual check - Dell Notebook 8GB/512SSD/i5/Win10/15.6in: Rs.{price:,.0f}")
print("  (Expected ~Rs.50,000-65,000 for this config in 2019 dataset)")
