from datetime import time

# Selenium
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

from bs4 import BeautifulSoup

from gpt_summarize.main import summarize_text

MAX_TOKENS = 3000
def truncate_content(content):
    tokens = content.split()
    truncated_tokens = tokens[:MAX_TOKENS]
    return ' '.join(truncated_tokens)


html_lists = []
# main_url, main_class, c_title, c_url, c_date
html_lists.append(['https://culedu.pusan.ac.kr/culedu/15027/subview.do',"artclTable artclHorNum1","_artclTdTitle", "https://culedu.pusan.ac.kr/", '_artclTdRdate','td'])
html_lists.append(['https://lib.pusan.ac.kr/community/news/?',"notice-board","subject-text", "https://lib.pusan.ac.kr/", 'date','div'])
html_lists.append(['https://international.pusan.ac.kr/international/14763/subview.do',"artclTable artclHorNum1","_artclTdTitle", "https://international.pusan.ac.kr/", '_artclTdRdate','td'])

print(html_lists)
def crawlAnnouncement(driver, html_list):

    try:
        driver.get(html_list[0])
    except:
        time.sleep(2)
        driver.get(html_list[0])


    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # 'artclTable artclHorNum1' 클래스를 가진 요소를 찾습니다.
    table = soup.find('table', {'class': html_list[1]})

    # 테이블 내부의 모든 행을 찾습니다.
    rows = table.find('tbody').find_all('tr')

    data = []

    MAX_LENGTH = 1000

    # 각 행에서 데이터를 수집합니다.
    for row in rows:
        title = row.find(html_list[5], {'class': html_list[2]}).get_text(strip=True)
        url = html_list[3]+row.find('a')['href']
        date = row.find('td', {'class': html_list[4]}).get_text(strip=True)

        data.append({"title": title, "urls": url, "date": date})

    driver.quit()

    print(data)

    return data


if __name__ == "__main__":
    # Initialize the webdriver
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')

    # Crawl the data
    for html_list in html_lists:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        crawlAnnouncement(driver, html_list)
        driver.quit()

    # save_culedu_announce_to_rds(crawled_data)