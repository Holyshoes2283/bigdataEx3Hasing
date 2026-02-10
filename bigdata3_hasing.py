import random
import bisect
from collections import Counter
import statistics
import numpy as np

MAX = 2**32
NUMBER = 42
N_KEYS = 10000
N_SERVERS = 100
VIRTUALS_PER_SERVER = 5

def assign_to_next_point(key, points_sorted):
    idx = bisect.bisect_right(points_sorted, key)
    return points_sorted[0] if idx == len(points_sorted) else points_sorted[idx]

def stats_from_loads(loads):
    return {
        "avg": statistics.mean(loads),
        "median": statistics.median(loads),
        "min": min(loads),
        "max": max(loads),
        "p25": float(np.percentile(loads, 25)),
        "p75": float(np.percentile(loads, 75)),
    }

random.seed(NUMBER)
keys = [random.randrange(MAX) for _ in range(N_KEYS)]
servers = sorted(random.sample(range(MAX), N_SERVERS))

assignments_A = [assign_to_next_point(k, servers) for k in keys]
counts_A = Counter(assignments_A)
loads_A = [counts_A.get(s, 0) for s in servers]
S_A = stats_from_loads(loads_A)

virtual_nodes = []
for s in servers:
    for _ in range(VIRTUALS_PER_SERVER):
        virtual_nodes.append((random.randrange(MAX), s))
virtual_nodes.sort(key=lambda x: x[0])
virtual_ids = [vid for (vid, _) in virtual_nodes]

def assign_key_to_real_server(key):
    idx = bisect.bisect_right(virtual_ids, key)
    if idx == len(virtual_ids):
        idx = 0
    return virtual_nodes[idx][1]

assignments_B = [assign_key_to_real_server(k) for k in keys]
counts_B = Counter(assignments_B)
loads_B = [counts_B.get(s, 0) for s in servers]
S_B = stats_from_loads(loads_B)

def fmt(x):
    return f"{x:.2f}" if isinstance(x, float) else str(x)

def pct_change(a, b):
    if a == 0:
        return "N/A" if b == 0 else "+inf%"
    return f"{((b - a) / a * 100):+.1f}%"

metrics = ["avg", "median", "min", "max", "p25", "p75"]

print(f"keys={N_KEYS}, servers={N_SERVERS}")
print()
print(f"{'        '} | {'1 id=>1 server'} | {'5 virtual ids=> 1 server':>20}")
print("-" * 52)
for m in metrics:
    print(f"{m:<8} | {fmt(S_A[m]):>14} | {fmt(S_B[m]):>20}")

