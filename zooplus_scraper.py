import sqlite3
import requests
import pandas as pd 
from bs4 import BeautifulSoup

if __name__=="__main__":

    # Get the HTML content of the website
    response = requests.get("https://www.zooplus.co.uk/shop/cats/dry_cat_food")
    soup = BeautifulSoup(response.content, "html.parser")

    # Get product wrappers. Each wrapper may have varying content.
    product_wrappers = soup.select('div[class*="ProductListItem_productWrapper"]')
    
    # Placeholder of the data
    product_titles = []
    ratings = []
    descriptions = []
    product_variants = []
    product_prices = []

    # Iterate through the wrappers
    for wrapper in product_wrappers:

        # Get the product title, rating, and description
        product_title = wrapper.select_one('a[class*="ProductListItem_productInfoTitleLink"]')
        rating = wrapper.find("span", "pp-visually-hidden")
        description = wrapper.select_one('p[class*="ProductListItem_productInfoDescription"]')
        
        # Get the variants of each product and their prices
        variants = [v.text for v in wrapper.select('span[class*="ProductListItemVariant_variantDescription"]')]
        prices = [p.text for p in wrapper.select('span[class*="z-price__amount"]')]

        # Append the results to the placeholder lists 
        product_titles.append(product_title.text)
        ratings.append(rating.text)
        descriptions.append(description.text)
        product_variants.append(variants)
        product_prices.append(prices)

    # Consolidate the data into dataframe
    data = {
        "product_titles": product_titles, 
        "ratings": ratings, 
        "descriptions": descriptions, 
        "variants": product_variants, 
        "prices": product_prices
    }
    df = pd.DataFrame(data).explode(["variants", "prices"])

    # Save the data in CSV format
    df.to_csv("zooplus.csv")

    # Save the data in SQLite database
    with sqlite3.connect("zooplus.db") as con:
        df.to_sql("products", con, if_exists="replace", index=False)