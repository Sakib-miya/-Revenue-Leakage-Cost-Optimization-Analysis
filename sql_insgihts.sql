create database revenue_leakage_and_cost_optimization_analysis;
use revenue_leakage_and_cost_optimization_analysis;
-- Query 1: Total Revenue Leakage Summary
WITH leakage_sources AS (
  -- Source 1: Excessive Discounts (>25%)
  SELECT 
    'Excessive Discounts' as leakage_source,
    SUM((unit_price - discounted_price) * quantity) as amount_lost
  FROM order_items
  WHERE discount_pct > 25
  
  UNION ALL
  
  -- Source 2: Unprofitable Shipping
  SELECT 
    'Shipping Loss' as leakage_source,
    SUM(shipping_cost - shipping_revenue) as amount_lost
  FROM ecom_orders
  WHERE shipping_cost > shipping_revenue
  
  UNION ALL
  
  -- Source 3: Returns (No Restocking Fee)
  SELECT 
    'Product Returns' as leakage_source,
    SUM(refund_amount + shipping_refunded) as amount_lost
  FROM returns
  
  UNION ALL
  
  -- Source 4: Negative Margin Orders
  SELECT 
    'Negative Margin Orders' as leakage_source,
    SUM(ABS(profit)) as amount_lost
  FROM ecom_orders
  WHERE profit < 0
)
SELECT 
  leakage_source,
  ROUND(amount_lost, 2) as total_leakage,
  ROUND(100.0 * amount_lost / SUM(amount_lost) OVER (), 2) as pct_of_total_leakage,
  ROUND(amount_lost / (SELECT SUM(total_revenue) FROM ecom_orders) * 100, 2) as pct_of_revenue
FROM leakage_sources
ORDER BY total_leakage DESC;

-- Query 2: Discount Abuse Analysis
SELECT 
  c.customer_id,
  c.segment,
  COUNT(o.order_id) as total_orders,
  ROUND(AVG(o.discount_amount), 2) as avg_discount_per_order,
  SUM(o.discount_amount) as total_discount_taken,
  SUM(o.total_revenue) as lifetime_revenue,
  SUM(o.profit) as lifetime_profit,
  ROUND(100.0 * SUM(CASE WHEN o.discount_amount > 50 THEN 1 ELSE 0 END) / COUNT(*), 2) as high_discount_rate
FROM ecom_customers c
JOIN ecom_orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.segment
HAVING total_discount_taken > 200
ORDER BY total_discount_taken DESC
LIMIT 50;

-- Query 3: Unprofitable Customer Segments
SELECT 
  segment,
  COUNT(DISTINCT customer_id) as customers,
  COUNT(*) as total_orders,
  ROUND(AVG(total_revenue), 2) as avg_order_value,
  ROUND(AVG(profit), 2) as avg_profit_per_order,
  SUM(total_revenue) as total_revenue,
  SUM(profit) as total_profit,
  ROUND(100.0 * SUM(profit) / SUM(total_revenue), 2) as profit_margin_pct,
  SUM(CASE WHEN profit < 0 THEN 1 ELSE 0 END) as unprofitable_orders
FROM ecom_orders
GROUP BY segment
ORDER BY total_profit ASC;

-- Query 4: High Return Products
SELECT 
  p.product_name,
  p.category,
  p.cost_price,
  p.standard_price AS standard_price,  -- Now correctly using 'standard_price' from products table
  COUNT(DISTINCT oi.order_id) as times_ordered,
  COUNT(DISTINCT r.order_id) as times_returned,
  ROUND(100.0 * COUNT(DISTINCT r.order_id) / COUNT(DISTINCT oi.order_id), 2) as return_rate,
  SUM(r.refund_amount) as total_refunds,
  ROUND(AVG(r.refund_amount), 2) as avg_refund
FROM products p
JOIN order_items oi ON p.product_id = oi.product_id  -- Join products table with order_items
LEFT JOIN returns r ON oi.order_id = r.order_id
GROUP BY p.product_id, p.product_name, p.category, p.cost_price, p.standard_price  -- Correct grouping
HAVING return_rate > 20
ORDER BY total_refunds DESC;

-- Query 5: Product Margin Erosion
SELECT 
  oi.category,
  oi.product_name,
  oi.cost_price,
  p.standard_price AS standard_price,  -- Using 'standard_price' from products table
  ROUND(AVG(oi.discounted_price), 2) as avg_selling_price,
  ROUND(p.standard_price - oi.cost_price, 2) as standard_margin,
  ROUND(AVG(oi.discounted_price) - oi.cost_price, 2) as actual_margin,
  ROUND(100.0 * (AVG(oi.discounted_price) - oi.cost_price) / AVG(oi.discounted_price), 2) as actual_margin_pct,
  ROUND(p.standard_price - AVG(oi.discounted_price), 2) as margin_erosion,
  SUM(oi.quantity) as units_sold
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id  -- Join products table with order_items
GROUP BY oi.category, oi.product_name, oi.cost_price, p.standard_price  -- Correct grouping
HAVING actual_margin_pct < 15
ORDER BY margin_erosion DESC
LIMIT 30;

-- Query 6: Shipping Cost Analysis by Region/Weight
SELECT 
  CASE 
    WHEN shipping_cost < 5 THEN 'Under $5'
    WHEN shipping_cost < 10 THEN '$5-$10'
    WHEN shipping_cost < 15 THEN '$10-$15'
    ELSE 'Over $15'
  END as shipping_cost_bucket,
  COUNT(*) as orders,
  ROUND(AVG(shipping_cost), 2) as avg_cost,
  ROUND(AVG(shipping_revenue), 2) as avg_revenue,
  ROUND(AVG(shipping_cost - shipping_revenue), 2) as avg_loss_per_order,
  SUM(shipping_cost - shipping_revenue) as total_shipping_loss
FROM ecom_orders
GROUP BY shipping_cost_bucket
ORDER BY total_shipping_loss DESC;

-- Query 7: Channel ROI Analysis
SELECT 
  channel,
  COUNT(DISTINCT o.customer_id) as customers,
  COUNT(o.order_id) as orders,
  SUM(o.total_revenue) as total_revenue,
  SUM(o.profit) as total_profit,
  ROUND(AVG(o.profit), 2) as avg_profit_per_order,
  ROUND(100.0 * SUM(o.profit) / SUM(o.total_revenue), 2) as profit_margin
FROM ecom_orders o
GROUP BY channel
ORDER BY total_profit DESC;

