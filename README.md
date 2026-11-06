THAMES – Retail Customer Analytics & Recommendation Platform

**THAMES** is an ML-powered retail intelligence platform that transforms customer activity data into actionable business insights through distributed data processing, customer segmentation and personalized product recommendations.

Built using **Databricks, PySpark, Delta Lake, Spark MLlib, MLflow and Streamlit**.

---

## Project Overview

THAMES simulates a retail analytics environment and processes customer interactions across product views, cart additions and purchases.

The platform combines data engineering, machine learning and interactive analytics to demonstrate an end-to-end retail intelligence workflow.

### Dataset at a Glance

| Dataset | Records |
|---|---:|
| Customers | 10,000 |
| Products | 500 |
| Customer activity events | 100,000 |
| Customer feature records | 10,000 |
| Generated recommendations | 49,995 |

*Data is synthetically generated for project demonstration.*

---

## Key Features

### 1. Customer Analytics
- Customer behavioural analysis using interaction data.
- Tracking of product views, cart additions and purchases.
- Customer-level feature engineering.
- Spending and purchasing behaviour analysis.

### 2. Product Catalogue
- Catalogue containing 500 synthetic retail products.
- Category and product search filters.
- Product attributes including price, brand, material, colour and ratings.

### 3. Customer Segmentation
- K-Means clustering using Apache Spark MLlib.
- Feature standardization and behavioural segmentation.
- Analysis of customer purchasing and engagement patterns.

### 4. Product Recommendation Engine
- Collaborative filtering using the Alternating Least Squares (ALS) algorithm.
- Implemented using Spark MLlib.
- Five unseen product recommendations generated per eligible customer.
- Recommendations ranked using predicted ALS scores.

### 5. MLflow Experiment Tracking
- Experiment and parameter logging.
- ALS model artifact tracking.
- Customer and product indexer logging.
- Model training metadata and experiment records.

### 6. Interactive Dashboard
Built with Streamlit and Plotly, featuring:
- Platform Overview
- Product Catalogue
- Customer Analytics
- Customer Segmentation
- Product Recommendations
- MLflow Tracking

---

## Technology Stack

| Layer | Technologies |
|---|---|
| Programming | Python |
| Distributed Processing | Apache PySpark, Spark SQL |
| Data Platform | Databricks |
| Storage | Delta Lake |
| Machine Learning | Spark MLlib, K-Means, ALS |
| Experiment Tracking | MLflow |
| Dashboard | Streamlit, Plotly |
| Connectivity | Databricks SQL Connector |
| Version Control | Git, GitHub |

---

## System Architecture

```text
          Synthetic Retail Data
                    |
                    v
          Databricks + PySpark
                    |
                    v
        Data Cleaning & Feature Engineering
                    |
                    v
              Delta Lake
                    |
          +---------+---------+
          |                   |
          v                   v
    K-Means Model          ALS Model
          |                   |
          v                   v
 Customer Segments      Product Recommendations
          |                   |
          +---------+---------+
                    |
                    v
             MLflow Tracking
                    |
                    v
           Streamlit Dashboard
                    |
                    v
          Interactive Analytics
```

---

## Model Evaluation

The ALS recommendation model was evaluated using a train/test split and full-catalogue ranking methodology.

Evaluation metrics:
- Precision@5
- Recall@5
- NDCG@5

The initial evaluation indicated limited recommendation relevance, highlighting the need for more realistic customer preference patterns in synthetic interaction data.

Further improvements to synthetic data generation and recommendation quality are planned.

---

## Repository Structure

```text
THAMES/
│
├── notebooks/
│   ├── day1.ipynb
│   ├── product_catalogue_creation.ipynb
│   └── thames_large_dataset.ipynb
│
├── dashboard/
│   └── app.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

*Note: The current repository keeps `app.py` in the root directory. The structure above can be updated if the dashboard is moved into a separate folder.*

---

## Getting Started

### Prerequisites
- Python 3.10 or later, compatible with the installed dependencies.
- A Databricks workspace.
- Access to the required THAMES Delta tables.
- Databricks SQL connection credentials.

### 1. Clone the Repository

```bash
git clone https://github.com/rusheel04/THAMES.git
cd THAMES
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Databricks Credentials

Create a `.streamlit/secrets.toml` file locally and provide the Databricks connection details using the secret keys expected by `app.py`.

Never commit credentials, access tokens or passwords to GitHub.

### 5. Run the Dashboard

```bash
streamlit run app.py
```

Open the application at:

```text
http://localhost:8501
```

---

## Future Enhancements

- More realistic customer preference modelling.
- Improved recommendation quality and model benchmarking.
- Automated data processing using Databricks Workflows.
- Dynamic customer event ingestion.
- Automated model retraining and evaluation.
- Dashboard deployment and monitoring.

---

## Author

Rusheel Ganguly

GitHub: [@rusheel04](https://github.com/rusheel04)

Project Repository: [THAMES](https://github.com/rusheel04/THAMES)
