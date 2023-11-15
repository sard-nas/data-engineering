from bs4 import BeautifulSoup
import re
import json

def parse_file(filename: str) -> list:
    with open(filename, encoding='utf-8') as file:
        text = file.read()
    soup = BeautifulSoup(text, 'html.parser')
    info = list()
    products = soup.find_all('div', attrs={'class': 'product-item'})
    for product in products:
        product_info = {}
        product_info['id'] = int(product.find_all('a')[0]['data-id'])
        product_info['link'] = product.find_all('a')[1]['href']
        product_info['image'] = product.img['src']
        product_info['name'] = product.span.get_text().strip()
        product_info['price'] = int(product.price.get_text().replace(' ', '').replace('₽', ''))
        product_info['bonus'] = int(product.strong.get_text().replace('+ начислим', '').replace('бонусов', ''))

        params = product.ul.find_all('li')
        for param in params:
            product_info[param['type']] = param.get_text().strip()
        info.append(product_info)
    return info

product_data = list()
for i in range(1,88):
    filename = f"data_2/{i}.html"
    product_data += parse_file(filename)

product_data = sorted(product_data, key=lambda x: x['id'])
with open('result.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(product_data))

filtered_data = list(filter(lambda x: x['bonus'] > 2000, product_data))         
with open('result_filtered.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(filtered_data))

prices = list(map(lambda x: x['price'], product_data))         
prices_stat = {
    'prices_sum': sum(prices),
    'prices_max': max(prices),
    'prices_min': min(prices),
    'prices_average': round(sum(prices)/len(prices), 2)
}
with open('statistic.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(prices_stat))

matrix = list(map(lambda x: x.get('matrix', 'unknown'), product_data))
freq = {}
for item in matrix:
    if item in freq:
        freq[item] += 1
    else:
        freq[item] = 1
with open('matrix_frequency.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(freq))