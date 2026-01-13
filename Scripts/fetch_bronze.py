import requests
import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("COINGECKO_API_KEY")

url = "https://api.coingecko.com/api/v3/simple/price?vs_currencies=usd&ids=bitcoin&names=Bitcoin&symbols=btc"


headers = {"x-cg-demo-api-key": "CG-VYaqHPKj4sti98MmdpfZYe3c"}

response = requests.get(url, headers=headers)

print(response.text)