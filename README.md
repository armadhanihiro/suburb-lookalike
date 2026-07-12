# Demografy AI - Suburb Look-alike Finder

An AI-powered suburb similarity engine developed during the Demografy Internship.

The application combines demographic Key Performance Indicators (KPIs) with semantic suburb descriptions generated through Google's Gemini Embedding model to discover Australian suburbs with similar demographic characteristics.

Instead of relying only on numerical similarity, the system performs **Hybrid Vector Search**, combining standardized demographic indicators with natural language embeddings and retrieving neighbours efficiently using **FAISS Approximate Nearest Neighbour (ANN) Search**.

---

# Features

## Data Processing

- BigQuery integration
- Automated demographic feature loading
- KPI standardisation
- Missing value handling using SA4 median
- Global median fallback
- Remote suburb detection
- Duplicate suburb handling

---

## Hybrid Retrieval

- Numerical similarity baseline
- Gemini text embeddings
- Hybrid vector fusion
- Configurable blend weight (α)
- FAISS Approximate Nearest Neighbour search
- Adjustable Top-N retrieval

---

## Explainability

- Top contributing KPIs
- Hybrid vs Numeric rank comparison
- Radar chart comparison
- Similarity explanation card

---

## Evaluation

- Golden Set evaluation
- Precision@k
- Recall@k
- Alpha sweep comparison
- Numeric vs Hybrid comparison

---

## Engineering

- Structured search logging
- RBAC lookup limitation
- Streamlit interface
- Cached Gemini embeddings

---

# Technology Stack

| Component | Technology |
|-----------|------------|
| Frontend | Streamlit |
| Data | Google BigQuery |
| Embeddings | Gemini Embedding API |
| Vector Search | FAISS |
| Machine Learning | Scikit-learn |
| Data Processing | Pandas, NumPy |
| Visualization | Plotly |
| Language | Python |

---

# Installation

Clone the repository

```bash
git clone https://github.com/<your-repository>.git

cd suburb-lookalike
```

Create virtual environment

```bash
python -m venv .venv
```

Windows

```bash
.venv\Scripts\activate
```

Mac/Linux

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Configure environment variables

Create a `.env`

```text
GEMINI_API_KEY=YOUR_API_KEY
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json
```

Generate embeddings

```bash
python -m scripts.build_embeddings
```

Run the application

```bash
streamlit run app.py
```

---

# 📁 Project Structure

```
suburb-lookalike
│
├── app.py
├── cache/
├── db/
├── engine/
├── evaluation/
├── logs/
├── scripts/
├── ui/
│
├── requirements.txt
└── README.md
```

---

# System Architecture

```text
                BigQuery
                    │
                    ▼
          Demographic Features
                    │
                    ▼
        Standardisation + Cleaning
                    │
        ┌───────────┴───────────┐
        ▼                       ▼
 Numerical Features      Text Profiles
        │                       │
        ▼                       ▼
                        Gemini Embeddings
        │                       │
        └───────────┬───────────┘
                    ▼
              Hybrid Fusion
                    │
                    ▼
              FAISS Index
                    │
                    ▼
            Similarity Search
                    │
                    ▼
          Explanation + Radar Chart
```

---

# 🔍 Hybrid Retrieval Pipeline

The retrieval pipeline combines demographic indicators and semantic suburb descriptions into a single hybrid vector representation.

```text
User selects a suburb
            │
            ▼
 Load demographic KPIs
            │
            ▼
 Standardise KPI values
            │
            ▼
Generate suburb profile
            │
            ▼
Gemini Embedding
            │
            ▼
Hybrid Vector Fusion
            │
            ▼
Build / Query FAISS Index
            │
            ▼
Retrieve Top-N Similar Suburbs
            │
            ▼
Generate KPI Explanation
            │
            ▼
Display Results
```

---

# 🧠 Hybrid Similarity

The system combines two complementary representations:

- **Numeric representation**
  - Standardised demographic KPIs
  - Captures measurable socioeconomic characteristics.

- **Semantic representation**
  - Gemini-generated embedding from suburb profile descriptions.
  - Captures contextual similarities that may not be reflected by numeric KPIs alone.

Both representations are L2-normalised before fusion.

The hybrid vector is defined as

\[
Hybrid = (1-\alpha)\times Numeric + \alpha \times TextEmbedding
\]

where

- α = embedding weight
- (1−α) = demographic KPI weight

This allows balancing structured demographic similarity with semantic similarity.

---

# ⚙️ FAISS Approximate Nearest Neighbour Search

Instead of performing an exhaustive NumPy cosine similarity search, the application indexes hybrid vectors using **FAISS**.

Benefits include:

- Faster similarity search
- Scalable retrieval
- Production-ready vector indexing
- Identical neighbours compared with the NumPy baseline

The FAISS implementation was validated against the previous NumPy baseline to ensure retrieval consistency.

---

# 📊 Evaluation Methodology

The retrieval quality is evaluated using a manually curated **Golden Set**.

Each reference suburb contains:

- one reference suburb
- five expected neighbours
- expert rationale

The retrieved suburbs are compared against this expected set using:

- Precision@3
- Precision@5
- Precision@10
- Recall@3
- Recall@5
- Recall@10

---

# 🏆 Golden Set

The evaluation contains **10 representative reference suburbs**, selected to cover different demographic archetypes across Australia.

| Cluster | Reference |
|----------|-----------|
| 0 | Birkdale (QLD) |
| 1 | Ingleburn (NSW) |
| 2 | Bega – Tathra (NSW) |
| 3 | Halls Creek (WA) |
| 4 | Bibra Industrial (WA) |
| 5 | Aitkenvale (QLD) |
| 6 | Jindalee – Mount Ommaney (QLD) |
| 7 | Abbotsford (VIC) |
| 8 | Subiaco – Shenton Park (WA) |
| 9 | Pallara – Willawong (QLD) |

Each reference contains five manually selected expected neighbours.

---

# 📈 Alpha Sweep

The hybrid model was evaluated using different blending weights.

| Alpha | Precision@3 | Precision@5 | Precision@10 | Recall@3 | Recall@5 | Recall@10 |
|-------:|------------:|------------:|-------------:|----------:|----------:|-----------:|
| 0.0 | 0.567 | 0.520 | 0.350 | 0.340 | 0.520 | 0.700 |
| 0.2 | 0.533 | 0.500 | 0.370 | 0.320 | 0.500 | 0.740 |
| 0.4 | 0.533 | 0.480 | 0.390 | 0.320 | 0.480 | 0.780 |
| 0.6 | 0.433 | 0.400 | 0.280 | 0.260 | 0.400 | 0.560 |
| 0.8 | 0.067 | 0.140 | 0.120 | 0.040 | 0.140 | 0.240 |
| 1.0 | 0.067 | 0.040 | 0.030 | 0.040 | 0.040 | 0.060 |

---

# 📌 Default Blend Weight

Although α = 0.0 achieves the highest Precision@5, it relies entirely on demographic KPIs and does not leverage semantic information.

The project adopts **α = 0.4** as the default blend weight because it provides:

- balanced contribution from numeric and semantic representations
- improved Recall@10
- meaningful semantic neighbourhoods
- more robust hybrid retrieval

This represents a practical trade-off between numerical consistency and semantic similarity.

---

# 📋 Example Evaluation

Example output from the evaluation harness:

| Metric | Score |
|---------|------:|
| Precision@3 | 0.533 |
| Precision@5 | 0.480 |
| Precision@10 | 0.390 |
| Recall@3 | 0.320 |
| Recall@5 | 0.480 |
| Recall@10 | 0.780 |

These metrics provide quantitative evidence that the hybrid retrieval pipeline produces relevant demographic neighbours while preserving semantic similarity.

---

# 📜 Structured Logging

To improve observability, every lookup is recorded as a structured JSON log.

Each search stores:

- Timestamp
- User ID
- Selected reference suburb
- Alpha value
- Top-N parameter
- Selected preset
- Data source
- Search latency
- Retrieved neighbours

Example:

```json
{
  "timestamp": "2026-06-29T22:57:43",
  "user_id": "user_066",
  "reference": "Googong (NSW)",
  "alpha": 0.4,
  "top_n": 5,
  "preset": "Custom",
  "duration_ms": 139.73,
  "results": [
    {
      "rank": 1,
      "suburb": "Denman Prospect",
      "score": 89.20
    }
  ]
}
```

Structured logging enables:

- Performance monitoring
- Usage analytics
- Search reproducibility
- Debugging
- Future recommendation analytics

---

# 🛡 Edge Case Handling

Several edge cases are handled to improve robustness.

## Missing KPI Values

Rows with excessive missing KPI values are excluded from modelling.

Remaining missing values are imputed using:

1. SA4 median
2. Global median fallback

This preserves local demographic characteristics while ensuring complete feature vectors.

---

## Duplicate Suburb Names

Display names are made unique by appending additional identifiers when duplicates exist.

This guarantees that the selected suburb always maps to the correct record.

---

## Remote Outliers

Remote suburbs are identified using a data-driven approach based on the dataset distribution.

Instead of hard-coded thresholds, the system flags suburbs that simultaneously belong to:

- the lowest population quantile
- the largest geographic area quantile

This makes the detection adaptive to future datasets.

---

## Gemini API Retry

Embedding generation uses exponential backoff to handle temporary API failures.

Retry schedule:

```
2 seconds
4 seconds
8 seconds
16 seconds
32 seconds
```

This improves stability during large embedding builds.

---

# 📈 Explainability

Unlike traditional similarity search, the application explains *why* suburbs are considered similar.

Each recommendation includes:

- similarity score
- top contributing KPIs
- hybrid vs numeric ranking difference
- radar chart comparison

This allows users to understand the reasoning behind every retrieved neighbour.

---

# Search Output

Each search returns:

- Top-N similar suburbs
- Similarity score
- State
- Top contributing KPIs
- Hybrid vs Numeric ranking difference
- Radar chart comparison

---

# Stretch Goal

The original internship specification proposed an optional extension:

**K-Means Demographic Archetypes**

This has intentionally been left as future work after completing the core hybrid retrieval pipeline.

---

# 📚 References

- Google Gemini Embedding API
- Google BigQuery
- FAISS: Facebook AI Similarity Search
- Scikit-learn
- Streamlit

---

# 👥 Authors

| Team Member | Role | Responsibilities |
|------------|------|------------------|
| **Armadhani Hiro Juni Permana** | **Embeddings / Fusion (Technical Lead)** | Led the technical direction of the project, implemented the hybrid retrieval pipeline, Gemini embeddings, vector fusion, FAISS integration, similarity evaluation (Golden Set, Precision@k/Recall@k, Alpha Sweep), structured logging, and technical documentation. |
| **Jiewen He** | **Data / Numeric** | Conducted dataset exploration, implemented the numeric pipeline, feature engineering, KPI preprocessing, missing value handling, and contributed to frontend development and application integration. |
| **Keerthika Mohan** | **Frontend / Evaluation** | Developed the Streamlit application, implemented UI features, integrated system components. |

---

# 📄 License

This repository was developed as part of an internship project.

All datasets remain the property of Demografy.

The source code is intended for educational and portfolio purposes unless otherwise specified.
