# THAMES – Retail Customer Analytics & Recommendation Platform

**THAMES** is a retail analytics platform built using Apache Spark, Databricks, Delta Lake and machine learning. It processes customer interaction data to generate behavioural insights, segment customers and recommend products through collaborative filtering.

## Project Overview

THAMES demonstrates how large-scale retail activity data can be transformed into actionable customer insights using distributed data processing and machine learning.

The platform uses synthetic retail data representing customer behaviour across product views, cart additions and purchases.

### Dataset

| Dataset | Records |
|---|---:|
| Customers | 10,000 |
| Products | 500 |
| Customer activity events | 100,000 |
| Customer features | 10,000 |
| Generated recommendations | 49,995 |

## Key Features

### 1. Customer Analytics
- Customer activity analysis.
- Views, cart additions and purchase tracking.
- Customer spending and behavioural feature engineering.
- Product and category-level analytics.

### 2. Customer Segmentation
- K-Means clustering using Spark MLlib.
- Customer segmentation based on behavioural features.
- Analysis of purchasing and engagement patterns.

### 3. Product Recommendation Engine
- ALS collaborative filtering using Spark MLlib.
- Recommendations generated for customers based on historical interactions.
- Previously interacted-with products excluded from recommendations.
- Five recommendations generated per eligible customer.

### 4. MLflow Experiment Tracking
- Model and experiment logging.
- ALS model artifact tracking.
- Customer and product indexer logging.
- Training and recommendation metadata.

### 5. Interactive Streamlit Dashboard
The dashboard includes six sections:
- Overview
- Product Catalogue
- Customer Analytics
- Customer Segmentation
- Product Recommendations
- MLflow Tracking

## Technology Stack

| Component | Technologies |
|---|---|
| Programming | Python |
| Data Processing | PySpark, Spark SQL |
| Data Platform | Databricks |
| Storage | Delta Lake |
| Machine Learning | Spark MLlib, K-Means, ALS |
| Experiment Tracking | MLflow |
| Dashboard | Streamlit, Plotly |
| Database Connectivity | Databricks SQL Connector |
| Version Control | Git, GitHub |

## Architecture

```text
Synthetic Retail Data
        |
        v
Databricks + PySpark
        |
        v
Data Cleaning and Feature Engineering
        |
        v
Delta Lake Tables
        |
        +--------------------+
        |                    |
        v                    v
K-Means Segmentation    ALS Recommendation Engine
        |                    |
        v                    v
Customer Segments       Product Recommendations
        |                    |
        +----------+---------+
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

# Local Setup

# Prerequisites
- Python 3.10 or later (use a version compatible with your installed dependencies).
- A Databricks workspace.
- Access to the THAMES Delta tables.
- Databricks SQL connection credentials.

### Installation

Clone the repository:

```bash
git clone https://github.com/rusheel04/THAMES.git
cd THAMES
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

# Databricks Configuration

Create a local `.streamlit/secrets.toml` file and configure your Databricks connection credentials.

The configuration must use the secret key names expected by `app.py`.

**Never commit access tokens, passwords or private credentials to GitHub.**

### Run the Dashboard

```bash
streamlit run app.py
```

The dashboard will be available locally at:

```text
http://localhost:8501
```

# Machine Learning Evaluation

The ALS recommendation model has been trained using customer-product interaction data.

A preliminary full-catalogue evaluation was performed using a train/test split and the following ranking metrics:

- Precision@5
- Recall@5
- NDCG@5

The initial results indicated limited recommendation relevance, highlighting the need for more realistic customer preference patterns in synthetic data generation.

Further model improvements and evaluation are ongoing.

#Project Status

Current implementation:
- Large-scale synthetic dataset generation.
- Customer feature engineering.
- K-Means customer segmentation.
- ALS collaborative filtering.
- MLflow experiment tracking.
- Interactive Streamlit analytics dashboard.

Planned improvements:
- Improved synthetic customer preference modelling.
- Recommendation model benchmarking.
- Automated data processing with Databricks Workflows.
- Dynamic event ingestion and dashboard refresh.
- Application deployment.

Author

Rusheel Ganguly

GitHub: [@rusheel04](https://github.com/rusheel04)
