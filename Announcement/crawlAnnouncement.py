
# Selenium
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from Announcement.announcement import save_culedu_announce_to_rds

from gpt_summarize.main import summarize_text

MAX_TOKENS = 3500 - 150  # 150 tokens for completion
def truncate_content(content):
    tokens = content.split()
    truncated_tokens = tokens[:MAX_TOKENS]
    return ' '.join(truncated_tokens)
def crawlAnnouncement(driver):
    # Get HTML
    driver.get('https://culedu.pusan.ac.kr/culedu/15027/subview.do')
    driver.implicitly_wait(3)
    titles_elements = driver.find_elements(By.CLASS_NAME, "_artclTdTitle")

    data = []

    # Collect all URLs first
    urls_list = []
    for title_element in titles_elements:
        title = title_element.text
        urls = title_element.find_element(By.TAG_NAME, 'a').get_attribute('href')
        urls_list.append({"title": title, "urls": urls})

    # Visit each URL and perform summarization
    for url_info in urls_list:
        title = url_info['title']
        urls = url_info['urls']

        driver.get(urls)
        driver.implicitly_wait(3)
        content = driver.find_element(By.CLASS_NAME, "artclView").text



        # Then, in the crawlAnnouncement function:
        truncated_content = truncate_content(content)
        for i in range(5):
            summarize_text(title, truncated_content)

        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[-1])

        data.append({"title": title, "urls": urls})

        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        driver.implicitly_wait(3)

        break

    driver.quit()

    print(data)

    return data



if __name__ == "__main__":
    # Initialize the webdriver
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    # Crawl the data
    # crawled_data = crawlAnnouncement(driver)
    crawlAnnouncement(driver)

    # Save the data to the database
    # save_culedu_announce_to_rds(crawled_data)