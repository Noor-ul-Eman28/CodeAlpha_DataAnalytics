"""
==========================================================================
 TASK 1: WEB SCRAPING
 CodeAlpha Data Analytics Internship
==========================================================================
Target site : https://books.toscrape.com/
              (a public "scraping sandbox" site built specifically for
              practicing web scraping — safe and legal to scrape)

What this script does
----------------------
1. Requests every category/listing page of books.toscrape.com (paginated).
2. Parses each product card with BeautifulSoup.
3. Extracts: title, price, star rating, stock availability, category,
   product URL, and UPC (from the product detail page).
4. Cleans the extracted fields (currency symbols, rating words -> numbers,
   whitespace) and stores everything in a pandas DataFrame.
5. Saves the final dataset to data/scraped_books.csv, which is then used
   by task2_eda.py and task3_data_visualization.py.

Libraries used: requests, BeautifulSoup (bs4), pandas, time, re

HOW TO RUN
----------
This script needs a normal internet connection (not available inside the
Claude sandbox that generated this project). Run it locally with:

    py -3.11 -m pip install requests beautifulsoup4 pandas
    py -3.11 task1_web_scraping.py

It will overwrite data/scraped_books.csv with freshly-scraped, live data.
==========================================================================
"""

import re
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/"
CATALOGUE_URL = BASE_URL + "catalogue/"
HEADERS = {"User-Agent": "Mozilla/5.0 (Educational Scraping Project - CodeAlpha Internship)"}

RATING_WORDS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


def get_soup(url: str) -> BeautifulSoup:
    """Fetch a URL and return a parsed BeautifulSoup object."""
    resp = requests.get(url, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, "lxml")


def extract_category(book_url: str) -> str:
    """
    Visit a single product page to pull the exact category name
    (breadcrumb) and UPC — this data is not present on the listing page.
    """
    soup = get_soup(book_url)
    breadcrumb = soup.select("ul.breadcrumb li a")
    category = breadcrumb[-1].get_text(strip=True) if len(breadcrumb) >= 2 else "Unknown"

    upc = None
    table = soup.find("table", class_="table table-striped")
    if table:
        for row in table.find_all("tr"):
            header = row.find("th")
            if header and header.get_text(strip=True) == "UPC":
                upc = row.find("td").get_text(strip=True)
                break
    return category, upc


def scrape_all_books(max_pages: int = None) -> pd.DataFrame:
    """
    Walk every paginated listing page of books.toscrape.com and collect
    every product card into a list of dicts.

    max_pages: optional cap for a quick test run (None = scrape all ~50 pages)
    """
    records = []
    page_num = 1
    next_page = "page-1.html"

    while next_page:
        url = CATALOGUE_URL + next_page
        print(f"Scraping listing page {page_num}: {url}")
        soup = get_soup(url)

        for card in soup.select("article.product_pod"):
            title = card.h3.a["title"].strip()
            relative_href = card.h3.a["href"].replace("../../../", "")
            product_url = CATALOGUE_URL + relative_href

            price_raw = card.select_one("p.price_color").get_text(strip=True)
            price = float(re.sub(r"[^\d.]", "", price_raw))

            availability = card.select_one("p.instock.availability").get_text(strip=True)
            in_stock = availability.lower().startswith("in stock")

            rating_class = card.select_one("p.star-rating")["class"]
            rating_word = [c for c in rating_class if c != "star-rating"][0]
            rating = RATING_WORDS.get(rating_word, None)

            category, upc = extract_category(product_url)
            time.sleep(0.05)  # be polite to the server

            records.append({
                "title": title,
                "price_gbp": price,
                "rating_out_of_5": rating,
                "in_stock": in_stock,
                "category": category,
                "upc": upc,
                "product_url": product_url,
            })

        # find the "next" pagination link, if any
        next_link = soup.select_one("li.next a")
        next_page = next_link["href"] if next_link else None
        page_num += 1

        if max_pages and page_num > max_pages:
            break

    return pd.DataFrame(records)


if __name__ == "__main__":
    print("Starting scrape of books.toscrape.com ...")
    df = scrape_all_books()  # remove the cap; pass max_pages=3 for a quick test
    df.drop_duplicates(subset="upc", inplace=True)
    df.to_csv("data/scraped_books.csv", index=False)
    print(f"\nDone. Scraped {len(df)} books across {df['category'].nunique()} categories.")
    print("Saved to data/scraped_books.csv")
