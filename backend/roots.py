"""
Roots
Item Price Scraper
"""
import json
from pprint import pprint

import requests
from bs4 import BeautifulSoup


def download_page(url):
    """Download a page of items"""
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    string = soup.prettify()

    results = []

    start = 0

    while True:
        header = "gtag('event', 'view_item_list', {'items':"
        start = string.find(header, start)
        if start == -1:
            break
        start += len(header)
        end = string.find("] });", start)
        items = string[start:end].strip()[:-1]
        start = end

        for char in "\r\t\n":
            items = items.replace(char, "")
        items = json.loads(items + "]")

        for item in items:
            results.append((item["name"], item["variant"], item["price"]))

    return results


def main():
    """main method"""
    urls = (
        "https://www.roots.com/ca/en/women/categories/tops/",
        "https://www.roots.com/ca/en/women/categories/bottoms/",
        "https://www.roots.com/ca/en/women/categories/dresses/",
        "https://www.roots.com/ca/en/women/categories/sweaters-and-cardigans/",
    )
    results = []
    for url in urls:
        items = download_page(url)
        results.extend(items)

    pprint(results)


if __name__ == "__main__":
    main()
