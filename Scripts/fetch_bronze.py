import requests
import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("COINGECKO_API_KEY")

url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"

params = {
    "vs_currency" :  "usd",
    "days": "365",
    "interval": "daily"
}

headers = {"x-cg-demo-api-key": "CG-VYaqHPKj4sti98MmdpfZYe3c"}

response = requests.get(url, params=params, headers=headers)

data = response.json()


### Creating the file paths to save raw data under data/raw/bitcoin.json
fetch_bronze_dir = os.path.dirname(os.path.abspath(__file__))
print(fetch_bronze_dir)

target_dir = os.path.join(fetch_bronze_dir, "..", "data","raw")

print(target_dir)

os.makedirs(target_dir, exist_ok=True)

file_path = os.path.join(target_dir, "bitcoin_raw.json")

print(f"Saving data to: {os.path.abspath(file_path)}")

## Save the Raw JSON

with open(file_path, "w")as f:
    f.write(response.text)


### Convert prices, market_caps, total_voluems into Data Frame and merge them.

prices = pd.DataFrame(data["prices"], columns=["timestamp","price"])
market_caps = pd.DataFrame(data["market_caps"], columns=["timestamp","market_caps"])
total_volumes = pd.DataFrame(data["total_volumes"], columns=["timestamp","total_volumes"])

### Merge all 3 response

df = prices.merge(market_caps, on="timestamp").merge(total_volumes, on="timestamp")

df["date"] = pd.to_datetime(df["timestamp"], unit="ms")

df = df[["timestamp", "date", "price", "market_caps", "total_volumes"]]

# print(df.head(10))

### Save the dataframe into csv in data/raw

csv_path = os.path.join(target_dir, "bitcoin_market_data.csv")

df.to_csv(csv_path, index=False)