import requests
import sqlite3


def scrape(zipcode):
    con = sqlite3.connect('listings.db')
    cur = con.cursor()

    def scrape_products(url):
        req = requests.get(url)
        result = req.json()

        for item in result['categories']:
            product_id = item['product_id']

            if not product_id:
                continue

            product_name = item['product_name']
            _brand = item['brands']
            brand = 'N/A'
            if _brand is not None:
                brand = ', '.join(_brand)
            category = item['category_name']
            original_price = item['price_without_deal']
            price = item['price']
            weight = item['product_weight'] + ' ' + item['product_unit']
            strain = item['product_strain_type_name']

            asap = item['asap']
            schedule = item['schedule']

            website = 'Grassdoor'
            if asap == 1:
                website = 'Grassdoor - ASAP'
            elif schedule == 1:
                website = 'Grassdoor - Schedule'

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
                website,
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

    scrape_products(f'https://api.grassdoor.com/api/v1/products/{zipcode}')
    scrape_products(
        f'https://api.grassdoor.com/api/v1/products/schedule/{zipcode}')


if __name__ == '__main__':
    scrape()
