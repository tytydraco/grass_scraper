import sqlite3
import sys
import rebud_scraper as rebud
import flowerco_scraper as flowerco
import grassdoor_scraper as grass

if len(sys.argv) <= 1:
    print('Missing argument for zipcode.')
    exit(1)
zipcode = sys.argv[1]

con = sqlite3.connect('listings.db')
cur = con.cursor()

cur.execute(
    '''CREATE TABLE IF NOT EXISTS listing(
    website TEXT NOT NULL,
    product_id TEXT NOT NULL,
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

grass.scrape(zipcode)
flowerco.scrape()
rebud.scrape()
