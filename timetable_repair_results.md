# Timetable Repair Results

| Variant | Seed | Hard Violations | Changed Sessions | Repair Time (ms) | Movable Sessions | Success |
|---|---:|---:|---:|---:|---:|---|
| Proposed adaptive local | 1 | 0 | 1 | 252.125 | 1 | Yes |
| Proposed adaptive local | 2 | 0 | 1 | 266.448 | 1 | Yes |
| Fixed mutation local | 1 | 0 | 1 | 602.282 | 1 | Yes |
| Adaptive global | 1 | 1 | 0 | 555.376 | 90 | No |
| Adaptive local no stability | 1 | 0 | 1 | 507.182 | 1 | Yes |

## Notes

- Hard violations must be zero for a feasible repaired timetable.
- The proposed adaptive local approach repaired the tested disruptions by changing one session.
- The adaptive global approach allowed all 90 sessions to move but did not reach feasibility within the fixed repair budget.
- These entries are individual experimental runs. The full 15-seed data is in ablation_runs.csv and aggregate values are in ablation_summary.csv.
