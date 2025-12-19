import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

np.random.seed(42)
random.seed(42)

print("Generating Revenue Leakage Analysis Dataset...")

# Parameters
n_customers = 3000
n_products = 200
n_orders = 8000
start_date = datetime(2023, 1, 1)
end_date = datetime(2024, 12, 31)

# ============================================
# 1. GENERATE CUSTOMERS
# ============================================
customers = []
for cust_id in range(1, n_customers + 1):
    segment = random.choices(
        ['High Value', 'Medium Value', 'Low Value', 'Bargain Hunter'],
        weights=[15, 35, 35, 15]
    )[0]
    channel = random.choices(
        ['Organic', 'Paid Ads', 'Email', 'Social', 'Affiliate'],
        weights=[25, 30, 20, 15, 10]
    )[0]
    
    customers.append({
        'customer_id': cust_id,
        'segment': segment,
        'acquisition_channel': channel,
        'join_date': start_date + timedelta(days=random.randint(0, 600))
    })

df_customers = pd.DataFrame(customers)

# ============================================
# 2. GENERATE PRODUCTS
# ============================================
products = []
categories = ['Electronics', 'Clothing', 'Home & Garden', 'Sports', 'Books']

for prod_id in range(1, n_products + 1):
    category = random.choice(categories)
    
    # Different margins by category
    if category == 'Electronics':
        cost = random.uniform(50, 500)
        markup = random.uniform(1.3, 1.8)  # Lower margin
    elif category == 'Clothing':
        cost = random.uniform(10, 80)
        markup = random.uniform(2.0, 3.5)  # Higher margin
    else:
        cost = random.uniform(5, 150)
        markup = random.uniform(1.5, 2.5)
    
    products.append({
        'product_id': prod_id,
        'product_name': f'{category}_Item_{prod_id}',
        'category': category,
        'cost_price': round(cost, 2),
        'standard_price': round(cost * markup, 2),
        'weight_kg': round(random.uniform(0.1, 5.0), 2)
    })

df_products = pd.DataFrame(products)

# ============================================
# 3. GENERATE ORDERS (with leakage scenarios)
# ============================================
orders = []
order_items = []
returns = []
order_id = 1

for _ in range(n_orders):
    customer = df_customers.sample(1).iloc[0]
    order_date = start_date + timedelta(days=random.randint(0, 700))
    
    # LEAKAGE SCENARIO 1: Discount abuse by segment
    if customer['segment'] == 'Bargain Hunter':
        discount_pct = random.uniform(25, 45)  # Heavy discounts!
        uses_coupon = True
    elif customer['segment'] == 'High Value':
        discount_pct = random.uniform(0, 10)
        uses_coupon = random.random() < 0.3
    else:
        discount_pct = random.uniform(5, 20)
        uses_coupon = random.random() < 0.5
    
    # Number of items
    n_items = random.choices([1, 2, 3, 4, 5], weights=[40, 30, 15, 10, 5])[0]
    order_products = df_products.sample(n_items)
    
    subtotal = 0
    order_cost = 0
    total_weight = 0
    
    # Generate order items
    for _, product in order_products.iterrows():
        quantity = random.randint(1, 3)
        unit_price = product['standard_price']
        discounted_price = unit_price * (1 - discount_pct / 100)
        
        item_total = discounted_price * quantity
        item_cost = product['cost_price'] * quantity
        
        subtotal += item_total
        order_cost += item_cost
        total_weight += product['weight_kg'] * quantity
        
        order_items.append({
            'order_id': order_id,
            'product_id': product['product_id'],
            'product_name': product['product_name'],
            'category': product['category'],
            'quantity': quantity,
            'unit_price': round(unit_price, 2),
            'discount_pct': round(discount_pct, 2),
            'discounted_price': round(discounted_price, 2),
            'cost_price': product['cost_price'],
            'total_revenue': round(item_total, 2),
            'total_cost': round(item_cost, 2)
        })
    
    # LEAKAGE SCENARIO 2: Unprofitable shipping
    shipping_cost = max(5, total_weight * 2.5 + random.uniform(-2, 3))
    
    # LEAKAGE SCENARIO 3: Free shipping threshold too low
    if subtotal > 50:  # Low threshold = loss on shipping
        shipping_revenue = 0
    else:
        shipping_revenue = 7.99
    
    orders.append({
        'order_id': order_id,
        'customer_id': customer['customer_id'],
        'segment': customer['segment'],
        'channel': customer['acquisition_channel'],
        'order_date': order_date,
        'subtotal': round(subtotal, 2),
        'discount_amount': round(sum([
            (item['unit_price'] - item['discounted_price']) * item['quantity']
            for item in order_items if item['order_id'] == order_id
        ]), 2),
        'shipping_cost': round(shipping_cost, 2),
        'shipping_revenue': shipping_revenue,
        'total_revenue': round(subtotal + shipping_revenue, 2),
        'total_cost': round(order_cost + shipping_cost, 2),
        'coupon_used': uses_coupon,
        'profit': round(subtotal + shipping_revenue - order_cost - shipping_cost, 2)
    })
    
    # LEAKAGE SCENARIO 4: High return rate (no restocking fee)
    return_prob = 0.15  # 15% return rate
    if random.random() < return_prob:
        return_reasons = [
            'Changed Mind', 
            'Wrong Size', 
            'Defective', 
            'Found Cheaper',  # LEAKAGE!
            'Not as Described'
        ]
        reason_weights = [35, 25, 15, 15, 10]
        
        return_date = order_date + timedelta(days=random.randint(3, 30))
        refund_amount = subtotal * random.uniform(0.5, 1.0)
        
        returns.append({
            'order_id': order_id,
            'return_date': return_date,
            'refund_amount': round(refund_amount, 2),
            'return_reason': random.choices(return_reasons, weights=reason_weights)[0],
            'restocking_fee': 0,  # NO FEE = LEAKAGE!
            'shipping_refunded': shipping_revenue
        })
    
    order_id += 1

df_orders = pd.DataFrame(orders)
df_order_items = pd.DataFrame(order_items)
df_returns = pd.DataFrame(returns)

# ============================================
# 4. SAVE ALL FILES
# ============================================
df_customers.to_csv('ecom_customers.csv', index=False)
df_products.to_csv('products.csv', index=False)
df_orders.to_csv('ecom_orders.csv', index=False)
df_order_items.to_csv('order_items.csv', index=False)
df_returns.to_csv('returns.csv', index=False)

# Print summary
print("\n✅ DATASET GENERATED SUCCESSFULLY!")
print(f"📊 {len(df_customers)} customers")
print(f"📦 {len(df_products)} products")
print(f"🛒 {len(df_orders)} orders")
print(f"📝 {len(df_order_items)} order items")
print(f"↩️  {len(df_returns)} returns")

# Calculate total leakage
total_revenue = df_orders['total_revenue'].sum()
total_cost = df_orders['total_cost'].sum()
total_profit = df_orders['profit'].sum()
total_returns = df_returns['refund_amount'].sum()
discount_leakage = df_orders['discount_amount'].sum()
shipping_leakage = (df_orders['shipping_cost'] - df_orders['shipping_revenue']).sum()

print(f"\n💰 REVENUE METRICS:")
print(f"Total Revenue: ${total_revenue:,.2f}")
print(f"Total Cost: ${total_cost:,.2f}")
print(f"Total Profit: ${total_profit:,.2f}")
print(f"Profit Margin: {(total_profit/total_revenue*100):.1f}%")

print(f"\n🔴 LEAKAGE IDENTIFIED:")
print(f"Discount Leakage: ${discount_leakage:,.2f}")
print(f"Shipping Loss: ${shipping_leakage:,.2f}")
print(f"Returns Loss: ${total_returns:,.2f}")
print(f"TOTAL LEAKAGE: ${(discount_leakage + shipping_leakage + total_returns):,.2f}")
print(f"Leakage % of Revenue: {((discount_leakage + shipping_leakage + total_returns)/total_revenue*100):.1f}%")