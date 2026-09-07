WITH orders AS (
    SELECT * FROM {{ ref('stg_orders') }}
),
customers AS (
    SELECT * FROM {{ ref('dim_customers') }}
),
payments AS (
    SELECT * FROM {{ ref('stg_payments') }}
)

SELECT
    o.order_id,
    COALESCE(c.customer_key, -1) AS customer_key, -- Assigns -1 if customer ID is an orphan
    o.order_status,
    p.payment_method,
    COALESCE(p.payment_status, 'UNPAID') AS payment_status,
    o.order_timestamp,
    o.gross_amount_usd,
    CASE 
        WHEN p.payment_status = 'SUCCESS' THEN o.gross_amount_usd 
        ELSE 0.0 
    END AS net_settled_amount_usd
FROM orders o
LEFT JOIN customers c ON o.customer_id = c.original_customer_id
LEFT JOIN payments p ON o.order_id = p.order_id