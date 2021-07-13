# Furniture.ca Living Room Products Scrapper

# To use phantomjs via selenium, you need:
# 1) Install NodeJS: brew install node or https://nodejs.org/en/
# 2) Using Node's package manager install NodeJS: npm -g install phantomjs-prebuilt (admin access)

import os
import logging
import json
import re
from time import sleep
from random import randint
from pathlib import Path
from selenium import webdriver
from bs4 import BeautifulSoup
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
logging.basicConfig(format='%(asctime)s - %(filename)s - %(message)s', level=logging.INFO)

ROOT = os.environ.get("ROOT")
# main_folder = Path(ROOT, 'Algorithm')
domain = 'www.furniture.ca'
item_per_page = 24  # specifically for this web
categories = ['living-room-packages', 'sofas', 'loveseats', 'sectionals', 'chairs-chaises', 'recliners',
              'ottomans-benches', 'cabinets-shelving', 'tv-stands-tv-mounts', 'coffee-tables',
              'sofa-console-tables', 'end-accent-tables']  # specifically for this web


def main():
    for k, j in enumerate(categories):
        cat = j
        cat_links = []
        logging.info('Start scraping category {}'.format(cat))
        # NOTE : There's chance that some elements are non available each time, due to unsure reason
        # (visibility setting / waiting certain element to load page). Besides, some category will have less data
        # SOLUTION: Change while i <= iters to run each request for multiple times
        i = 0  # set # of trials
        offset = item_per_page  # based on certain website format
        while i <= 2: #10
            logging.info('Start iteration {}'.format(i))
            logging.info('Start offset {}'.format(offset))
            # TODO: selenium depreation warning
            link = 'https://www.furniture.ca/collections/furniture-living-room-' + cat + '?offset=' + str(offset)
            driver = webdriver.PhantomJS(
                executable_path='/usr/local/lib/node_modules/phantomjs-prebuilt/lib/phantom/bin/phantomjs')
            rdm = randint(10, 36)
            driver.get(link)
            page = BeautifulSoup(driver.page_source, 'html.parser')
            r = re.compile(r'myshopify.com/products')  # specifically for this web
            for a in page.findAll('a', href=r):
                # find link
                link = a['href']
                # check if link is new
                if link not in cat_links:
                    logging.info('Found new link {}'.format(link))
                    cat_links.append(link)
                else:
                    logging.warning('Found link already exists so skipped')

            # check if good to go to next page
            if (len(cat_links) % item_per_page == 0) and (len(cat_links) != 0):
                offset += item_per_page
            i += 1
            logging.info('Collected {} items'.format(len(cat_links)))
            sleep(rdm)

        # write json file
        product_link = {'category': cat, 'link': cat_links}
        with open(Path(ROOT, 'links_cat_{}.json'.format(k)), 'w') as outfile:
            json.dump(product_link, outfile)
        logging.info('Finish scraping category {}'.format(cat))

    # combine all category links
    logging.info('Start combining all category links')
    product_links = []
    for i in range(0, len(categories)):
        with open(Path(ROOT, 'links_cat_{}.json'.format(i))) as outfile:
            f = json.load(outfile)
            product_links.append(f)
    with open(Path(ROOT, 'product_links.json'), 'w') as outfile:
        json.dump(product_links, outfile)
    logging.info('Finish combining all category links')


if __name__ == "__main__":
    main()
