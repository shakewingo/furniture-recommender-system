# Furniture.ca Living Room Products Scrapper
# Environment: PyCharm, Python 3.6


# To use phantomjs via selenium, you need:
# 1) Install NodeJS
# 2) Using Node's package manager install phantomjs: sudo npm -g install phantomjs-prebuilt (admin access)
# 3) install selenium (in your virtualenv, if you are using that)

# # issue : exist elements that have chance to be non visible each time, reason (visibility setting / waiting certain element to load page) is not sure
# # solution: run a page couple more times until whole products on that page is detected


import os
import json
import re
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from bs4 import BeautifulSoup
from time import sleep
from random import randint


main_folder = '/Users/yingyao/Desktop'
pageno = 0

# create json file
os.chdir(main_folder)
product_links = []
for i,j in enumerate (['living-room-packages', 'sofas', 'loveseats', 'sectionals', 'chairs & chaises', 'recliners', 'ottmans & benches', 'cabinets & shelvings',
                       'TV stands & mounts', 'coffee tables', 'sofa & console tables', 'end & accent tables']):
    product_link = {'category': j, 'link': None}
    product_links.append(dict(product_link))

with open('product_links.json','w') as outfile:
         json.dump(product_links, outfile)

# # #######################################################################
# # # obtain product link of each page
# # #######################################################################
for instance in range(100):
    i = 0  # change category manually: exp: living room packages-->0
    cat = 'living-room-packages' # change category manually
    domain = 'www.furniture.ca'
    link = 'https://www.furniture.ca/collections/furniture-living-room-'+cat+'?limit=36&offset='+str(pageno)+'&slot=collections%2Ffurniture-living-room-'+cat
    #print (link)
    driver = webdriver.PhantomJS(executable_path='/usr/local/lib/node_modules/phantomjs-prebuilt/lib/phantom/bin/phantomjs')
    rdm = randint(10,36)
    wait = WebDriverWait(driver,rdm)
    driver.get(link)
    # f = lambda d: re.search(
    #           re.compile(r'\d+'),
    #           d.find_element_by_xpath('//button[@class=\'findify-widget--pagination__button findify-widget--pagination__last\']').text
    #           )
    # wait.until(f)
    page = BeautifulSoup(driver.page_source,'html.parser')
    #print(page)

# findify-widget--product _1anW_: href
    domain = 'www.furniture.ca'
    product_links = {'category': cat, 'link': None}
#
# read json file
    os.chdir(main_folder)
    with open('product_links.json') as link_file:
         product_links_pre = json.load(link_file)

    if product_links_pre[i]['link'] is None:
        product_links['link'] = []
    else:
        product_links['link']= product_links_pre[i]['link']

    r = re.compile(r'/products/+')
#
    for a in page.findAll('a', href=r):
        link = domain + a['href']
        if link not in product_links['link']:
            product_links['link'].append(link)
        else: pass

    print (product_links)
    print (len(product_links['link']))

    product_links_pre[i]['link'] = product_links['link']
#
# overwrite json file
    os.chdir(main_folder)
    with open('product_links.json','w') as outfile:
         json.dump(product_links_pre, outfile)

    if (len(product_links['link'])%36 == 0) and (link is not None) and len(product_links['link'])!= 0:
        pageno = pageno + 36   # volume of products on that page
    print ('We have collected: '+ str(pageno) + ' products')
    sleep(5)
