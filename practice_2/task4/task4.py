import json
import pickle

def change_price(price: float, method: str, param: float) -> float:
    methods = {
        'add': lambda x, y: x + y,
        'sub': lambda x, y: x - y,
        'percent+': lambda x, y: x + x * y,
        'percent-': lambda x, y: x - x * y
        }
    return methods[method](price, param)

with open("products_74.pkl", "rb") as f:
    data = pickle.load(f)

products = {}
for item in data:
    products[item['name']] = item['price']

with open("price_info_74.json") as f:
    price_info = json.load(f)

for price in price_info:
    products[price['name']] = change_price(products[price['name']], price['method'], price['param'])

result = []
for key, value in products.items():
    elem = {
        'name': key,
        'price': round(value, 2)
    }
    result.append(elem)

with open('updated_products.pkl', 'wb') as r_file:
    r_file.write(pickle.dumps(result))