import requests
import sqlite3
import sys

con = sqlite3.connect('rebud.db')
cur = con.cursor()

cur.execute(
    '''CREATE TABLE IF NOT EXISTS listing(
    product_id INTEGER,
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

req = requests.post('https://ms.logickit.io/hydra-api/search',
                    headers={'X-Logickit-Store': 'www.rebud.com'})
result = req.json()

for item in result['list']:
    product_id = item['id']
    product_name = item['name']
    brands = item['brand']
    category = item['product_type']
    original_price = item['unit_price']
    price = item['sales_price'] if item['sales_price'] else original_price
    weight = str(item['net_weight']) + ' ' + item['net_weight_g']
    strain = item['product_type_name']

    sql = f'''INSERT INTO listing VALUES(
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
        brands,
        category,
        original_price,
        price,
        weight,
        strain,
    )
    print(values)
    cur.execute(sql, values)

con.commit()
