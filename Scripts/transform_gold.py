import pandas as pd
import os 

### Using os module to fetch the dir name and input file path

transform_gold_dir = os.path.dirname(os.path.abspath(__file__))

input_file_path = os.path.join(transform_gold_dir,"..","data","processed","clean_bitcoin_market_data.csv")

output_file_path = os.path.join(transform_gold_dir,"..","data","processed","bitcoin_monthly_metrics.csv")


### Loading csv into Dataframe
gold_df = pd.read_csv(input_file_path, parse_dates=["date"])

print(gold_df.head(5))

#### Create Year-Month Key 

gold_df["YearMonth"] = gold_df["date"].dt.to_period("M").dt.to_timestamp()




### Monthly aggregation (Gold Tables)
### Monthly average price

monthly_price = gold_df.groupby("YearMonth")["price"].mean().reset_index().rename(columns={"price":"avg_price"})

### Monthly average market cap

monthly_caps = gold_df.groupby("YearMonth")["market_caps"].mean().reset_index().rename(columns={"market_caps":"avg_market_caps"})

### Monthly volumes

monthly_volumes = gold_df.groupby("YearMonth")["total_volumes"].mean().reset_index().rename(columns={"total_volumes":"avg_total_volumes"})


#### Combine this 3 averages into gold table

monthly_gold = (
    monthly_price.merge(monthly_caps, on="YearMonth").merge(monthly_volumes, on="YearMonth").sort_values("YearMonth")

)

#### Month-over-Month (MoM) comparison

monthly_gold["price_mom_pct"] = monthly_gold["avg_price"].pct_change() * 100
monthly_gold["market_cap_mom_pct"] = monthly_gold["avg_market_caps"].pct_change() * 100
monthly_gold["volumes_mom_pct"] = monthly_gold["avg_total_volumes"].pct_change() * 100

#### Saving the file into data/processed subfolder

monthly_gold.to_csv(output_file_path, index=False)
