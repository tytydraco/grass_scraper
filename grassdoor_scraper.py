import requests
import sqlite3
import sys

if len(sys.argv) <= 1:
    print('Missing argument for zipcode.')
    exit(1)
ZIPCODE = sys.argv[1]

con = sqlite3.connect('grass.db')
cur = con.cursor()

cur.execute('DROP TABLE listing;')
con.commit()

cur.execute(
'''CREATE TABLE IF NOT EXISTS listing(
    product_id INTEGER PRIMARY KEY,
    product_name TEXT NOT NULL,
    brands TEXT,
    category TEXT NOT NULL,
    original_price REAL NOT NULL,
    price REAL NOT NULL,
    weight REAL,
    weight_unit TEXT,
    strain TEXT,
    menu TEXT,
    thc_percent TEXT,
    has_deal INTEGER DEFAULT 0
);''')

def scrape_products(url):
    req = requests.get(url)
    result = req.json()

    for item in result['categories']:
        product_id = item['product_id']

        if not product_id:
            continue

        product_name = item['product_name']
        brands = ', '.join(item['brands'])
        category = item['category_name']
        original_price = item['price_without_deal']
        price = item['price']
        weight = item['product_weight']
        weight_unit = item['product_unit']
        strain = item['product_strain_type_name']

        asap = item['asap']
        schedule = item['schedule']

        menu = None
        if asap == 1:
            menu = 'asap'
        elif schedule == 1:
            menu = 'schedule'

        thc_percentage = None
        for attr in item['product_attributes']:
            if attr['name'] == 'THC':
                thc_percentage = attr['value']
                break

        has_deal = item['is_deal_available']

        sql = f'''INSERT OR IGNORE INTO listing VALUES(
            ?,
            ?,
            ?,
            ?,
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
            weight_unit,
            strain,
            menu,
            thc_percentage,
            has_deal,
        )
        print(values)
        cur.execute(sql, values)

    con.commit()

scrape_products(f'https://api.grassdoor.com/api/v1/products/{ZIPCODE}')
scrape_products(f'https://api.grassdoor.com/api/v1/products/schedule/{ZIPCODE}')