-- Cleans whitespaces, standardizes country codes, and handles corrupt dates
WITH raw_customers AS (
    SELECT *
    FROM read_parquet('data/bronze/customers/customers.parquet')
)

SELECT 
    TRIM(customer_id) AS customer_id,
    LOWER(TRIM(COALESCE(email, 'unknown@noemail.com'))) AS clean_email,
    CASE
        WHEN UPPER(TRIM(country_raw)) IN ('INDONESIA', 'ID', 'IDN') THEN 'ID'
        WHEN UPPER(TRIM(country_raw)) IN ('UNITED STATES', 'US', 'USA') THEN 'US'
        WHEN UPPER(TRIM(country_raw)) IN ('SINGAPORE', 'SG') THEN 'SG'
        ELSE 'OTHER'
    END AS country_code,
    CASE
        WHEN registered_at = 'INVALID_DATE' THEN NULL
        ELSE TRY_CAST(registered_at AS TIMESTAMP)
    END AS registered_at
FROM raw_customers