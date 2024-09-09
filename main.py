import time
import math
import re
from random import shuffle
import sys
import psycopg2
import cloudscraper
from bs4 import BeautifulSoup
from book import Book
from info import info
from mails import mailahmet


def main():
    start_time = time.time()
    author_name = sys.argv[1]
    result_author_name = ""
    if ' ' in author_name:
        names = author_name.split() 

        for x in names:
            result_author_name = result_author_name + x + "+"

        author_name = result_author_name[:-1]
    

    book_list = []
    seller_list = []
    
    (db_name, username, password) = info()[0]
    conn = psycopg2.connect(database=db_name, user=username, password=password, host='localhost', port='5432')
    conn.autocommit = True
    cursor = conn.cursor()
    SQL_COMMAND = "select seller_link, seller_name  from sellers"
    cursor.execute(SQL_COMMAND)
    result = cursor.fetchall()
    shuffle(result)
    for row in result:
        tup = (row[0], row[1])
        seller_list.append(tup)
    result_urls = []
    
    
    for item in seller_list:
        url = item[0]
        numbers = [int(s) for s in re.findall(r'\d+', url)]
        seller_code = numbers[0]

        result_url = url
        result_url = "https://www.nadirkitap.com/kitapara.php?ara=aramayap&ref=&kategori=0&kitap_Adi=&yazar={}&ceviren=&hazirlayan=&siralama=&satici={}&ortakkargo=0&yayin_Evi=&yayin_Yeri=&isbn=&fiyat1=&fiyat2=&tarih1=0&tarih2=0&guzelciltli=0&birincibaski=0&imzali=0&eskiyeni=0&cilt=0&listele=&tip=yazar&dil=0&page=".format(author_name, (seller_code))
        result_urls.append(result_url)
    for url in result_urls: 

        scraper = cloudscraper.create_scraper()
        page_content = scraper.get((url + "1")).text
        soup = BeautifulSoup(page_content, "html.parser")

        total_item_number = soup.find('p', {"class": "icon no-icon aramap"}).text.split()[0]
        if total_item_number == "Arama":
            #print("Author {} is not found...".format(book_name))
            continue

        page_number = math.ceil((int(total_item_number) / 25))



        product_list = soup.find('ul', class_="product-list")
        li_css = "body > div.section.margin-top-20px > div > div > div.col-md-9.col-xs-12 > div.list-cell > ul > li"
        items = product_list.select(li_css)
        
        for item in items:  # iterate book elements inside list
            name = item.find('h4').text.strip()
            author = item.find('p').text
            price = item.find("div", {"class": "col-md-6 col-xs-12 no-padding text-right product-list-price"}).text.split()[0]
            seller = (soup.find("h1", {"class": "aramatitle"}).text)[len(author_name) + 1:].replace("kitapları", "").strip()
            book = Book(name, author, price, seller)
            book_list.append(book)
    
        if page_number > 1:
            i = 2
            while i < page_number + 1:
                page_content = scraper.get(url + str(i)).text
                soup = BeautifulSoup(page_content, "html.parser")
                product_list = soup.find('ul', class_="product-list")
                li_css = "body > div.section.margin-top-20px > div > div > div.col-md-9.col-xs-12 > div.list-cell > ul > li"
                items = product_list.select(li_css)

                for item in items:
                    name = item.find('h4').text.strip()
                    author = item.find('p').text
                    price = item.find("div", {"class": "col-md-6 col-xs-12 no-padding text-right product-list-price"}).text.split()[0]
                    seller = (soup.find("h1", {"class": "aramatitle"}).text)[len(author_name) + 1:].replace("kitapları", "").strip()
                    book = Book(name, author, price, seller)
                    book_list.append(book)
                i = i + 1
    
    
    end_time = time.time()
    print("exec time: ", round((end_time - start_time) / 60, 2), " minutes.")

    mail_message = "Subject: {} \n\n".format(author_name)

    file_name = author_name.replace("+", "_")
    file = open('/home/om/Documents/author_in_sellers/{}.txt'.format(file_name), 'w')
    result_message = "Toplam " + str(len(book_list)) + " kitap bulunmustur.\n"
    i = 1 
    for book in book_list:
        mail_message = mail_message + str(i) + "." + book.get_seller() + ", " + book.get_name() + ", " + book.get_price() + "\n\n"
        file.write(str(i) + "." + book.get_seller() + ", " + book.get_name() + ", " + book.get_price() + "\n")
        i = i + 1
    msg = mail_message.encode('utf-8')
    mailahmet(msg)
    print("Program is over...")



if __name__ == "__main__":
    main()
