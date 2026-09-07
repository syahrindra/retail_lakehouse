## Project Overview

This project implements an automated, containerized **Medallion Data Lakehouse** (Bronze -> Silver -> Gold) designed to ingest, cleanse, transform, and analyze **10,590,000 transaction events**.

The architecture uses a vectorized modern data stack—combining **Python 3.12**, **Apache PyArrow**, **DuckDB**, and **dbt-core (`dbt-duckdb`)** inside **Docker Compose**—to process out-of-core datasets exceeding 10 million rows while keeping peak memory consumption under 500 MB RAM and total storage footprint under 1.2 GB.

read the detail here: [doc](https://syahrindra.vercel.app/projects/retail_lakehouse)


## How to Run Locally

### Prerequisites
- [Docker](https://docs.docker.com/get-docker/) & [Docker Compose](https://docs.docker.com/compose/install/) installed.

### Execution via Docker Compose

```bash
# 1. Clone the repository
git clone https://github.com/syahrindra/retail_lakehouse.git
cd retail_lakehouse_10m

# 2. Build and run the complete pipeline container
docker compose up --build
```

### Direct Local Execution (Optional Python Virtual Environment)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the orchestrator
python orchestrator.py
```
