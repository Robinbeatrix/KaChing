"""
American Eagle
Item Price Scraper
"""
import json

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
            # pprint(item)
            results.append((item["name"], item["variant"], item["price"]))

    return results


def main():
    """main method"""

    headers = {
        "User-Agent": "Mozilla/5.0 (platform; rv:geckoversion) Gecko/geckotrail Firefox/firefoxversion"
    }

    url = "https://www.ae.com/ca/en/c/ae/women/tops/cat10049"
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    string = soup.prettify()

    with open("test.txt", "w+") as f:
        f.write(string)


if __name__ == "__main__":
    main()
