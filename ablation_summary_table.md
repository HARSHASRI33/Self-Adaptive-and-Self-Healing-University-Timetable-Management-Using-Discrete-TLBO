# Ablation Study Summary

| Variant | Runs | Repair Success Rate (%) | Mean Hard Violations | Mean Changed Sessions | Mean Movable Sessions | Mean Repair Time (ms) |
|---|---:|---:|---:|---:|---:|---:|
| Proposed adaptive local | 15 | 100 | 0 | 1 | 1 | 492.31 |
| Fixed mutation local | 15 | 100 | 0 | 1 | 1 | 560.01 |
| Adaptive global | 15 | 0 | 1 | 0 | 90 | 579.65 |
| Adaptive local no stability | 15 | 100 | 0 | 1 | 1 | 520.06 |

## Interpretation

The proposed adaptive local repair configuration achieved a 100% repair-success rate across 15 runs while moving one session on average. The global-repair configuration allowed all 90 sessions to move, but did not achieve feasibility within the fixed 25-generation repair budget.
