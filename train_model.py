
import csv, re, math, json, random

# ── Load dataset ──────────────────────────────────────────────────────────────
with open('laptop_price.csv', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    rows = list(reader)
rows = [{k.strip().lstrip('\ufeff'): v for k,v in r.items()} for r in rows]

# ── Feature extraction helpers ────────────────────────────────────────────────
def parse_ram(s):
    m = re.match(r'(\d+)GB', s)
    return int(m.group(1)) if m else 4

def parse_weight(s):
    m = re.search(r'([\d.]+)', s)
    return float(m.group(1)) if m else 2.0

def parse_screen_size(s):
    try: return float(s)
    except: return 15.6

def parse_storage(mem_str):
    """Return (ssd_gb, hdd_gb, is_ssd_primary)"""
    ssd = 0; hdd = 0
    parts = mem_str.split('+')
    for part in parts:
        part = part.strip()
        # size
        m = re.search(r'([\d.]+)\s*(TB|GB)', part, re.I)
        if not m: continue
        val = float(m.group(1))
        unit = m.group(2).upper()
        if unit == 'TB': val *= 1024
        val = int(val)
        if re.search(r'SSD|NVMe|Flash', part, re.I):
            ssd += val
        else:
            hdd += val
    total = ssd + hdd
    return total if total > 0 else 256, ssd > 0

def parse_resolution(s):
    m = re.search(r'(\d{3,4})x(\d{3,4})', s)
    if m:
        return int(m.group(1)) * int(m.group(2))
    return 1366*768

def has_ips(s):
    return 1 if re.search(r'IPS|Retina|4K', s, re.I) else 0

def parse_cpu_freq(cpu_str):
    m = re.search(r'([\d.]+)GHz', cpu_str)
    return float(m.group(1)) if m else 2.0

def cpu_tier(cpu_str):
    cpu = cpu_str.lower()
    if 'i9' in cpu or 'xeon' in cpu: return 4
    if 'i7' in cpu or 'ryzen 7' in cpu: return 3
    if 'i5' in cpu or 'ryzen 5' in cpu: return 2
    if 'i3' in cpu or 'ryzen 3' in cpu or 'pentium' in cpu: return 1
    return 0

def gpu_tier(gpu_str):
    gpu = gpu_str.lower()
    if any(x in gpu for x in ['rtx','gtx 10','gtx 16','gtx 20','quadro','vega','rx 5']): return 3
    if any(x in gpu for x in ['gtx 9','940','950','960','970','980']): return 2
    if any(x in gpu for x in ['mx','radeon r5','radeon r7','radeon r9']): return 1
    return 0  # integrated

COMPANIES = ['Apple','Asus','Dell','HP','Lenovo','MSI','Microsoft','Razer','Samsung','Acer','Other']
TYPES     = ['Gaming','Ultrabook','Workstation','2 in 1 Convertible','Notebook','Netbook']
OPSYS     = ['Windows 10','macOS','Mac OS X','Linux','Chrome OS','No OS','Other']

def company_enc(s):
    return [1 if s == c else 0 for c in COMPANIES[:-1]]  # drop last

def type_enc(s):
    return [1 if s == t else 0 for t in TYPES[:-1]]

def os_enc(s):
    norm = s if s in OPSYS[:-1] else 'Other'
    return [1 if norm == o else 0 for o in OPSYS[:-1]]

# ── Build feature matrix ──────────────────────────────────────────────────────
X = []
y = []

for r in rows:
    try:
        price = float(r['Price'])
        if price <= 0: continue

        ram   = parse_ram(r['Ram'])
        wt    = parse_weight(r['Weight'])
        size  = parse_screen_size(r['Inches'])
        stor, is_ssd = parse_storage(r['Memory'])
        pix   = parse_resolution(r['ScreenResolution'])
        ips   = has_ips(r['ScreenResolution'])
        freq  = parse_cpu_freq(r['Cpu'])
        ctier = cpu_tier(r['Cpu'])
        gtier = gpu_tier(r['Gpu'])

        feats = [
            math.log2(max(ram, 1)),          # f0
            math.log2(max(stor, 1)),          # f1
            size,                             # f2
            math.log(max(pix, 1)),            # f3
            ips,                              # f4
            freq,                             # f5
            ctier,                            # f6
            gtier,                            # f7
            1 if is_ssd else 0,               # f8
            wt,                               # f9
        ] + company_enc(r['Company']) + type_enc(r['TypeName']) + os_enc(r['OpSys'])

        X.append(feats)
        y.append(math.log(price))             # predict log(price)
    except Exception as e:
        pass

print(f'Rows used: {len(X)}, features per row: {len(X[0])}')

# ── OLS via normal equations (no external libs) ───────────────────────────────
def mat_mul(A, B):
    rows_A, cols_A = len(A), len(A[0])
    rows_B, cols_B = len(B), len(B[0])
    C = [[0.0]*cols_B for _ in range(rows_A)]
    for i in range(rows_A):
        for k in range(cols_A):
            if A[i][k] == 0: continue
            for j in range(cols_B):
                C[i][j] += A[i][k] * B[k][j]
    return C

def transpose(A):
    return [[A[i][j] for i in range(len(A))] for j in range(len(A[0]))]

def mat_inv(A):
    """Gauss-Jordan inverse"""
    n = len(A)
    M = [row[:] + [1.0 if i==j else 0.0 for j in range(n)] for i,row in enumerate(A)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(M[r][col]))
        M[col], M[pivot] = M[pivot], M[col]
        pv = M[col][col]
        if abs(pv) < 1e-12: raise ValueError("Singular matrix")
        M[col] = [x/pv for x in M[col]]
        for r in range(n):
            if r != col:
                f = M[r][col]
                M[r] = [M[r][j] - f*M[col][j] for j in range(2*n)]
    return [row[n:] for row in M]

# Add intercept column
Xb = [[1.0] + row for row in X]
Xt = transpose(Xb)
XtX = mat_mul(Xt, Xb)
Xty = mat_mul(Xt, [[yi] for yi in y])

# Ridge regression: XtX + lambda*I  (lambda=0.01 for numerical stability)
LAMBDA = 0.01
n_feat = len(XtX)
for i in range(n_feat):
    XtX[i][i] += LAMBDA

print("Solving Ridge normal equations (lambda=0.01)...")
XtX_inv = mat_inv(XtX)
beta = mat_mul(XtX_inv, Xty)
coeffs = [b[0] for b in beta]
print(f"Solved. {len(coeffs)} coefficients.")

# ── Evaluate: train/test split 80/20 ─────────────────────────────────────────
random.seed(42)
idx = list(range(len(X)))
random.shuffle(idx)
split = int(0.8 * len(idx))
train_idx = set(idx[:split])
test_idx  = idx[split:]

def predict(row):
    xb = [1.0] + row
    return sum(coeffs[j] * xb[j] for j in range(len(xb)))

# Test metrics
preds = [predict(X[i]) for i in test_idx]
actuals = [y[i] for i in test_idx]
n = len(test_idx)

ss_res = sum((a - p)**2 for a,p in zip(actuals, preds))
ss_tot = sum((a - sum(actuals)/n)**2 for a in actuals)
r2 = 1 - ss_res/ss_tot

mae_log = sum(abs(a-p) for a,p in zip(actuals,preds))/n
# Mean Absolute Percentage Error on actual price
mape = sum(abs(math.exp(a)-math.exp(p))/math.exp(a) for a,p in zip(actuals,preds))/n * 100
rmse_log = math.sqrt(ss_res/n)

print(f"\n=== Test-set metrics (n={n}) ===")
print(f"  R²:        {r2:.4f}")
print(f"  MAE(log):  {mae_log:.4f}")
print(f"  RMSE(log): {rmse_log:.4f}")
print(f"  MAPE:      {mape:.1f}%")

# ── Feature names for export ──────────────────────────────────────────────────
feat_names = ['intercept','log2_ram','log2_storage','screen_size','log_pixels',
              'ips_flag','cpu_freq_ghz','cpu_tier','gpu_tier','ssd_flag','weight_kg']
feat_names += [f'company_{c}' for c in COMPANIES[:-1]]
feat_names += [f'type_{t.replace(" ","_")}' for t in TYPES[:-1]]
feat_names += [f'os_{o.replace(" ","_")}' for o in OPSYS[:-1]]

print("\n=== Coefficients ===")
for name, c in zip(feat_names, coeffs):
    print(f"  {name:35s}: {c:.6f}")

# ── Export to JSON ────────────────────────────────────────────────────────────
export = {
    "model": "OLS Linear Regression on log(price_INR)",
    "dataset": "laptop_data.csv — 1,303 laptops, prices in INR, sourced from Kaggle (Rashmi Margani / CampusX version), originally scraped from idealo.de, 2019",
    "rows_used": len(X),
    "features": len(X[0]),
    "test_r2": round(r2, 4),
    "test_mape_pct": round(mape, 2),
    "test_rmse_log": round(rmse_log, 4),
    "coefficients": {name: round(c, 6) for name, c in zip(feat_names, coeffs)},
    "feature_order": feat_names,
    "companies": COMPANIES,
    "types": TYPES,
    "os_list": OPSYS
}

with open('model_coeffs.json', 'w') as f:
    json.dump(export, f, indent=2)
print("\nSaved model_coeffs.json")
