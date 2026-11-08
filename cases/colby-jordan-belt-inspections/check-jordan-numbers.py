"""Independent check; run with Python 3 and the team's released CSV path."""
import csv
import json
import sys
from decimal import Decimal

with open(sys.argv[1], newline='', encoding='utf-8-sig') as f:
    rows = list(csv.DictReader(f))
groups = {
    'All records': rows,
    'Belt contact': [r for r in rows if r['injury_mechanism'] == 'Belt contact'],
    'Search: belt': [r for r in rows if 'belt' in r['Narrative_1'].lower()],
}
output = {}
for label, group in groups.items():
    weight = sum((Decimal(r['Weight']) for r in group), Decimal(0))
    severe = [r for r in group if r['Disposition'] in ('2', '4', '5', '8')]
    severe_weight = sum((Decimal(r['Weight']) for r in severe), Decimal(0))
    output[label] = [len(group), str(weight), len(severe), str(severe_weight),
                     str(100 * severe_weight / weight)]
print(json.dumps(output, indent=2))
