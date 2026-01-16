import pandas as pd
import matplotlib.pyplot as plt
import os 


transform_gold_dir = os.path.dirname(os.path.abspath(__file__))

input_file_path = os.path.join(transform_gold_dir,"..","data","processed","bitcoin_monthly_metrics.csv")

# Output file path for saving
output_file_path = os.path.join(transform_gold_dir,"..","data","processed")


### Reading the file in pandas

df = pd.read_csv(input_file_path)

#### Plotting the bar charts
#### Monthly Price change.

plt.bar(df["YearMonth"], df["avg_price"], color="blue", edgecolor="navy")
plt.xlabel("YearMonth")
plt.ylabel("Avg Price")
plt.title("Bitcoin Monthly Average Price")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(f"{output_file_path}/monthly_price_bar_chart.png")
          

### Plotting Monthly change and % change in line

fig, ax1 = plt.subplots(figsize=(10,6))

### Plot Bar Chart (Average Price)

ax1.bar(df["YearMonth"], df["avg_price"], color="blue", edgecolor="navy", alpha=0.7, label="Average Price")
ax1.set_xlabel("Year_Month")
ax1.set_ylabel("Average Price ($)", color="blue")
ax1.tick_params(axis='y', labelcolor='blue')

### Create second axis for line chart

ax2 = ax1.twinx()

### Plot line Chart (%change) with makers

ax2.plot(df["YearMonth"], df["price_mom_pct"], color="red", marker='o', linewidth=2, label="Monthly % change")
ax2.set_ylabel('Monthly % change (%)', color='red')
ax2.tick_params(axis='y', labelcolor='red')

### Final touches
plt.title('Average Price and Monthly % change')
ax1.set_xticklabels(df["YearMonth"], rotation=45)

### Combine legends from both axes

lines_1, labels1 = ax1.get_legend_handles_labels()
lines_2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines_1 + lines_2, labels1 + labels2, loc='upper left')

plt.tight_layout()
plt.savefig(f"{output_file_path}/price_and_pct_change_chart.png")