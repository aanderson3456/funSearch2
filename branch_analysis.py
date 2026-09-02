import json
from collections import Counter

def analyze_branches(tree, branch_counts):
    if not tree or tree[0] == 'win':
        return
    if tree[0] == 'move':
        branches = tree[2]
        num_critical = len(branches)
        branch_counts[num_critical] += 1
        
        for b in branches:
            analyze_branches(b[1], branch_counts)
        analyze_branches(tree[3], branch_counts)

with open('/tmp/cert_4_5.json') as f:
    cert = json.load(f)

counts = Counter()
analyze_branches(cert['strategy_tree'], counts)

total_moves = sum(counts.values())
print(f"Total Maker moves (nodes): {total_moves}")
print("Branching factor breakdown (number of critical responses Breaker has):")
for k in sorted(counts.keys()):
    perc = (counts[k] / total_moves) * 100
    print(f"  {k} critical responses: {counts[k]} times ({perc:.1f}%)")
