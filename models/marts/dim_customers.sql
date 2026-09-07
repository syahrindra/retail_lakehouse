WITH clean_customers AS (
    SELECT * FROM {{ ref('stg_customers') }}
)

SELECT
    DENSE_RANK() OVER (ORDER BY customer_id) AS customer_key,
    customer_id AS original_customer_id,
    clean_email,
    country_code,
    registered_at
FROM clean_customers

UNION ALL

-- Default unknown member key for orphan orders
SELECT
    -1 AS customer_key,
    'UNKNOWN' AS original_customer_id,
    'unknown@noemail.com' AS clean_email,
    'OTHER' AS country_code,
    NULL AS registered_at