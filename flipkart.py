# Web Scrapping of Flipkart website

import pandas as pd
from bs4 import BeautifulSoup
import requests
import re
# Creating empty sets for data
prod_name = []
prod_desc = []
prod_rev = []
prod_rate = []
prod_price = []
prod_star = []
prod_brand = []

# Loading the Flipkart official website
# Extracting data of first 10 pages
for i in range(1,10):
#    print('page:',i)
    url = 'https://www.flipkart.com/search?q=mobiles&sid=tyy%2C4io&as=on&as-' \
      'show=on&otracker=AS_QueryStore_OrganicAutoSuggest_1_7_na_na_' \
      'na&otracker1=AS_QueryStore_OrganicAutoSuggest_1_7_na_na_na&as-pos=1&as-t' \
      'ype=RECENT&suggestionId=mobiles%7CMobiles&requestId=a505a258-8b3d-4672-9e78-b35219d81523&as-' \
      'searchtext=mobiles&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.' \
      'price_range.to%3D30000&page=' + str(i)

    # extracting the contents of the page
    r = requests.get(url)
    #print(r)
    # Extracting content in text form
    soup = BeautifulSoup(r.text, 'lxml')
    box = soup.find('div',class_='_1YokD2 _3Mn1Gg')

    # Extracting the all the product names
    name = soup.find_all('div',class_ = '_4rR01T')

    #print(name)
    # Extracting product names individually
    for i in name:
        name = i.text
        prod_name.append(name)

    #print(prod_name)
    #print(len(prod_name))

    # Extracting price of the product
    price = box.find_all('div',class_ ='_30jeq3 _1_WHN1')
    #print(price)

    for i in price:
        name = i.text
        # Removing rupee symbol by extracting only numerical values
        name= re.sub(r'\D','',name)
        prod_price.append(name)
    #print(prod_price)
    #print(len(prod_price))

    # Extracting description
    desc = box.find_all('ul',class_ = '_1xgFaf')
    #print(desc)

    for i in desc:
        name = i.text
        prod_desc.append(name)
    #print(prod_desc)
    #print(len(prod_desc))

    star = box.find_all('div',class_ = '_3LWZlK')
    #print(star)

    for i in star:
        name = i.text
        prod_star.append(name)

    #print(prod_star)
    #print(len(prod_star))

    # Extracting no. of reviews
    rev_rate = box.find_all('span',class_ = '_2_R_DZ')
    for i in rev_rate:
        name = i.text
        #Split the item string into rating and review components
        components = name.split('\xa0&\xa0')
        #Extract the ratings and reviews from the components
        rating = components[0].replace(",", "").replace(' Ratings','')
        #print(rating)
        review = components[1].replace(",", "").replace(' Reviews','')
        # Append the ratings and reviews to the respective lists
        prod_rate.append(rating)
        prod_rev.append(review)

# Brand Name
for item in prod_name:
    name = item.split(' ')
    brand = name[0]
    prod_brand.append(brand)

df = pd.DataFrame({'Product Name': prod_name,'Brand': prod_brand
                      ,'Price':prod_price,'Description': prod_desc,
                   'Star Rating of 5': prod_star,
                   'No. of Reviews':prod_rev
                   ,'No. of rating': prod_rate})

df.to_csv('E:/notes/Msc DS/PROJECTS/python/webscrapping/flipkart_data.csv')