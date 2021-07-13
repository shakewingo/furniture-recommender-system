# Living Room Furniture Recommender System
An end-to-end development of living room furniture recommender system based on multivariant LDA. The project contains three parts, web scraping from 
[furniture.ca](https://www.furniture.ca)

## Environment Setup
The project is written in macOS arm64, for virtual env setup and tensorflow installed on Mac M1: refer
[tensorflow_macos](https://github.com/apple/tensorflow_macos/issues/153), then
downgrade pillow `conda install pillow=8.2.0`, downgrade h5py `pip install h5py==2.10.0`

`conda env update --file environment.yml`

`conda env update --file environment_engine.yml`

## Web Scraping
1. Run `python Algorithm/pdt_link_scraper.py` to get all product links for living room furnitures. Expect to have file 
   product_links.json generated in root path. 
2. Run `python Algorithm/pdt_info_scraper.py` to obtain all product attributes such as name, image, price, description. 
   Expect to have Furniture.csv generated in root path.
* After step 1, you can run `python Algorithm/test.py` to count categories.

Note that, the above steps could really take 1-2 whole days to finish. The original meta data run on Jun 2020 has XXX 
product images and XXX product records in csv. You can obtain it by running it by yourself or contact me 
[yaoyingshakewin@gmail.com](mailto:yaoyingshakewin@gmail.com) for a cleaned up version in order to replicate the rest study.

## Multivariant LDA Recommender Algorithm
