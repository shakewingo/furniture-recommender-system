import os
import logging
import json
from pathlib import Path
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
from pdt_link_scraper import categories

ROOT = os.environ.get("ROOT")
for i in range(len(categories)):
    with open(Path(ROOT, 'links_cat_{}.json'.format(i))) as file:
        f = json.load(file)
        logging.info('Category {} has number of records {}'.format(f['category'], len(f['link'])))


