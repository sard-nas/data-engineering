from bs4 import BeautifulSoup
import csv

with open('text_5_var_74', encoding='utf-8') as file:
    text = file.read()
    soup = BeautifulSoup(text, 'html.parser')
    result = []
    
    rows = soup.find_all('tr')[1:]
    for row in rows:
        elements = row.find_all('td')
        item = {
            'company': elements[0].text,
            'contact': elements[1].text,
            'country': elements[2].text,
            'price': elements[3].text,
            'item': elements[4].text
        }
        result.append(item)

with open('text_5_output', 'w', encoding='utf-8', newline='') as output:
    writer = csv.writer(output,delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for item in result:
        writer.writerow(item.values())
