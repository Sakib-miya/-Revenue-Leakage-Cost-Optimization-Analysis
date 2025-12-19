
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load data
customers = pd.read_csv('ecom_customers.csv')
products = pd.read_csv('products.csv')
orders = pd.read_csv('ecom_orders.csv')
items = pd.read_csv('order_items.csv')
returns = pd.read_csv('returns.csv')

# Convert dates
orders['order_date'] = pd.to_datetime(orders['order_date'])
returns['return_date'] = pd.to_datetime(returns['return_date'])

# ==============================================
# 1. REVENUE LEAKAGE BREAKDOWN (PIE CHART)
# ==============================================
leakage_sources = {
    'Excessive Discounts': orders[orders['discount_amount'] > 50]['discount_amount'].sum(),
    'Shipping Loss': (orders['shipping_cost'] - orders['shipping_revenue']).sum(),
    'Product Returns': returns['refund_amount'].sum(),
    'Negative Margin Orders': orders[orders['profit'] < 0]['profit'].abs().sum()
}

plt.figure(figsize=(10, 7))
colors = ['#ff6b6b', '#ee5a6f', '#f06595', '#cc5de8']
explode = (0.1, 0, 0, 0)
plt.pie(leakage_sources.values(), labels=leakage_sources.keys(), autopct='%1.1f%%',
        colors=colors, explode=explode, startangle=90)
plt.title('Revenue Leakage by Source\nTotal Leakage: ${:,.0f}'.format(sum(leakage_sources.values())), 
          fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('leakage_breakdown.png', dpi=300)
plt.show()

# ==============================================
# 2. DISCOUNT DISTRIBUTION ANALYSIS
# ==============================================
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Histogram of discount amounts
axes[0].hist(orders['discount_amount'], bins=30, color='coral', edgecolor='black', alpha=0.7)
axes[0].axvline(orders['discount_amount'].median(), color='red', linestyle='--', 
                label=f'Median: ${orders["discount_amount"].median():.2f}')
axes[0].set_title('Distribution of Discount Amounts per Order', fontsize=12, fontweight='bold')
axes[0].set_xlabel('Discount Amount ($)')
axes[0].set_ylabel('Number of Orders')
axes[0].legend()
axes[0].grid(axis='y', alpha=0.3)

# Discount by segment
segment_discount = orders.groupby('segment')['discount_amount'].mean().sort_values(ascending=False)
axes[1].barh(segment_discount.index, segment_discount.values, color='steelblue')
axes[1].set_title('Average Discount by Customer Segment', fontsize=12, fontweight='bold')
axes[1].set_xlabel('Average Discount ($)')
for i, v in enumerate(segment_discount.values):
    axes[1].text(v + 1, i, f'${v:.2f}', va='center')

plt.tight_layout()
plt.savefig('discount_analysis.png', dpi=300)
plt.show()

# ==============================================
# 3. UNPROFITABLE CUSTOMERS HEATMAP
# ==============================================
customer_metrics = orders.groupby('customer_id').agg({
    'profit': 'sum',
    'order_id': 'count',
    'discount_amount': 'sum'
}).reset_index()

customer_metrics = customer_metrics.merge(customers[['customer_id', 'segment']], on='customer_id')

# Top 20 most unprofitable
unprofitable = customer_metrics.nsmallest(20, 'profit')

plt.figure(figsize=(12, 8))
pivot = unprofitable.pivot_table(index='customer_id', values=['profit', 'discount_amount'], aggfunc='sum')
sns.heatmap(pivot, annot=True, fmt='.0f', cmap='RdYlGn_r', center=0, cbar_kws={'label': 'Amount ($)'})
plt.title('Top 20 Most Unprofitable Customers', fontsize=14, fontweight='bold')
plt.xlabel('Metric')
plt.ylabel('Customer ID')
plt.tight_layout()
plt.savefig('unprofitable_customers.png', dpi=300)
plt.show()

# ==============================================
# 4. RETURN RATE BY CATEGORY
# ==============================================
items_with_returns = items.merge(returns, on='order_id', how='left')
items_with_returns['returned'] = items_with_returns['refund_amount'].notna()

return_by_category = items_with_returns.groupby('category').agg({
    'order_id': 'count',
    'returned': 'sum'
}).reset_index()
return_by_category['return_rate'] = (return_by_category['returned'] / return_by_category['order_id'] * 100)

plt.figure(figsize=(10, 6))
bars = plt.bar(return_by_category['category'], return_by_category['return_rate'], 
               color=['red' if x > 15 else 'orange' if x > 10 else 'green' 
                      for x in return_by_category['return_rate']])
plt.axhline(y=15, color='red', linestyle='--', label='Critical Threshold (15%)')
plt.title('Return Rate by Product Category', fontsize=14, fontweight='bold')
plt.xlabel('Category')
plt.ylabel('Return Rate (%)')
plt.xticks(rotation=45)
plt.legend()
plt.grid(axis='y', alpha=0.3)
for i, v in enumerate(return_by_category['return_rate']):
    plt.text(i, v + 0.5, f'{v:.1f}%', ha='center', fontweight='bold')
plt.tight_layout()
plt.savefig('return_rate_by_category.png', dpi=300)
plt.show()

# ==============================================
# 5. PROFIT MARGIN BY SEGMENT (BOX PLOT)
# ==============================================
plt.figure(figsize=(10, 6))
orders['profit_margin'] = (orders['profit'] / orders['total_revenue'] * 100)
sns.boxplot(data=orders, x='segment', y='profit_margin', palette='Set2')
plt.axhline(y=0, color='red', linestyle='--', linewidth=2, label='Break-even')
plt.title('Profit Margin Distribution by Customer Segment', fontsize=14, fontweight='bold')
plt.xlabel('Customer Segment')
plt.ylabel('Profit Margin (%)')
plt.xticks(rotation=45)
plt.legend()
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('profit_margin_by_segment.png', dpi=300)
plt.show()

# ==============================================
# 6. SHIPPING LOSS ANALYSIS
# ==============================================
orders['shipping_loss'] = orders['shipping_cost'] - orders['shipping_revenue']
orders['subtotal_bucket'] = pd.cut(orders['subtotal'], 
                                   bins=[0, 50, 100, 200, 500, 10000],
                                   labels=['$0-50', '$50-100', '$100-200', '$200-500', '$500+'])

shipping_analysis = orders.groupby('subtotal_bucket').agg({
    'shipping_loss': ['mean', 'sum', 'count']
}).round(2)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Average shipping loss by order value
axes[0].bar(range(len(shipping_analysis)), shipping_analysis[('shipping_loss', 'mean')], 
            color='salmon', edgecolor='black')
axes[0].set_xticks(range(len(shipping_analysis)))
axes[0].set_xticklabels(shipping_analysis.index, rotation=45)
axes[0].set_title('Avg Shipping Loss by Order Value', fontsize=12, fontweight='bold')
axes[0].set_xlabel('Order Subtotal Range')
axes[0].set_ylabel('Average Shipping Loss ($)')
axes[0].axhline(y=0, color='green', linestyle='--', linewidth=2)
axes[0].grid(axis='y', alpha=0.3)

# Total shipping loss
axes[1].barh(range(len(shipping_analysis)), shipping_analysis[('shipping_loss', 'sum')], 
             color='coral')
axes[1].set_yticks(range(len(shipping_analysis)))
axes[1].set_yticklabels(shipping_analysis.index)
axes[1].set_title('Total Shipping Loss by Order Value', fontsize=12, fontweight='bold')
axes[1].set_xlabel('Total Shipping Loss ($)')
for i, v in enumerate(shipping_analysis[('shipping_loss', 'sum')]):
    axes[1].text(v + 100, i, f'${v:.0f}', va='center')

plt.tight_layout()
plt.savefig('shipping_loss_analysis.png', dpi=300)
plt.show()

print("✅ All visualizations saved!")

# ==============================================
# 7. GENERATE SUMMARY STATISTICS
# ==============================================
print("\n" + "="*60)
print("REVENUE LEAKAGE ANALYSIS - KEY METRICS")
print("="*60)

total_revenue = orders['total_revenue'].sum()
total_profit = orders['profit'].sum()
total_leakage = sum(leakage_sources.values())

print(f"\n💰 REVENUE OVERVIEW:")
print(f"Total Revenue: ${total_revenue:,.2f}")
print(f"Total Profit: ${total_profit:,.2f}")
print(f"Overall Margin: {(total_profit/total_revenue*100):.1f}%")

print(f"\n🔴 TOTAL LEAKAGE: ${total_leakage:,.2f}")
print(f"Leakage as % of Revenue: {(total_leakage/total_revenue*100):.1f}%")

print(f"\n📊 LEAKAGE BREAKDOWN:")
for source, amount in leakage_sources.items():
    print(f"  {source}: ${amount:,.2f} ({amount/total_leakage*100:.1f}%)")

print(f"\n🎯 SEGMENTS AT RISK:")
segment_stats = orders.groupby('segment').agg({
    'profit': ['sum', 'mean'],
    'order_id': 'count'
}).round(2)
print(segment_stats)

print(f"\n↩️  RETURN STATISTICS:")
print(f"Total Returns: {len(returns)}")
print(f"Return Rate: {(len(returns)/len(orders)*100):.1f}%")
print(f"Total Refunded: ${returns['refund_amount'].sum():,.2f}")
