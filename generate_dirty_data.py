import pyarrow as pa
import pyarrow.parquet as pq
import pandas as pd
import numpy as np
import os
import random
from datetime import datetime, timedelta

os.makedirs("data/bronze/customers", exist_ok=True)
os.makedirs("data/bronze/orders", exist_ok=True)
os.makedirs("data/bronze/payments", exist_ok=True)

print("--> Generating 10.5M+ dirty records across 3 datasets...")

# ---------------------------------------------------------
# 1. CUSTOMERS (~500,000 rows)
# ---------------------------------------------------------
NUM_CUSTOMERS = 500_000
countries_dirty = ["Indonesia", "ID", "IDN", " United States ", "US", "USA", "Singapore", "SG", None]

print("    [1/3] Generating 500,000 Customer profiles...")
cust_df = pd.DataFrame({
    "customer_id": [f"CUST_{i}" for i in range(1, NUM_CUSTOMERS + 1)],
    "email": [f"user_{i}@example.com" if random.random() > 0.08 else None for i in range(1, NUM_CUSTOMERS + 1)],
    "country_raw": np.random.choice(countries_dirty, size=NUM_CUSTOMERS),
    "registered_at": [
        (datetime(2024, 1, 1) + timedelta(days=random.randint(0, 500))).strftime("%Y/%m/%d %H:%M:%S")
        if random.random() > 0.05 else "INVALID_DATE"
        for _ in range(NUM_CUSTOMERS)
    ]
})
pq.write_table(pa.Table.from_pandas(cust_df), "data/bronze/customers/customers.parquet")
del cust_df # Free RAM immediately

# ---------------------------------------------------------
# 2. ORDERS (~4,500,000 base rows + 2% duplicates = 4.59M)
# ---------------------------------------------------------
NUM_ORDERS = 4_500_000
print("    [2/3] Generating 4,590,000 Order records...")

# Base IDs + intentional duplicate primary keys
order_ids = [f"ORD_{i}" for i in range(1, NUM_ORDERS + 1)]
duplicate_ids = random.choices(order_ids, k=int(NUM_ORDERS * 0.02))
all_order_ids = order_ids + duplicate_ids
TOTAL_ORDER_ROWS = len(all_order_ids)

orders_df = pd.DataFrame({
    "order_id": all_order_ids,
    "customer_id": [f"CUST_{random.randint(1, NUM_CUSTOMERS + 5000)}" for _ in range(TOTAL_ORDER_ROWS)], # Includes orphan IDs
    "order_status": np.random.choice(["COMPLETED", "CANCELLED", "PENDING", None], size=TOTAL_ORDER_ROWS),
    "order_timestamp": [
        (datetime(2025, 1, 1) + timedelta(minutes=random.randint(0, 500000))).isoformat()
        for _ in range(TOTAL_ORDER_ROWS)
    ],
    "item_count": np.random.randint(1, 10, size=TOTAL_ORDER_ROWS),
    "unit_price": np.round(np.random.uniform(5.0, 250.0, size=TOTAL_ORDER_ROWS), 2),
    "total_amount": np.where(np.random.rand(TOTAL_ORDER_ROWS) < 0.12, None, 0.0) # 12% missing amounts for dbt imputation
})
pq.write_table(pa.Table.from_pandas(orders_df), "data/bronze/orders/orders.parquet")
del orders_df

# ---------------------------------------------------------
# 3. PAYMENTS (~5,500,000 transaction attempts)
# ---------------------------------------------------------
NUM_PAYMENTS = 5_500_000
print("    [3/3] Generating 5,500,000 Payment events...")

payments_df = pd.DataFrame({
    "payment_id": [f"PAY_{i}" for i in range(1, NUM_PAYMENTS + 1)],
    "order_id": [f"ORD_{random.randint(1, NUM_ORDERS)}" for _ in range(NUM_PAYMENTS)],
    "payment_method": np.random.choice(["CREDIT_CARD", "E_WALLET", "BANK_TRANSFER", None], size=NUM_PAYMENTS),
    "payment_status": np.random.choice(["SUCCESS", "FAILED", "REFUNDED"], size=NUM_PAYMENTS),
    "payment_timestamp": [
        (datetime(2025, 1, 1) + timedelta(minutes=random.randint(0, 500000))).isoformat()
        for _ in range(NUM_PAYMENTS)
    ]
})
pq.write_table(pa.Table.from_pandas(payments_df), "data/bronze/payments/payments.parquet")
del payments_df

print("--> SUCCESS: 10,590,000 dirty records written to Bronze Parquet Lakehouse!")