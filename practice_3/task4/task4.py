from bs4 import BeautifulSoup
import json

def parse_file(filename: str) -> list:
    with open(filename, encoding='utf-8') as file:
        text = file.read()
    soup = BeautifulSoup(text, 'xml')
    info = list()
    products = soup.find_all('clothing')
    for product in products:
        product_info = {
            'id': int(product.find('id').get_text()),
            'name': product.find('name').get_text().strip(),
            'category': product.find('category').get_text().strip(),
            'size': product.find('size').get_text().strip(),
            'color': product.find('color').get_text().strip(),
            'material': product.find('material').get_text().strip(),
            'price': int(product.find('price').get_text().strip()),
            'rating': float(product.find('rating').get_text().strip()),
            'reviews': int(product.find('reviews').get_text().strip()),
        }
        if product.find('new'):
            product_info['new'] = product.find('new').get_text().strip() == '+'
        if product.find('exclusive'):
            product_info['exclusive'] = product.find('exclusive').get_text().strip()  == 'yes'
        if product.find('sporty'):
            product_info['sporty'] = product.find('sporty').get_text().strip() == 'yes'
        info.append(product_info)
    return info

product_data = list()
for i in range(1,101):
    filename = f"data_4/{i}.xml"
    product_data += parse_file(filename)

product_data = sorted(product_data, key=lambda x: x['id'])
with open('result.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(product_data, ensure_ascii=False))

filtered_data = list(filter(lambda x: x['rating'] > 4, product_data))         
with open('result_filtered.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(filtered_data, ensure_ascii=False))

prices = list(map(lambda x: x['price'], product_data))         
prices_stat = {
    'prices_sum': sum(prices),
    'prices_max': max(prices),
    'prices_min': min(prices),
    'prices_average': round(sum(prices)/len(prices), 2)
}
with open('price_statistic.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(prices_stat))

category = list(map(lambda x: x['category'], product_data))
freq = {}
for item in category:
    if item in freq:
        freq[item] += 1
    else:
        freq[item] = 1
with open('category_frequency.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(freq, ensure_ascii=False))