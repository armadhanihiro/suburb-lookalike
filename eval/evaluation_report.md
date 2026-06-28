# Golden Set Evaluation Report

Alpha: 0.4
Golden references: 10

| Reference | P@3 | P@5 | P@10 | R@3 | R@5 | R@10 |
|---|---:|---:|---:|---:|---:|---:|
| Birkdale - Queensland | 0.667 | 0.600 | 0.400 | 0.400 | 0.600 | 0.800 |
| Ingleburn - New South Wales | 0.667 | 0.400 | 0.300 | 0.400 | 0.400 | 0.600 |
| Bega - Tathra - New South Wales | 0.000 | 0.200 | 0.200 | 0.000 | 0.200 | 0.400 |
| Halls Creek - Western Australia | 0.333 | 0.200 | 0.400 | 0.200 | 0.200 | 0.800 |
| Bibra Industrial - Western Australia | 0.333 | 0.600 | 0.500 | 0.200 | 0.600 | 1.000 |
| Aitkenvale - Queensland | 0.333 | 0.600 | 0.400 | 0.200 | 0.600 | 0.800 |
| Jindalee - Mount Ommaney - Queensland | 0.667 | 0.600 | 0.400 | 0.400 | 0.600 | 0.800 |
| Abbotsford - Victoria | 1.000 | 0.600 | 0.400 | 0.600 | 0.600 | 0.800 |
| Subiaco - Shenton Park - Western Australia | 0.333 | 0.400 | 0.400 | 0.200 | 0.400 | 0.800 |
| Pallara - Willawong - Queensland | 1.000 | 0.600 | 0.500 | 0.600 | 0.600 | 1.000 |
| **Average** | **0.533** | **0.480** | **0.390** | **0.320** | **0.480** | **0.780** |

## Interpretation

- Precision measures how many returned suburbs were expected neighbours.
- Recall measures how many expected neighbours were successfully retrieved.
- Precision usually decreases as K increases because more results are included.
- Recall usually increases as K increases because the model has more chances to retrieve expected neighbours.