import time
import sys
from random import shuffle
import psycopg2
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium_stealth import stealth
from info import info
from mails import mailahmet
from email.mime.text import MIMEText


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
res_list = []
for row in result:
    seller_list.append(row[0])

SIZE = len(seller_list)
total_time = 0
for i, url in enumerate(seller_list):
    sub_start_time = time.time()
    options = Options()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('disable-infobars')
    options.add_argument('--headless=new')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    stealth(driver,
       languages=["en-US", "en"],
       vendor="Google Inc.",
       platform="Win32",
       webgl_vendor="Intel Inc.",
       renderer="Intel Iris OpenGL Engine",
       fix_hairline=True,
    )

    driver.get(url)
    seller_name = driver.title
    BOX_XPATH = "//*[@id=\"kitap_Adi\"]"
    wait = WebDriverWait(driver, 20)
    try:
        search_box = wait.until(EC.visibility_of_element_located((By.XPATH, BOX_XPATH)))
    except:
        driver.quit()
        continue
    print((i + 1),". seller. ", (SIZE - i - 1), " sellers remain...")
    search_box.send_keys(sys.argv[1])
    BUTTON_XPATH = "/html/body/div[2]/div/div/div[2]/form/div/div[3]/button"
    button = wait.until(EC.element_to_be_clickable((By.XPATH, BUTTON_XPATH)))
    button.click()
    URL = str(driver.current_url)
    driver.quit()

    driver = webdriver.Chrome(options=options)
    stealth(driver,
       languages=["en-US", "en"],
       vendor="Google Inc.",
       platform="Win32",
       webgl_vendor="Intel Inc.",
       renderer="Intel Iris OpenGL Engine",
       fix_hairline=True,
    )

    driver.get(URL)
    try:
        book_list = driver.find_element(By.CLASS_NAME, 'list-cell')
    except:
        sub_finish_time = time.time()
        sub_execution_time = (sub_finish_time - sub_start_time) / 60
        total_time = int(total_time + sub_execution_time)
        avg_time = total_time / (i + 1)
        estimated_end_time = avg_time * (SIZE - i + 1)

        driver.close()
        continue

    items = book_list.find_elements(By.CLASS_NAME, 'break-work')
    print("====================", seller_name, "====================")
    for idx, item in enumerate(items):
        xpath_row = '/html/body/div[2]/div/div/div[2]/div[6]/ul/li[{}]/div[2]/div/div[1]/h4/a'.format(idx + 1)
        xpath_price = '/html/body/div[2]/div/div/div[2]/div[6]/ul/li[{}]/div[2]/div/div[2]/div[3]'.format(idx + 1)
        try:
            x = item.find_element(By.XPATH, xpath_row)
            y = item.find_element(By.XPATH, xpath_price)
            title = x.get_attribute("title")
            TITLE = str(title)
            price = str(y.text)
            print(price)
            res_list.append((str(seller_name), str(title), (price)))

        except Exception as inst:
            message = inst
            print()

    driver.close()
    print("=======================================================\n")
    sub_finish_time = time.time()
    sub_execution_time = (sub_finish_time - sub_start_time) / 60
    total_time = int(total_time + sub_execution_time)
    avg_time = total_time / (i + 1)
    estimated_end_time = avg_time * (SIZE - i + 1)
    print("This operation took ", round(sub_execution_time, 2), " minutes")
    print("Estimated finish time: ", round(estimated_end_time), " minutes...")
    driver.quit()

end_time = time.time()
print("Total Executione time: ", (end_time - start_time) / 60, "minutes...")
file_name = sys.argv[1]
mail_message = "Subject: {} \n\n".format(sys.argv[1])
file = open('/home/om/Documents/{}.txt'.format(file_name), 'w')
result_message = "Toplam " + str(len(res_list)) + " kitap bulunmustur."
file.write(result_message)
for obj in res_list:
    mail_message = mail_message + " " + obj[0] + "-" + "-" + obj[1] + "-" + (obj[2]) + '\n\n'
    file.write(obj[0] + "-" + "-" + obj[1] + "-" + (obj[2]) + '\n\n')
time.sleep(14)
msg = mail_message.encode('utf-8')
mailahmet(msg)
