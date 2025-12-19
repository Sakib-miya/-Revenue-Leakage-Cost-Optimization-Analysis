💰 Revenue Leakage & Cost Optimization Analysis (E-Commerce)
📌 Project Overview

This project is an end-to-end Revenue Leakage and Cost Optimization analysis for a mid-size e-commerce business.

The objective of this project is to identify hidden profit losses, understand why revenue is leaking, and provide data-driven recommendations to improve profitability.

This project demonstrates how a data analyst:

Simulates real business problems

Builds realistic datasets

Performs deep analysis using SQL and Python

Communicates insights using clear visualizations

All data used in this project is synthetic (mock data) but designed to closely mimic real-world e-commerce behavior.

🎯 Business Questions Answered

How much revenue is being lost due to excessive discounts?

Which customer segments are unprofitable?

How much money is lost through returns and refunds?

Is the shipping policy causing losses?

Which products and categories suffer from margin erosion?

What percentage of total revenue is leaking?

🧱 Data Used (Synthetic E-Commerce Data)

All datasets were generated using Python to simulate a realistic e-commerce environment.

📁 Dataset Files

ecom_customers.csv – Customer details (segment, acquisition channel, join date)

products.csv – Product catalog with category, cost price, standard price, and weight

ecom_orders.csv – Order-level revenue, discounts, shipping cost, and profit

order_items.csv – Item-level pricing, discounts, and costs

returns.csv – Returned orders with refund amount and return reason

📊 Data Scale

3,000 customers

200 products

8,000 orders

Multiple customer segments and acquisition channels

⚙️ Dataset Generation Logic (Python)

📄 File: dataset_generator.py

The dataset was intentionally designed with built-in revenue leakage scenarios to reflect real business issues:

Embedded Leakage Scenarios

Discount Abuse

“Bargain Hunter” customers receive heavy discounts (25–45%)

No discount strategy or control

Unprofitable Shipping

Shipping cost based on product weight

Free shipping threshold set too low ($50)

High Product Returns

15% return rate

No restocking fee

Refunds include avoidable reasons like “Found Cheaper”

Low-Margin Products

Electronics category has lower margins

Discounts further reduce profitability

This makes the dataset realistic and suitable for revenue leakage analysis.

🔍 Analysis Performed
1️⃣ Revenue Leakage Quantification

Discount leakage

Shipping losses

Refund losses from returns

Losses from negative-margin orders

Leakage calculated as a percentage of total revenue

2️⃣ Discount Abuse Analysis

Average discount by customer segment

Identification of customers abusing discounts

High-discount order rate analysis

3️⃣ Customer & Segment Profitability

Profit calculated at order and customer level

Identification of loss-making segments

Segment-level profit margins

4️⃣ Product & Category Margin Erosion

Standard margin vs actual margin

Impact of discounts on product profitability

Identification of low-margin products

5️⃣ Returns Analysis

Return rate by product category

Financial impact of refunds

Identification of preventable returns

6️⃣ Shipping Cost Analysis

Shipping loss by order value bucket

Average and total shipping loss

Identification of unprofitable shipping ranges

7️⃣ Channel ROI Analysis

Revenue and profit by acquisition channel

Channel-level profit margins

📊 Visualizations (Matplotlib & Seaborn)

This project uses Python-based visualizations for analysis and storytelling.

Visual Outputs

Revenue leakage breakdown (pie chart)

Discount distribution and segment comparison

Top unprofitable customers heatmap

Return rate by product category

Profit margin distribution by customer segment

Shipping loss analysis by order value

Generated image files include:

leakage_breakdown.png

discount_analysis.png

unprofitable_customers.png

return_rate_by_category.png

profit_margin_by_segment.png

shipping_loss_analysis.png

⚠️ Transparency & Attribution

The Matplotlib and Seaborn visualization code used in this project was generated with the assistance of Claude (Anthropic AI).

I personally:

Designed the business problem

Built the dataset generation logic

Defined all revenue leakage scenarios

Wrote and executed SQL analysis

Verified and interpreted results

Wrote all insights and documentation

This disclosure is included for ethical transparency.

🗄 SQL Analysis

SQL was used to perform detailed analysis, including:

Total revenue leakage by source

Discount abuse detection

Unprofitable customer segment analysis

High-return product identification

Product margin erosion

Shipping loss analysis

Acquisition channel ROI analysis

All SQL queries are included in a single SQL file and use:

CTEs

Aggregations

Conditional logic

Business-focused metrics

📸 Dashboard / Visualization Images (Add Here)


<img width="4200" height="1500" alt="discount_analysis" src="https://github.com/user-attachments/assets/70bb2380-e8be-4429-857f-4dbc17d3c4ab" />
<img width="3000" height="1800" alt="return_rate_by_category" src="https://github.com/user-attachments/assets/b394d219-966b-425c-8c9c-e144191ac530" />

<img width="3000" height="2100" alt="leakage_breakdown" src="https://github.com/user-attachments/assets/c1a7b860-8629-442b-a25b-4d167d2d9f60" />
<img width="4200" height="1500" alt="shipping_loss_analysis" src="https://github.com/user-attachments/assets/bb73f685-8767-4574-b0ef-77456beadb02" />

<img width="3000" height="1800" alt="profit_margin_by_segment" src="https://github.com/user-attachments/assets/26257a3c-9022-4ba0-9b65-25b9a983ecf7" />
<img width="3600" height="2400" alt="unprofitable_customers" src="https://github.com/user-attachments/assets/e666da03-2d4b-4945-ba86-a6f40f95d274" />



📌 Key Findings

A significant portion of revenue is lost due to discount abuse

“Bargain Hunter” customers contribute low or negative profit

Free shipping threshold is too low and causes consistent shipping losses

Product returns represent a major leakage source

Electronics products suffer the most from margin erosion

💡 Business Recommendations

Limit blanket discounts and target high-value customers

Increase free shipping threshold

Introduce restocking fees for non-defective returns

Improve product descriptions to reduce avoidable returns

Closely monitor discount-heavy customers

🚀 Future Improvements

Build an interactive Power BI dashboard

Add customer lifetime profitability modeling

Simulate pricing and shipping policy changes

Implement anomaly detection for discount abuse

💼 Why This Project Matters

This project demonstrates:

Real-world revenue and profitability analysis

Strong Python and SQL skills

Business-focused thinking

Visualization-driven storytelling

Ethical AI usage transparency
