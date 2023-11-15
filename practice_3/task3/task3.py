from bs4 import BeautifulSoup
import re
import json

def parse_file(filename: str) -> dict:
    with open(filename, encoding='utf-8') as file:
        text = file.read()
    soup = BeautifulSoup(text, 'xml')
    info = {
        'name': soup.find_all('name')[0].get_text().strip(),
        'constellation': soup.find_all('constellation')[0].get_text().strip(),
        'spectral-class': soup.find_all('spectral-class')[0].get_text().strip(),
        'radius': int(soup.find_all('radius')[0].get_text()),
        'rotation': float(soup.find_all('rotation')[0].get_text().split()[0].strip()),
        'age': float(soup.find_all('age')[0].get_text().split()[0].strip()),
        'distance': float(soup.find_all('distance')[0].get_text().split()[0].strip()),
        'absolute-magnitude': float(soup.find_all('absolute-magnitude')[0].get_text().split()[0].strip()),
    }
    return info

star_data = list()
for i in range(1, 501):
    filename = f"data_3/{i}.xml"
    star_data.append(parse_file(filename))

star_data = sorted(star_data, key=lambda x: x['age'], reverse=True)
with open('result.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(star_data, ensure_ascii=False))

filtered_data = list(filter(lambda x: x['radius'] > 500000000, star_data))         
with open('result_filtered.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(filtered_data, ensure_ascii=False))

distances = list(map(lambda x: x['distance'], star_data))         
distance_stat = {
    'distance_sum': round(sum(distances), 2),
    'distance_max': round(max(distances), 2),
    'distance_min': round(min(distances), 2),
    'distance_average': round(sum(distances)/len(distances), 4)
}
with open('distances_stat.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(distance_stat, ensure_ascii=False))

constellations = list(map(lambda x: x['constellation'], star_data))
freq = {}
for item in constellations:
    if item in freq:
        freq[item] += 1
    else:
        freq[item] = 1

with open('constellations_frequency.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(freq, ensure_ascii=False))