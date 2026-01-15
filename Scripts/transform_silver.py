import pandas as pd
import os

### Using OS module to fetch Input file and setting up Output File path

### Moving into Scripts dir
transform_silver_dir = os.path.dirname(os.path.abspath(__file__))

### Moving into data/raw folder
input_file_path = os.path.join(transform_silver_dir,"..","data","raw","bitcoin_market_data.csv")

### Setting up output files
output_file_path = os.path.join(transform_silver_dir,"..","data","processed","clean_bitcoin_market_data.csv")

#### Cleaning and Transforming Raw Bronze Layer Data.
df = pd.read_csv(input_file_path, parse_dates=["date"])


### Checking duplicate dates. 
counts = df["date"].value_counts()

duplicates = counts[counts>1]
print(duplicates)

### If there are two same dates. Aggregate the Data.

if not duplicates.empty:
    df = (
        df.groupby("date").agg({
            "price": "mean",
            "market_caps": "mean",
            "total_volumes" : "sum"
        })
        .reset_index()
    )



### Build full day timeline and set them as index.

full_range = pd.date_range(df["date"].min(), df["date"].max(), freq= "D")

df = df.set_index("date").reindex(full_range)

### Filling missing vales
### Stock market on Leaves will carry the same price, same market cap and 0 volumes
### Volumes were number of stocks traded. On holiday no stock will be traded (buy/sell)


### Checking any missing price, market_caps and total_volumes column
missing_price = df[df["price"].isna()]

# print(missing_price)

missing_market_caps = df[df["market_caps"].isna()]

# print(missing_market_caps)

missing_total_volumes = df[df["total_volumes"].isna()]

# print(missing_total_volumes)

### General Cleaning strategy for missing data in price, market_caps and total_volumes

df["price"] = df["price"].ffill()
df["market_caps"] = df["market_caps"].ffill()
df["total_volumes"] = df["total_volumes"].fillna(0)

### Reset full range index as date

df = df.reset_index().rename(columns={"index":"date"})


### Validate sanity
### Python assert function. assert condition

### Find there is any negative values in price, market_caps and total_values

neg_values = (df[["price","market_caps","total_volumes"]] < 0).sum().sum()

### Try and except block
try:
    assert neg_values == 0, f"Found {neg_values} negative values"
    ### Saving the file in processed folder
    df.to_csv(output_file_path, index=False)
except AssertionError as e:
    print(f"There is an error: {e}")

