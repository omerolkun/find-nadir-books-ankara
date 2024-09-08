import time
import math
import sys
from bs4 import BeautifulSoup
import cloudscraper

def main():
    start_time = time.time()
    book_name = sys.argv[1]

    url = "https://www.nadirkitap.com/kitapara.php?satici=166344&ara=aramayap&tip=yazar&kitap_Adi={}".format(book_name)
    bottom_selector = "body > div.section.margin-top-20px > div > div > div.col-md-9.col-xs-12 > div.col-md-12.col-xs-12.pagination-product-bottom"

    scraper = cloudscraper.create_scraper()
    page_content = scraper.get(url).text
    soup = BeautifulSoup(page_content, "html.parser")
    product_list = soup.find('ul', class_="product-list")
    li_css = "body > div.section.margin-top-20px > div > div > div.col-md-9.col-xs-12 > div.list-cell > ul > li"
    total_item_number = int(soup.find('p', {"class": "icon no-icon aramap"}).text.split()[0])
    page_number = math.ceil((total_item_number / 25))
    print(page_number, " pages", "type of page_number: ", type(page_number))
    items = product_list.select(li_css)
    
    for book in items:
        name = book.find('h4')
        print(name.text.strip())
        author = book.find('p')
        print(author.text, "\n--")

    
    end_time = time.time()
    print("exec time: ", round(end_time - start_time, 2), " seconds.")



if __name__ == "__main__":
    main()
