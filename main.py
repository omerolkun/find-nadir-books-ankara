import time
import math
import sys
from bs4 import BeautifulSoup
from book import Book
import cloudscraper

def main():
    start_time = time.time()
    book_name = sys.argv[1]

    url = "https://www.nadirkitap.com/kitapara.php?satici=166344&ara=aramayap&tip=yazar&kitap_Adi={}".format(book_name)
    url2 = "https://www.nadirkitap.com/kitapara.php?ara=aramayap&ref=&kategori=0&kitap_Adi=&yazar={}&ceviren=&hazirlayan=&siralama=&satici=166344&ortakkargo=0&yayin_Evi=&yayin_Yeri=&isbn=&fiyat1=&fiyat2=&tarih1=0&tarih2=0&guzelciltli=0&birincibaski=0&imzali=0&eskiyeni=0&cilt=0&listele=&tip=yazar&dil=0&page={}"
    book_list = []

    scraper = cloudscraper.create_scraper()
    page_content = scraper.get(url2.format(book_name, 1)).text
    soup = BeautifulSoup(page_content, "html.parser")

    total_item_number = soup.find('p', {"class": "icon no-icon aramap"}).text.split()[0]
    if total_item_number == "Arama":
        print("Author {} is not found...".format(book_name))
        sys.exit()

    page_number = math.ceil((int(total_item_number) / 25))



    product_list = soup.find('ul', class_="product-list")
    li_css = "body > div.section.margin-top-20px > div > div > div.col-md-9.col-xs-12 > div.list-cell > ul > li"
    items = product_list.select(li_css)
    
    for item in items:  # iterate book elements inside list
        name = item.find('h4').text.strip()
        author = item.find('p').text
        price = item.find("div", {"class": "col-md-6 col-xs-12 no-padding text-right product-list-price"}).text.split()[0]
        book = Book(name, author, price)
        book_list.append(book)
    
    if int(total_item_number) > 1:
        i = 2
        while i < int(total_item_number) + 1:
            page_content = scraper.get(url2.format(book_name, i)).text
            soup = BeautifulSoup(page_content, "html.parser")
            product_list = soup.find('ul', class_="product-list")
            li_css = "body > div.section.margin-top-20px > div > div > div.col-md-9.col-xs-12 > div.list-cell > ul > li"
            items = product_list.select(li_css)

            for item in items:
                name = item.find('h4').text.strip()
                author = item.find('p').text
                price = item.find("div", {"class": "col-md-6 col-xs-12 no-padding text-right product-list-price"}).text.split()[0]
                book = Book(name, author, price)
                book_list.append(book)
            i = i + 1
    
    print("total book number is ", len(book_list))
    
    end_time = time.time()
    print("exec time: ", round(end_time - start_time, 2), " seconds.")



if __name__ == "__main__":
    main()
