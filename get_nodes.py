import json

def count_nodes(tree):
    if not tree: return 1
    if tree[0] == 'win': return 1
    if tree[0] == 'move':
        return 1 + count_nodes(tree[3]) + sum(count_nodes(b[1]) for b in tree[2])
    return 1

with open('/tmp/cert_4_5.json') as f:
    cert = json.load(f)
    print("Total nodes:", count_nodes(cert['strategy_tree']))
