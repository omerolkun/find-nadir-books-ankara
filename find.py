import time
import re
import cloudscraper
import sys
import re
from random import shuffle
import psycopg2
from info import info
from mails import mailahmet
from bs4 import BeautifulSoup
from book import Book

start_time = time.time()
(db_name, username, password) = info()[0]
seller_list = []
conn = psycopg2.connect(database=db_name, user=username, password=password, host='localhost', port='5432')
conn.autocommit = True
cursor = conn.cursor()
SQL_COMMAND = "select seller_link from sellers"
cursor.execute(SQL_COMMAND)
result = cursor.fetchall()
shuffle(result)
TITLE = ""
for row in result:
    seller_list.append(row[0])
result_urls = []
book_name = sys.argv[1]
for url in seller_list:
    numbers = [int(s) for s in re.findall(r'\d+', url)]
    seller_code = numbers[0]
    result_url = url
    result_url = "https://www.nadirkitap.com/kitapara.php?satici={}&ara=aramayap&tip=kitap&kitap_Adi={}".format(seller_code, book_name)
    result_url = "https://www.nadirkitap.com/kitapara.php?ara=aramayap&ref=&kategori=0&kitap_Adi={}&yazar=&ceviren=&hazirlayan=&siralama=&satici={}&ortakkargo=0&yayin_Evi=&yayin_Yeri=&isbn=&fiyat1=&fiyat2=&tarih1=0&tarih2=0&guzelciltli=0&birincibaski=0&imzali=0&eskiyeni=0&cilt=0&listele=&tip=kitap&dil=0&page=".format(seller_code, book_name)
    result_urls.append(result_url)

result_list = []
for seller in result_urls:
    scraper = cloudscraper.create_scraper()
    page_content = (scraper.get(seller).text)
    soup = BeautifulSoup(page_content, "html.parser")
    rows = soup.find_all("div", {"class": "product-list-right-top"})

    if len(rows) > 0:
        seller_name = soup.find("a", {"class": "seller-link"}).string
        for single_row in rows:
            name = single_row.find('a')['title']
            price = single_row.find(class_="col-md-6 col-xs-12 no-padding text-right product-list-price").string
            try:
                price_spl = re.split(r"[,.]", price)
                int_price = int(price_spl[0])
            except:
                int_price = -1
            tup = (seller_name, name, int_price)
            result_list.append(tup)

for x in result_list:
    print(x)
end_time = time.time()
print("Total Executione time: ", round((end_time - start_time) / 60, 2), "minutes...")

file_name = sys.argv[1]
mail_message = "Subject: {} \n\n".format(sys.argv[1])

file = open('/home/om/Documents/ankaradakisahafkitap/{}.txt'.format(file_name), 'w')
result_message = "Toplam " + str(len(result_list)) + " kitap bulunmustur.\n\n"
file.write(result_message)
result_list.sort(key=lambda a: a[2])

for obj in result_list:
    mail_message = mail_message + " " + obj[0] + "-" + obj[1] + "-" + str(obj[2]) + '\n\n'
    file.write(obj[0] + "-" + obj[1] + "-" + str(obj[2]) + '\n\n')
time.sleep(14)
msg = mail_message.encode('utf-8')
mailahmet(msg)
