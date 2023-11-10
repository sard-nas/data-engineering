import os
import json
import msgpack

with open('products_74.json') as file:
    data = json.load(file)

prices = {}
for product in data:
    if product['name'] in prices.keys():
        prices[product['name']].append(product['price'])
    else:
        prices[product['name']] = [product['price'], ]

result = list()
for name, lst in prices.items():
    elem = {
        'name': name,
        'min': min(lst),
        'max': max(lst),
        'average': sum(lst) / len(lst)
    }
    result.append(elem)

with open('task3_result.json', 'w') as json_file:
    json_file.write(json.dumps(result))

with open('task3_result.msgpack', 'wb') as msgpack_file:
    msgpack_file.write(msgpack.dumps(result))
    
print(f"Size of json file:    {os.path.getsize('task3_result.json')}")
print(f"Size of msgpack file: {os.path.getsize('task3_result.msgpack')}")
