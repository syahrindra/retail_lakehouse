-- Aggregate multiple payment attempts per order into a single payment status state

WITH raw_payments AS (
    SELECT * FROM read_parquet('data/bronze/payments/payments.parquet')
),
ranked_payments AS (
    SELECT
        TRIM(payment_id) AS payment_id,
        TRIM(order_id) AS order_id,
        COALESCE(payment_method, 'UNKNOWN') AS payment_method,
        payment_status,
        TRY_CAST(payment_timestamp AS TIMESTAMP) as payment_timestamp,
        ROW_NUMBER() OVER (
            PARTITION BY order_id
            ORDER BY
                CASE 
                    WHEN payment_status = 'SUCCESS' THEN 1
                ELSE 2
                END,
                payment_timestamp DESC
        ) AS status_rank
    FROM raw_payments
)

SELECT
    payment_id,
    order_id,
    payment_method,
    payment_status,
    payment_timestamp,
FROM ranked_payments
WHERE status_rank = 1