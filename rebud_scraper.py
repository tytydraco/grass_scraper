import requests
import sqlite3


def scrape():
    con = sqlite3.connect('listings.db')
    cur = con.cursor()

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
            ?,
            ?
        );'''

        values = (
            'REBUD',
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


if __name__ == '__main__':
    scrape()
