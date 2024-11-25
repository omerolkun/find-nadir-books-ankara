import cloudscraper
import psycopg2
from info import info
from bs4 import BeautifulSoup

def main():
    ankara_url = "https://www.nadirkitap.com/sahaflar.php?favori=0&rumuz=&sehir=6"
    ankara_url2 = "https://www.nadirkitap.com/sahaflar.php?ara=1&favori=0&rumuz=&sehir=6&page={}"
    scraper = cloudscraper.create_scraper()
    page = scraper.get(ankara_url2).text
    soup = BeautifulSoup(page, "html.parser")
    pagination_block = soup.find("ul", {"class": "pagination pagination-product"})
    last_button = pagination_block.find("form")
    page_number = int(last_button.text.strip().split(" ")[1])
    urls = {}

    for i in range(page_number):
        url = ankara_url2.format(i+1)
        page = scraper.get(url).text
        soup = BeautifulSoup(page, "html.parser")
        list_block = soup.find("div", {"class": "list-cell"})
        sellers = list_block.find_all("li")
        for item in sellers:
            url = item.find("a")["href"]
            name = item.find("a").text
            if '\'' in name:
                print("yes")
                print(name)
                print("0000000000000000000000")
                name = name.replace("\'", "AA")
                print(name)
            urls[name] = url
    

    (db_name, username, password) = info()[0]
    conn = psycopg2.connect(database = db_name, user = username, host= 'localhost', password = password, port = 5432)

    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS sellersank(
                id SERIAL PRIMARY KEY,
                seller_name VARCHAR (100) NOT NULL,
                seller_link VARCHAR (100) NOT NULL)
                """)
    conn.commit()
    
    for key in urls:
        print(key, urls[key])
        sql_command = "INSERT INTO sellersank (seller_name,seller_link) VALUES ('{}','{}')".format(key, urls[key])
        cur = conn.cursor()
        cur.execute(sql_command)
        conn.commit()
        cur.close()



if __name__ == "__main__":
    main()
