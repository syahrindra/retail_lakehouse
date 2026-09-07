import duckdb

conn = duckdb.connect()

print("-- RAW DATA LAKE AUDIT REPORT ---")

#1. Check Row Counts & Null Distribution in Customers table
print("\n[1] Customer Data Anomaly Audit:")
conn.execute("""
    SELECT
        COUNT(*) AS total_rows,
        COUNT(CASE
                WHEN email is NULL THEN 1
            END) AS missing_emails,
        COUNT(CASE
                WHEN registered_at = 'INVALID_DATE' THEN 1
            END) AS corrupt_dates,
        COUNT(DISTINCT country_raw) AS distinct_country_strings
    FROM read_parquet('data/bronze/customers/customers.parquet')
""").df().to_string(index=False)
print(conn.execute("SELECT country_raw, COUNT(*) FROM read_parquet('data/bronze/customers/customers.parquet') GROUP BY 1 LIMIT 10").df())

#2. Check Primary Key Uniqueness & Missing Amount in Orders
print("\n[2] Orders Data Anomaly Audit:")
print(conn.execute("""
    SELECT 
        COUNT(*) AS total_rows,
        COUNT(DISTINCT order_id) AS unique_order_ids,
        (COUNT(*) - COUNT(DISTINCT order_id)) AS duplicate_primary_keys,
        COUNT(CASE 
                WHEN total_amount IS NULL OR total_amount = 0 THEN 1 
            END) AS missing_total_amounts
    FROM read_parquet('data/bronze/orders/orders.parquet')
""").df().to_string(index=False))

# 3. Check Referential Integrity (Orphan Customers)
print("\n[3] Orphan Records Audit:")
print(conn.execute("""
    SELECT 
        COUNT(o.order_id) AS orders_with_missing_customer_profile
    FROM read_parquet('data/bronze/orders/orders.parquet') o
    LEFT JOIN read_parquet('data/bronze/customers/customers.parquet') c
      ON o.customer_id = c.customer_id
    WHERE c.customer_id IS NULL
""").df().to_string(index=False))