# Living Room Furniture Recommender System
This is an end-to-end development of living room furniture recommender system. The repo contains 
three parts: web scraping from [furniture.ca](https://www.furniture.ca), recommender system algorithm and a local web application via flask.

## Environment Setup
The project is written in macOS arm64, for virtual env setup and tensorflow installed on Mac M1: please carefully refer
[tensorflow_macos](https://github.com/apple/tensorflow_macos/issues/153), then after the below env is activated, you'll
have to downgrade pillow `conda install pillow=8.2.0`, downgrade h5py `pip install h5py==2.10.0`

`conda env update --file environment.yml`

`conda env update --file environment_engine.yml`

## Part I: Web Scraping
1. 
```
export ROOT=your furniture-recommender-system root path 
conda activate furniture-recommender
```
2. `python Algorithm/pdt_link_scraper.py` to get all product links for living room furnitures. Expect to have file 
   product_links.json generated in root path. 
3. `python Algorithm/pdt_info_scraper.py` to obtain all product attributes such as name, image, price, description. 
   Expect to have Meta_org folder and Furniture.csv generated in root path.
* After step 2, you can run `python Algorithm/test.py` to count categories.

Note that, the above steps could really take 1-2 whole days to finish. The original meta data run on Jun 2020 has 2953 
product images and 2904 product records in csv. You can obtain it by running on your own or contact me 
[yaoyingshakewin@gmail.com](mailto:yaoyingshakewin@gmail.com) for a cleaned up version in order to replicate the rest study.

## Part II: Multivariant LDA Recommender Algorithm
0. Prerequisite: finish **part I** or have Meta_org folder and furniture.csv ready
1. `conda activate furniture-recommender`
2. `jupyter lab`
3. Open Algorithm/furniture_recommender_algorithm.ipynb and run

Note that, the recommendation method is based on extracting both text attributes and image features from pre-trained 
ResNet50 model and then use them to create the bag of words and fit in LDA topic modelling. References:

* [A Multimodal Recommender System for Large-scale Assortment Generation in E-commerce](https://arxiv.org/abs/1806.11226)
* [Discovering Style Trends through Deep Visually Aware Latent Item Embeddings](https://arxiv.org/abs/1804.08704)

## Part III: Web Application
0. Prerequisite: can run directly from this repo or finish **part II**
1. 
```
export FLASK_APP=run.py
export FLASK_ENV=development
conda activate furniture-recommender-engine
cd Engine
```
2. 
```
flask dropDB
flask createDB
flask importDB
flask run
```

You should be able to find link such as http://127.0.0.1:5000/ to open. And Bang! It's done!

Note that, the web template is forked from https://github.com/MathMagicx/MediumFlaskImageRecommender

## Recommender System Demo


https://user-images.githubusercontent.com/42901821/125501142-1cfcd2b3-be69-4e9f-a97e-3fad8cbc35bd.mp4


