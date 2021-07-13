# Furniture.ca Living Room Products Scrapper

# Ensure python has CA certificate:
# https://stackoverflow.com/questions/42982143/python-requests-how-to-use-system-ca-certificates-debian-ubuntu

import csv
import json
import os
import re
import time
import logging
from pathlib import Path
import urllib
from urllib.request import urlretrieve
import numpy as np
import requests
import certifi
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from bs4 import BeautifulSoup
from dotenv import load_dotenv, find_dotenv
import tensorflow
from pdt_link_scraper import categories

load_dotenv(find_dotenv())
logging.basicConfig(format='%(asctime)s - %(filename)s - %(message)s', level=logging.INFO)

ROOT = os.environ.get("ROOT")
meta_folder = Path(ROOT, 'Meta_org')
delays = [7, 4, 6, 2, 10, 19]


# To avoid being blocked: consider user agent / referers / proxy IPs / delays

# def get_random_ua():
#     random_ua = ''
#     ua_file = '/Users/yingyao/Desktop/Projects/CQADS/Recommender System/Meta/Chrome_UA.txt'
#     try:
#         with open(ua_file) as f:
#             lines = f.readlines()
#         if len(lines) > 0:
#             prng = np.random.RandomState()
#             index = prng.permutation(len(lines) - 1)
#             idx = np.asarray(index, dtype=np.integer)[0]
#             random_ua = lines[int(idx)]
#     except Exception as ex:
#         print('Exception in random_ua')
#         print(str(ex))
#     finally:
#         return random_ua
#
# user_agent = get_random_ua()
#
# headers = {
#         'user-agent': user_agent
#         # 'referer' : referer
#
#     }
def main():
    with open(Path(ROOT, 'product_links.json')) as link_file:
        gt_pdts = json.load(link_file)

    if not os.path.exists(meta_folder):
        os.makedirs(meta_folder)

    # access to each category's product
    for j in range(0, len(categories)):
        logging.info('Start scraping info for category {}'.format(j))
        start_time = time.time()
        pdt_links_per_ctg = gt_pdts[j]['link']  # change it manually
        pdt_ctg = gt_pdts[j]['category']

        if pdt_links_per_ctg is None:
            logging.error('Category {} has no link'.format(j))
        else:
            for i in range(len(pdt_links_per_ctg)):
                try:
                    link = pdt_links_per_ctg[i]
                    logging.info('Link is {}'.format(link))
                    page = requests.get(link)
                    if page.status_code != 404:
                        soup = BeautifulSoup(page.content, 'html.parser')
                        pdt_meta = soup.find_all('meta')
                        pdt_info = {'category': None, 'name': None, 'image': None, 'price': None, 'url': None,
                                    'desc': None,
                                    'details': None}  # 'width': None, 'height': None
                        csv_header = pdt_info.keys()
                        for variant in pdt_meta:
                            pdt_info['category'] = pdt_ctg
                            info = variant.get('content')
                            typ = variant.get('property')
                            if typ == 'og:image' and pdt_info['image'] is None:  # only select the 1st front image
                                pdt_info['image'] = info
                            if typ == 'og:price:amount':
                                pdt_info['price'] = re.sub(r'[^\w\s]', '', info, re.UNICODE)  # encode is required
                            if typ == 'og:description':
                                pdt_info['desc'] = re.sub(r'[^\w\s]', '', info, re.UNICODE)
                            if typ == 'og:title':
                                pdt_info['name'] = re.sub(r'[^\w\s]', '', info, re.UNICODE)
                            if typ == 'og:url':
                                pdt_info['url'] = info

                        details = []
                        pdt_detail = soup.find_all('p')
                        for item in pdt_detail:
                            if ":" in item.get_text():
                                details.append(item.get_text().replace('\n', '').encode('utf-8').strip())
                                pdt_info['details'] = details

                        # download image and save info in csv
                        sub_folder = Path(meta_folder, pdt_ctg)
                        try:
                            if not os.path.exists(sub_folder):
                                os.makedirs(sub_folder)
                        except OSError:
                            logging.error('Creating directory. ' + str(sub_folder))

                        try:
                            urlretrieve(pdt_info['image'], Path(sub_folder, pdt_info['name'] + '.jpg'))
                            with open(Path(ROOT, 'Furniture.csv'), 'a') as f:  # Just use 'a' means adding
                                writer = csv.DictWriter(f, fieldnames=csv_header)
                                if f.tell() == 0:
                                    writer.writeheader()  # write a header
                                writer.writerow(pdt_info)

                        except urllib.error.HTTPError as err:
                            logging.error('Image Error: ' + err.code)

                        delay = np.random.choice(delays)
                        time.sleep(delay)
                    else:
                        logging.error('Page is not Found')

                    delay = np.random.choice(delays)
                    time.sleep(delay)

                except Exception as e:
                    logging.error(e)
                    pass

        delay = np.random.choice(delays)
        time.sleep(delay)
        end_time = time.time()
        logging.info('Finish scraping info for category {}'.format(j))
        logging.info('Elapsed time is: ' + str(round((end_time - start_time) / 60, 2)) + ' minus')


if __name__ == "__main__":
    main()
