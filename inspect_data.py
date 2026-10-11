
import csv, statistics, collections

with open('laptop_price.csv', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

# Strip any BOM / whitespace from keys
rows = [{k.strip().lstrip('\ufeff'): v for k,v in r.items()} for r in rows]

print(f'Total rows: {len(rows)}')
print(f'Columns: {list(rows[0].keys())}')
print()

# Check price field
prices = []
for r in rows:
    try:
        prices.append(float(r['Price']))
    except:
        pass

print(f'Price stats ({len(prices)} valid):')
print(f'  Min:    {min(prices):,.0f}')
print(f'  Max:    {max(prices):,.0f}')
print(f'  Median: {statistics.median(prices):,.0f}')
print(f'  Mean:   {statistics.mean(prices):,.0f}')
print()

# Sample prices alongside specs to confirm currency
print('Sample rows (Company, TypeName, Ram, Price):')
for r in rows[:8]:
    print(f"  {r['Company']:12} {r['TypeName']:15} {r['Ram']:6} {float(r['Price']):>12,.0f}")

print()
# Check for missing values
print('Missing values per column:')
for col in rows[0].keys():
    missing = sum(1 for r in rows if not r[col].strip())
    print(f'  {col}: {missing}')

print()
# Unique categoricals
print('Unique Company:', sorted(set(r['Company'] for r in rows)))
print()
print('Unique TypeName:', sorted(set(r['TypeName'] for r in rows)))
print()
print('Unique OpSys:', sorted(set(r['OpSys'] for r in rows)))
print()
print('Unique Ram samples:', sorted(set(r['Ram'] for r in rows))[:10])
print('Unique Weight samples:', sorted(set(r['Weight'] for r in rows))[:10])
print('Unique Memory samples:', sorted(set(r['Memory'] for r in rows))[:10])
