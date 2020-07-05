import requests
import pandas as pd

API_KEY = '07df2195-191e-4843-9f2c-430b977339b4'
PRICE_LIMIT = 100000
UNITS = 320

data = requests.get(f'https://api.hypixel.net/skyblock/bazaar?key={API_KEY}').json()

products = list(data['products'].keys())
sell_price = []
buy_price = []
sell_volume = []
buy_volume = []
for product in products:
    sell_price.append(data['products'][product]['quick_status']['sellPrice'])
    buy_price.append(data['products'][product]['quick_status']['buyPrice'])
    sell_volume.append(data['products'][product]['quick_status']['sellVolume'])
    buy_volume.append(data['products'][product]['quick_status']['buyVolume'])

bazaar_df = pd.DataFrame({"item": products, "sell_price": sell_price, "buy_price": buy_price, "sell_volume": sell_volume, "buy_volume": buy_volume})
bazaar_df['margin_pct'] = ((bazaar_df['buy_price'] - bazaar_df['sell_price']) / bazaar_df['sell_price']) * 100
bazaar_df['flip_score'] = bazaar_df['margin_pct'] * bazaar_df['buy_volume'] / bazaar_df['sell_volume']
# bazaar_df['flip_score'] = bazaar_df['margin_pct'] * bazaar_df['sell_volume']
bazaar_df.sort_values(by='flip_score', ascending=False, inplace=True)


print(bazaar_df.head(20))