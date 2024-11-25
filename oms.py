import time
import math
import re
import logging
import cloudscraper
import sys
import re
from random import shuffle
import psycopg2
from info import info
from mails import mailahmet
from bs4 import BeautifulSoup
from book import Book
from datetime import datetime


def main():
    start_time = datetime.now().replace(microsecond=0)
    logging.basicConfig(filename='/home/dashone00/test-board/others/find-nadir-books-ankara/log.log', level=logging.INFO)
    logging.info("started at {}".format(str(start_time)))

    if len(sys.argv) < 3:
        print("Missing parameters. Format: python3 find.py book_name author_name")
        print("If author_name doesn't matter, type * instead of a name")
        print("End of program")
        sys.exit()

    author = sys.argv[2]
    title = sys.argv[1]
    temp = ""
    if " " in title:
        words = title.split()
        for i in range(len(words)):
            temp = temp + words[i] + "+"
        title = temp[:-1]


    generic_url = "https://www.nadirkitap.com/kitapara.php?satici={}&ara=aramayap&tip=kitap&kitap_Adi={}"
    (db_name, username, password) = info()[0]
    seller_list = []
    conn = psycopg2.connect(database=db_name, user=username, password=password, host='localhost', port='5432')
    conn.autocommit = True
    cursor = conn.cursor()
    SQL_COMMAND = "select seller_link from sellersank"
    cursor.execute(SQL_COMMAND)
    result = cursor.fetchall()
    logging.info("Urls are fetched from db at {}".format(str(datetime.now().replace(microsecond=0))))
    shuffle(result)
    for row in result:
        seller_list.append(row[0])
    result_urls = []
    just_last_part = []   # string which is following from the last dash in the url
    for item in seller_list: 
        parts = item.split("-")
        last_part = parts[len(parts)-1]
        just_last_part.append(last_part)


    for url in just_last_part:
        numbers = [int(s) for s in re.findall(r'\d+', url)]
        seller_code = numbers[0]
        result_urls.append(generic_url.format(seller_code, title))

        
    lst = get_books(result_urls)
    logging.info("{} books are found.".format(str(len(lst))))
    send_mail(lst, author)
    end_time = datetime.now().replace(microsecond=0)
    logging.info("End of program at {}\n".format(str(end_time)))




def get_books(result_urls):
    book_list = []
    for url in result_urls:
        scraper = cloudscraper.create_scraper()
        page_content = scraper.get(url).text
        soup = BeautifulSoup(page_content, "html.parser")
        page_number_block_css_selector = "p.icon"
        try: 
            page_number_block = ((soup.select(page_number_block_css_selector)[0]).text).strip()
        except Exception as e:
            logging.info(str(info) + " , " + url)
            continue
        book_count = page_number_block.split()[0]

        if book_count != "Arama":
            book_count = int(book_count)
        else:
            book_count = 0
            continue
        

        page_number = math.ceil((book_count/25))
        product_list_block = soup.find("ul", {"class": "product-list"})
        products = product_list_block.find_all("li", recursive=False)
        for product in products:
            information_block = product.find("h4")
            title = information_block.text.strip()
            author = (product.find("p").text).lower()
            products_block = product.find_all("div", recursive=False)
            sec_blocks = products_block[1].find("div")
            price_block = sec_blocks.find_all("div", recursive=False)[1]
            price = price_block.find_all("div")[2].text
            price_int = price_text_to_int(price)
            seller = (product.find("a", {"class": "seller-link"})).text
            book_list.append((title, author, price_int, seller))
        if page_number == 1:
            continue
        else:
            codes = extract_codes(url)
            url3 = "https://www.nadirkitap.com/kitapara.php?ara=aramayap&ref=&kategori=0&kitap_Adi={}&yazar=&ceviren=&hazirlayan=&siralama=&satici={}&ortakkargo=0&yayin_Evi=&yayin_Yeri=&isbn=&fiyat1=&fiyat2=&tarih1=0&tarih2=0&guzelciltli=0&birincibaski=0&imzali=0&eskiyeni=0&cilt=0&listele=&tip=kitap&dil=0&page={}"
            for i in range(page_number - 1):
                url = url3.format(codes[1], codes[0], str(i+2))
                page_content = scraper.get(url).text
                soup = BeautifulSoup(page_content, "html.parser")
                product_list_block = soup.find("ul", {"class": "product-list"})
                products = product_list_block.find_all("li", recursive=False)
                for product in products:
                    information_block = product.find("h4")
                    title = information_block.text.strip()
                    author = product.find("p").text
                    products_block = product.find_all("div", recursive=False)
                    sec_blocks = products_block[1].find("div")
                    price_block = sec_blocks.find_all("div", recursive=False)[1]
                    price_text = price_block.find_all("div")[2].text
                    price = price_text_to_int(price_text)
                    information_block = product.find("h4")
                    title = information_block.text.strip()
                    author = product.find("p").text
                    book_list.append((title, author, price, seller))
    sorted_book_list = sorted(book_list, key=lambda tup: tup[2])        
    return sorted_book_list


def extract_codes(url):
    code = ""
    for i in range(len(url)):
        if url[i].isnumeric():
            code = code + url[i]
        if url[i] == "&":
            break

    c = url.split("=")
    title = c[4]

    return (code, title)

def price_text_to_int(price_text):
    price_split = price_text.split()
    price_no_camma = price_split[0].replace(",", ".")
    price_result = 0
    try:
        price_float = float(price_no_camma)
        price_result = int(price_float)
    except:
        price_result = -1
    return price_result



def send_mail(result_list, author):
    print(len(result_list), ", ", author)
    mail_message = "Subject: {} \n\n".format(sys.argv[1])
    for obj in result_list:
        if author == "*":
            mail_message = mail_message + " " + obj[3] + "-" + obj[1] + "-" + str(obj[2]) + " TL " + "-" + obj[0] + '\n\n'
        if author == obj[1]:
            mail_message = mail_message + " " + obj[3] + "-" + obj[1] + "-" + str(obj[2]) + " TL " +"-" + obj[0] + '\n\n'
        else:
            print("here is interesting for ", str(obj))
            continue
    time.sleep(14)
    msg = mail_message.encode('utf-8')
    mailahmet(msg)

if __name__ == "__main__":
    main()
