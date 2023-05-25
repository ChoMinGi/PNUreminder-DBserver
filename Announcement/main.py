from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from crawl_major import crawl_major
from url_lists.major_list import major_list, err_list


from aws.mongoDB_connection import mongoDB_connection

import logging

logging.basicConfig(filename='main_lv_log.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)

if __name__ == "__main__":
    # Initialize the webdriver
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')

    # for institute_list in institute_lists:
    #     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    #     crawlAnnouncement(driver, institute_list)
    #     driver.quit()

    # one_stop_url = "https://onestop.pusan.ac.kr/page?menuCD=000000000000386"
    # crawlOnestop(driver, one_stop_url)

    mongo_client = mongoDB_connection()
    mongo_db = mongo_client.get_database("major_announcement")
    # for major_list in major_list():
    for major_list in err_list():
        major_url=major_list[0]
        middle_url = major_url[1]
        major_name=major_list[2]

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        datas = crawl_major(driver, middle_url, major_url)

        mongo_collection = mongo_db[major_name]

        if datas is not None:
            for data in datas:
                if mongo_collection.count_documents({'urls': data['urls']}, limit=1) == 0:
                    mongo_collection.insert_one(data)
                else:
                    logging.info(f"Document with urls {data['urls']} already exists.")
        else:
            logging.warning("No data to process")

        driver.quit()


    # save_culedu_announce_to_rds(crawled_data)