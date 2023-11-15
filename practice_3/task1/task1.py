from bs4 import BeautifulSoup
import re
import json

def parse_file(filename: str) -> dict:
    with open(filename, encoding='utf-8') as file:
        text = file.read()
    soup = BeautifulSoup(text, 'html.parser')
    info = {}
    info['category'] = soup.find_all('span', string=re.compile('Категория:'))[0].get_text().replace('Категория:', '').strip()
    info['book title'] = soup.find_all("h1", attrs={"class": "book-title"})[0].get_text().strip().strip()
    info['author'] = soup.find_all('p', attrs={'class': 'author-p'})[0].get_text().strip()
    info['pages'] = int(soup.find_all('span', attrs={'class': 'pages'})[0].get_text().split()[1])        
    info['year'] = int(soup.find_all('span', attrs={'class': 'year'})[0].get_text().split()[-1])
    info['ISBN'] = soup.find_all('span', string=re.compile('ISBN:'))[0].get_text().split(':')[1].strip()
    info['description'] = soup.find_all('p', string=re.compile('Описание'))[0].get_text().replace('Описание', '').strip()
    info['image'] = soup.find_all('img')[0]['src']
    info['rating'] = float(soup.find_all('span', string=re.compile('Рейтинг:'))[0].get_text().replace('Рейтинг:', ''))
    info['views'] = int(soup.find_all('span', string=re.compile('Просмотры:'))[0].get_text().replace('Просмотры:', ''))
    return info

book_data = list()
for i in range(1,1000):
    filename = f"data_1/{i}.html"
    book_data.append(parse_file(filename))

book_data = sorted(book_data, key=lambda x: x['rating'], reverse=True)
with open('result.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(book_data, ensure_ascii=False))

filtered_data = list(filter(lambda x: x['year'] > 2000, book_data))         
with open('result_filtered.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(filtered_data, ensure_ascii=False))

views = list(map(lambda x: x['views'], book_data))         
views_stat = {
    'views_sum': sum(views),
    'views_max': max(views),
    'views_min': min(views),
    'views_average': round(sum(views)/len(views), 2)
}
with open('views_stat.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(views_stat, ensure_ascii=False))

categories = list(map(lambda x: x['category'], book_data))
freq = {}
for category in categories:
    if category in freq:
        freq[category] += 1
    else:
        freq[category] = 1
with open('categories_frequency.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(freq, ensure_ascii=False))