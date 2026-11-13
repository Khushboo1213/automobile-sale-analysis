"""
Automobile Sales Data Analysis
Run: python src/analyze_sales.py
Dataset is illustrative synthetic practice data, not actual Maruti Suzuki data.
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "automobile_sales_sample.csv"
OUTPUT_DIR = ROOT / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

# 1. Load the CSV file
sales = pd.read_csv(DATA_FILE)

# 2. Inspect and clean the data
sales["Date"] = pd.to_datetime(sales["Date"], errors="coerce")
sales = sales.drop_duplicates()
sales = sales.dropna(subset=["Date", "Model", "Region", "Units_Sold", "Unit_Price_INR"])
sales["Units_Sold"] = pd.to_numeric(sales["Units_Sold"], errors="coerce")
sales["Unit_Price_INR"] = pd.to_numeric(sales["Unit_Price_INR"], errors="coerce")
sales = sales.dropna(subset=["Units_Sold", "Unit_Price_INR"])
sales["Revenue_INR"] = sales["Units_Sold"] * sales["Unit_Price_INR"]
sales["Month"] = sales["Date"].dt.to_period("M").astype(str)

# 3. Calculate headline metrics
total_units = int(sales["Units_Sold"].sum())
total_revenue = sales["Revenue_INR"].sum()
average_unit_price = sales["Unit_Price_INR"].mean()
print(f"Total units sold: {total_units:,}")
print(f"Total revenue: Rs. {total_revenue:,.0f}")
print(f"Average unit price: Rs. {average_unit_price:,.0f}")

# 4. Group data to answer business questions
model_summary = sales.groupby("Model")["Units_Sold"].sum().sort_values(ascending=False)
region_summary = sales.groupby("Region")["Revenue_INR"].sum().sort_values(ascending=False)
monthly_summary = sales.groupby("Month")["Units_Sold"].sum()
category_summary = sales.groupby("Category")["Units_Sold"].sum().sort_values(ascending=False)

print("\\nTop-selling model:", model_summary.index[0])
print("Highest-revenue region:", region_summary.index[0])

# 5. Save summary tables
model_summary.to_csv(OUTPUT_DIR / "model_sales_summary.csv")
region_summary.to_csv(OUTPUT_DIR / "regional_revenue_summary.csv")
monthly_summary.to_csv(OUTPUT_DIR / "monthly_sales_summary.csv")

# 6. Create a four-chart dashboard
fig, axes = plt.subplots(2, 2, figsize=(13, 8))
fig.suptitle("Automobile Sales Analysis Dashboard - Sample Data", fontsize=15, fontweight="bold")

model_summary.plot(kind="bar", ax=axes[0, 0], title="Units Sold by Model")
axes[0, 0].set_ylabel("Units")
axes[0, 0].tick_params(axis="x", rotation=25)

(region_summary / 10_000_000).plot(kind="bar", ax=axes[0, 1], title="Revenue by Region")
axes[0, 1].set_ylabel("Revenue (Rs. crore)")

monthly_summary.plot(kind="line", marker="o", ax=axes[1, 0], title="Monthly Units Sold")
axes[1, 0].set_ylabel("Units")
axes[1, 0].tick_params(axis="x", rotation=45)

category_summary.plot(kind="bar", ax=axes[1, 1], title="Units Sold by Category")
axes[1, 1].set_ylabel("Units")

plt.tight_layout()
plt.savefig(OUTPUT_DIR / "sales_dashboard.png", dpi=160, bbox_inches="tight")
print("\\nDashboard saved to outputs/sales_dashboard.png")
