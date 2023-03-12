from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import time
import pymysql
import pymysql.cursors

connection = pymysql.connect(
  host="localhost",
  user="root",
  password="1234",
  database="pnuagent",
)


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)


def crawl_dropdown():
    # 웹 페이지 접속
    driver.get('https://onestop.pusan.ac.kr/page?menuCD=000000000000368')
    driver.implicitly_wait(3)
    dropdown = Select(driver.find_elements(By.XPATH,'//*[@id="SCH_BLD_CD"]'))
    items=dropdown.select_by_index(1)
    return items



driver.quit()

with connection:
    with connection.cursor() as cursor:
        sql = "INSERT INTO buildings (name, room) VALUES (%s, %s)"
        cursor.execute(sql, ('이름', '한글숫자123abc'))

    connection.commit()


    with connection.cursor() as cursor:
        sql = "SELECT * FROM buildings WHERE name=%s"
        cursor.execute(sql, ('이름',))
        result = cursor.fetchall()
        print(result)
        print("Data inserted successfully.")






