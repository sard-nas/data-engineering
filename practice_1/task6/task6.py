#link: https://www.coinlore.com/cryptocurrency-data-api

import requests, json
from bs4 import BeautifulSoup

url = "https://api.coinlore.net/api/tickers/?start=0&limit=3"

response = requests.get(url)
data = json.loads(response.text)

markup = """<table>
    <tr>
        <th>id</th>
        <th>symbol</th>
        <th>name</th>
        <th>nameid</th>
        <th>rank</th>
        <th>price_usd</th>
        <th>percent_change_24h</th>
        <th>percent_change_1h</th>
        <th>percent_change_7d</th>
        <th>price_btc</th>
        <th>market_cap_usd</th>
        <th>volume24</th>
        <th>volume24a</th>
        <th>csupply</th>
        <th>tsupply</th>
        <th>msupply</th>
    </tr>
</table>"""

soup = BeautifulSoup(markup,"html.parser")
table = soup.table
for row in data["data"]:
    tr = soup.new_tag("tr")
    for key, value in row.items():
        td = soup.new_tag("td")
        td.string = str(value)
        tr.append(td)
    table.append(tr)

with open('task6_result.html', 'w') as output:
    output.write(soup.prettify())