from selenium.webdriver.common.by import By
import time
from selenium import webdriver
from info import info
import undetected_chromedriver as uc
import psycopg2

def get_urls():
    url = "https://www.nadirkitap.com/sahaflar.php?favori=0&rumuz=&sehir=6"
    driver = uc.Chrome()
    driver.get(url)
    driver.minimize_window()
    list_link_seller = []
    list_seller_name = []
    xpath = "/html/body/div[2]/div/div/div[2]/div[4]/nav/ul/li[8]/a"
    lst = driver.find_element(By.CLASS_NAME, "list-cell")
    lst_elements = lst.find_elements(By.CLASS_NAME, "a14brd")
    for item in lst_elements:
        list_link_seller.append(item.get_attribute("href"))
        list_seller_name.append(item.text)

    time.sleep(3)
    nex = driver.find_element(By.XPATH, xpath)
    nex.click()
    time.sleep(3)
    lst = driver.find_element(By.CLASS_NAME, "list-cell")
    lst_elements = lst.find_elements(By.CLASS_NAME, "a14brd")
    for item in lst_elements:
        list_link_seller.append(item.get_attribute("href"))
        list_seller_name.append(item.text)

    time.sleep(4)

    for i in range(7):
        xpath2 = "/html/body/div[2]/div/div/div[2]/div[4]/nav/ul/li[10]/a"
        next = driver.find_element(By.XPATH, xpath2)
        time.sleep(2)
        lst = driver.find_element(By.CLASS_NAME, "list-cell")
        lst_elements = lst.find_elements(By.CLASS_NAME, "a14brd")
        for item in lst_elements:
            list_link_seller.append(item.get_attribute("href"))
            list_seller_name.append(item.text)
        time.sleep(1)
        next.click()
        time.sleep(3)


        
    time.sleep(3)

    nex = driver.find_element(By.XPATH, xpath2)
    nex.click()
    time.sleep(4)
    driver.close()
    return list_seller_name, list_link_seller

start_time = time.time()
seller_name, seller_list = get_urls()
(db_name, username, password) = info()[0]
conn = psycopg2.connect(database = db_name, user = username, host= 'localhost', password = password, port = 5432)

cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS sellers(
            id SERIAL PRIMARY KEY,
            seller_name VARCHAR (100) NOT NULL,
            seller_link VARCHAR (100) NOT NULL)
            """)
print("no prob")
conn.commit()
exit(1)
for item_name,item_link in zip(seller_name, seller_list):
    print(item_name)
    if '\'' in item_name:
        item_name = item_name.replace("'", "\\'")
        continue
    cur = conn.cursor()
    sql_command = "INSERT INTO sellers (seller_name,seller_link) VALUES ('{}','{}')".format(item_name, item_link)
    cur.execute(sql_command)
    conn.commit()
    cur.close()


cur.close()
conn.close()

print("bar time: ",  (time.time() - start_time)/60, " mins..." )

