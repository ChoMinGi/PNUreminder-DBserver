
# Selenium
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import mysql.connector



def crawlAnnouncement(driver):
    # Get HTML
    driver.get('https://culedu.pusan.ac.kr/culedu/15027/subview.do')
    driver.implicitly_wait(3)
    titles_elements = driver.find_elements(By.CLASS_NAME, "_artclTdTitle")

    data = []

    for idx, title_element in enumerate(titles_elements):
        title = title_element.text
        link = title_element.find_element(By.TAG_NAME, 'a').get_attribute('href')

        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[-1])

        driver.get(link)
        driver.implicitly_wait(3)
        content = driver.find_element(By.CLASS_NAME, "artclView").get_attribute('innerHTML')

        data.append({"title": title, "content": content})

        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        driver.implicitly_wait(3)

    driver.quit()

    print(data)

    return data

def save_to_database(data):
    # Connect to the database
    cnx = mysql.connector.connect(user='your_user', password='your_password', host='your_host', database='your_database')
    cursor = cnx.cursor()

    # Insert data into the database
    for item in data:
        title = item['title']
        content = item['content']
        insert_query = "INSERT INTO your_table (title, content) VALUES (%s, %s)"
        cursor.execute(insert_query, (title, content))

    # Commit the changes and close the connection
    cnx.commit()
    cursor.close()
    cnx.close()

if __name__ == "__main__":
    # Initialize the webdriver
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    # Crawl the data
    crawled_data = crawlAnnouncement(driver)

    # Save the data to the database
    # save_to_database(crawled_data)
