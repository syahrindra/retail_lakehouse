import duckdb

conn = duckdb.connect("analytics_warehouse.duckdb")

print("=========================================================")
print("         ANALYTICS EXECUTIVE DASHBOARD ")
print("=========================================================")

# Business Metric 1: Financial Conversion & Settlement Analysis
print("\n1. FINANCIAL REVENUE SUMMARY:")
df_rev = conn.execute("""
    SELECT 
        COUNT(*) AS total_orders,
        ROUND(SUM(gross_amount_usd), 2) AS total_gross_revenue_usd,
        ROUND(SUM(net_settled_amount_usd), 2) AS total_net_settled_revenue_usd,
        ROUND((SUM(net_settled_amount_usd) / SUM(gross_amount_usd)) * 100, 2) AS payment_conversion_rate_pct
    FROM fct_order_payments
""").df()
print(df_rev.to_string(index=False))

# Business Metric 2: Revenue Distribution by Country
print("\n2. SETTLED REVENUE BY COUNTRY:")
df_country = conn.execute("""
    SELECT 
        c.country_code,
        COUNT(f.order_id) AS total_orders,
        ROUND(SUM(f.net_settled_amount_usd), 2) AS settled_revenue_usd
    FROM fct_order_payments f
    JOIN dim_customers c ON f.customer_key = c.customer_key
    GROUP BY 1
    ORDER BY settled_revenue_usd DESC
""").df()
print(df_country.to_string(index=False))

# Business Metric 3: Payment Gateway Performance
print("\n3. PAYMENT GATEWAY SUCCESS RATES:")
df_payment = conn.execute("""
    SELECT 
        payment_method,
        COUNT(*) AS total_attempts,
        COUNT(CASE WHEN payment_status = 'SUCCESS' THEN 1 END) AS successful_attempts,
        ROUND(COUNT(CASE WHEN payment_status = 'SUCCESS' THEN 1 END) * 100.0 / COUNT(*), 2) AS success_rate_pct
    FROM fct_order_payments
    GROUP BY 1
    ORDER BY success_rate_pct DESC
""").df()
print(df_payment.to_string(index=False))