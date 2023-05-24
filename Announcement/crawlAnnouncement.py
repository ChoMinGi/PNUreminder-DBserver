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


institute_lists = []
# main_url, main_class, c_title, c_url, c_date
# 교양교육원, 도서관,국제처, 교육인증원, 정보화본부
one_stop_url= "https://onestop.pusan.ac.kr/page?menuCD=000000000000386"
# institute_lists.append(['https://culedu.pusan.ac.kr/culedu/15027/subview.do',"artclTable artclHorNum1","_artclTdTitle", "https://culedu.pusan.ac.kr/", '_artclTdRdate','td'])
# institute_lists.append(['https://lib.pusan.ac.kr/community/news/?',"notice-board","subject-text", "https://lib.pusan.ac.kr/", 'date','div'])
# institute_lists.append(['https://international.pusan.ac.kr/international/14763/subview.do',"artclTable artclHorNum1","_artclTdTitle", "https://international.pusan.ac.kr/", '_artclTdRdate','td'])
# institute_lists.append(['https://cea.pusan.ac.kr/cea/39260/subview.do?',"artclTable artclHorNum1","_artclTdTitle", "https://cea.pusan.ac.kr/", '_artclTdRdate','td'])
# institute_lists.append(['https://health.pusan.ac.kr/health/33893/subview.do?',"artclTable artclHorNum1","_artclTdTitle", "https://health.pusan.ac.kr/", '_artclTdRdate','td'])
# institute_lists.append(['https://uitc.pusan.ac.kr/uitc/28397/subview.do?',"artclTable artclHorNum1","_artclTdTitle", "https://uitc.pusan.ac.kr/", '_artclTdRdate','td'])

print(institute_lists)

def crawlOnestop(driver, one_stop_url):

    try:
        driver.get(one_stop_url)
    except:
        time.sleep(2)
        driver.get(one_stop_url)


    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # 'artclTable artclHorNum1' 클래스를 가진 요소를 찾습니다.
    table = soup.find('table', {'class': "table table-hover table-bordered"})

    # 테이블 내부의 모든 행을 찾습니다.
    rows = table.find('tbody').find_all('tr')
    data = []

    for row in rows[5:]:
        inner_rows = row.find_all('td')
        title = inner_rows[0].get_text(strip=True)
        num = row.find('th').get_text(strip=True)
        num = int(num)+200
        url = f"https://onestop.pusan.ac.kr/page?menuCD=000000000000386&mode=DETAIL&seq={num}"
        date = inner_rows[2].text

        data.append({"title": title, "urls": url, "date": date})
    driver.quit()
    return data


def crawlAnnouncement(driver, institute_list):

    try:
        driver.get(institute_list[0])
    except:
        time.sleep(2)
        driver.get(institute_list[0])


    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # 'artclTable artclHorNum1' 클래스를 가진 요소를 찾습니다.
    table = soup.find('table', {'class': institute_list[1]})

    # 테이블 내부의 모든 행을 찾습니다.
    rows = table.find('tbody').find_all('tr')

    data = []

    MAX_LENGTH = 1000

    # 각 행에서 데이터를 수집합니다.
    for row in rows:
        title = row.find(institute_list[5], {'class': institute_list[2]}).get_text(strip=True)
        url = institute_list[3]+row.find('a')['href']
        date = row.find('td', {'class': institute_list[4]}).get_text(strip=True)

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
    # for institute_list in institute_lists:
    #     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    #     crawlAnnouncement(driver, institute_list)
    #     driver.quit()

    one_stop_url = "https://onestop.pusan.ac.kr/page?menuCD=000000000000386"
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    # crawlOnestop(driver, one_stop_url)

    driver.quit()


    # save_culedu_announce_to_rds(crawled_data)