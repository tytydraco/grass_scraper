import sqlite3
import requests
from bs4 import BeautifulSoup

con = sqlite3.connect('flower.db')
cur = con.cursor()

cur.execute(
    '''CREATE TABLE IF NOT EXISTS listing(
    product_id TEXT PRIMARY KEY,
    product_name TEXT NOT NULL,
    brand TEXT,
    category TEXT NOT NULL,
    original_price REAL NOT NULL,
    price REAL NOT NULL,
    weight TEXT,
    strain TEXT
);''')

cur.execute('DELETE FROM listing;')
con.commit()


page = 0
while True:
    req = requests.get(
        f'https://flowercompany.com/search/json-results?start={page}')
    result = req.json()

    results = result['pageResults']
    if results == 0:
        break

    for html in result['products']:
        soup = BeautifulSoup(html, 'html.parser')

        product_id = soup.find('div', {'id': True}).attrs['id']
        product_name = str.strip(
            soup.find('a', ['product-card-product-name']).contents[0])
        brand = str.strip(
            soup.find('a', ['product-card-brand-url']).contents[0])

        category = soup.find('div', {'data-category': True})
        if category is None:
            category = 'other'
        else:
            category = category.attrs['data-category']

        original_price = soup.find(
            True, {'data-price-retail': True}).attrs['data-price-retail']
        price = soup.find(True, {'data-price': True}).attrs['data-price']

        weight = soup.find('span', ['product-card-thc'])
        if weight is not None:
            weight = weight.contents[0]

        strain = soup.find('div', ['product-type-text'])
        if strain is not None:
            strain = strain.contents[0]

        sql = f'''INSERT OR IGNORE INTO listing VALUES(
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?
        );'''

        values = (
            product_id,
            product_name,
            brand,
            category,
            original_price,
            price,
            weight,
            strain,
        )
        print(values)
        cur.execute(sql, values)

    con.commit()

    page += 1
