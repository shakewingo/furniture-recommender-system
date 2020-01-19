# Furniture.ca Living Room Products Scrapper
# Environment: PyCharm, Python 3.6

import csv
import json
import os
import re
import time
import urllib
from urllib.request import urlretrieve

import numpy as np
import requests
from bs4 import BeautifulSoup
import certifi

delays = [7, 4, 6, 2, 10, 19]

# #######################################################################
# # access to each category's product
# #######################################################################
main_folder = '/Users/yingyao/Desktop'
os.chdir(main_folder)

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


with open('product_links.json') as link_file:
    gt_pdts = json.load(link_file)
#print (len(gt_pdts[j]['link']))

for j in range(0,12):
    start_time = time.time()
    pdt_links_per_ctg = gt_pdts[j]['link']   # change it manually
    pdt_ctg = gt_pdts[j]['category']

    # print(pdt_ctg)
    # print(pdt_links_per_ctg[1])

    if pdt_links_per_ctg is None:
       pass
    else:
        for i in range(len(pdt_links_per_ctg)):
                link = 'https://' + pdt_links_per_ctg[i]
                page = requests.get(link)

                if page.status_code != 404:
                    soup = BeautifulSoup(page.content, 'html.parser')
                    pdt_meta = soup.find_all('meta')
                    pdt_info = {'category': None, 'name': None, 'image': None, 'price': None, 'url': None, 'desc': None,
                                'details': None}  # 'width': None, 'height': None

                    for variant in pdt_meta:
                        pdt_info['category'] = pdt_ctg
                        info = variant.get('content')
                        type = variant.get('property')
                        # print (info, type)
                        if type == 'og:image' and pdt_info['image'] is None:  # only select the 1st front image
                            pdt_info['image'] = info
                        if type == 'og:price:amount':
                            pdt_info['price'] = re.sub(r'[^\w\s]', '', info, re.UNICODE)  # encode is required
                        if type == 'og:description':
                            pdt_info['desc'] = re.sub(r'[^\w\s]', '', info, re.UNICODE)
                        if type == 'og:title':
                            pdt_info['name'] = re.sub(r'[^\w\s]', '', info, re.UNICODE)
                        if type == 'og:url':
                            pdt_info['url'] = info

                    details = []
                    pdt_detail = soup.find_all('p')
                    for item in pdt_detail:
                        if ":" in item.get_text():
                            details.append(item.get_text().replace('\n', '').encode('utf-8').strip())
                            pdt_info['details'] = details

                    #print(pdt_info)

                    # download image and save info in csv
                    sub_folder = main_folder + '/Meta/' + pdt_ctg

                    try:
                        if not os.path.exists(sub_folder):
                            os.makedirs(sub_folder)
                    except OSError:
                        print('Error: Creating directory. ' + sub_folder)

                    os.chdir(sub_folder)

                    # make sure python has CA certificate: /Applications/Python\ 3.6/Install\ Certificates.command
                    try:
                        urlretrieve(pdt_info['image'], pdt_info['name'] + '.jpg')
                        try:
                            if not os.path.exists(main_folder + '/Meta'):
                                os.makedirs(main_folder + '/Meta')
                        except OSError:
                            print('Error: Creating directory. ' + main_folder + '/Meta')

                        os.chdir(main_folder + '/Meta')

                        with open('Furniture.csv', 'a') as f:  # Just use 'a' means adding
                            a = csv.DictWriter(f, pdt_info.keys())
                            a.writerow(pdt_info)

                    except urllib.error.HTTPError as err:
                        print('Image Error: ' + err.code)

                    delay = np.random.choice(delays)
                    time.sleep(delay)

                else:
                    print('Page is not Found')

                delay = np.random.choice(delays)
                time.sleep(delay)

                end_time = time.time()
                print('Running time is: ' + str(round((end_time - start_time) / 60, 2)) + ' minus')


        delay = np.random.choice(delays)
        time.sleep(delay)

