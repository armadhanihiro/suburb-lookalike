# Alpha Sweep Evaluation Report

Golden references: 10

| Alpha | P@3 | P@5 | P@10 | R@3 | R@5 | R@10 |
|---:|---:|---:|---:|---:|---:|---:|
| 0.0 | 0.567 | 0.520 | 0.350 | 0.340 | 0.520 | 0.700 |
| 0.2 | 0.533 | 0.500 | 0.370 | 0.320 | 0.500 | 0.740 |
| 0.4 | 0.533 | 0.480 | 0.390 | 0.320 | 0.480 | 0.780 |
| 0.6 | 0.433 | 0.400 | 0.280 | 0.260 | 0.400 | 0.560 |
| 0.8 | 0.067 | 0.140 | 0.120 | 0.040 | 0.140 | 0.240 |
| 1.0 | 0.067 | 0.040 | 0.030 | 0.040 | 0.040 | 0.060 |

## Interpretation

- Alpha controls the balance between numeric KPI similarity and text embedding similarity.
- Alpha 0.0 represents numeric-only similarity.
- Alpha 1.0 represents text-only similarity.
- The selected default alpha should balance precision and recall while keeping rankings stable.