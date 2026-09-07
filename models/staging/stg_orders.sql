-- Imputes missing values and removes duplicate primary keys. we dont want to just delete duplicate from main data

WITH raw_orders AS (
    SELECT * FROM read_parquet('data/bronze/orders/orders.parquet')
),
deduplicated AS (
    SELECT
        TRIM(order_id) AS order_id,
        TRIM(customer_id) AS customer_id,
        COALESCE(order_status, 'UNKNOW') AS order_status,
        TRY_CAST(order_timestamp AS TIMESTAMP) AS order_timestamp,
        item_count,
        unit_price,
        -- Impute missing amount if NULL or zero
        CASE
            WHEN total_amount IS NULL OR total_amount = 0
            THEN ROUND(item_count * unit_price, 2)
            ELSE total_amount
        END AS gross_amount_usd,
        ROW_NUMBER() OVER (
            PARTITION BY order_id
            ORDER BY order_timestamp DESC
        ) AS row_num
    FROM raw_orders
)

SELECT
    order_id,
    customer_id,
    order_status,
    order_timestamp,
    item_count,
    unit_price,
    gross_amount_usd
FROM deduplicated
WHERE row_num = 1 -- Retains only distinct record per order_id