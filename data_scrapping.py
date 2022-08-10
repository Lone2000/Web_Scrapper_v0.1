from unittest import skip
from bs4 import BeautifulSoup
import re, requests
from numpy import sort
from django.http import request

search_item = input("What product do you want to search for? ")

url = f"https://www.newegg.ca/p/pl?d={search_item}&N=4131"
page = requests.get(url).text
doc = BeautifulSoup(page, "html.parser")

pages_text = doc.find(class_="list-tool-pagination-text").strong

pages = int(str(pages_text).split("/")[-2].split(">")[-1][:-1])

items_found = {}

for page in range(1, pages + 1):
    url = f"https://www.newegg.ca/p/pl?d={search_item}&N=4131&page={page}"
    page = requests.get(url).text
    doc = BeautifulSoup(page, "html.parser")

    div = doc.find(class_="item-cells-wrap border-cells items-grid-view four-cells expulsion-one-cell")
    items = div.find_all(text=re.compile(search_item))

    for item in items:
        parent = item.parent
        link = None
        if parent.name != "a":
            continue
               
        link = parent['href']
        #print(link)

        item_data = (parent.parent).parent

        price = item_data.find(class_="price-current").strong
        #Fixing the "None" Type Error When Login To See Price
        if price == None:
            continue
        
        items_found[item]= {"price":price.string.replace(",",""), "link": link  } 

sorted_items = sorted(items_found.items() ,  key = lambda x:x[1]["price"])

for item in sorted_items:
    print(item[0])
    print(f"${item[1]['price']}")
    print(item[1]["link"])
    print('''<----------------------->''')




