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

def get_institute_lists():
    institute_lists = []
    # main_url, main_class, c_title, c_url, c_date
    # 교양교육원, 도서관,국제처, 교육인증원, 정보화본부
    # institute_lists.append(['https://culedu.pusan.ac.kr/culedu/15027/subview.do',"artclTable artclHorNum1","_artclTdTitle", "https://culedu.pusan.ac.kr/", '_artclTdRdate','td'])
    # institute_lists.append(['https://lib.pusan.ac.kr/community/news/?',"notice-board","subject-text", "https://lib.pusan.ac.kr/", 'date','div'])
    # institute_lists.append(['https://international.pusan.ac.kr/international/14763/subview.do',"artclTable artclHorNum1","_artclTdTitle", "https://international.pusan.ac.kr/", '_artclTdRdate','td'])
    # institute_lists.append(['https://cea.pusan.ac.kr/cea/39260/subview.do?',"artclTable artclHorNum1","_artclTdTitle", "https://cea.pusan.ac.kr/", '_artclTdRdate','td'])
    # institute_lists.append(['https://health.pusan.ac.kr/health/33893/subview.do?',"artclTable artclHorNum1","_artclTdTitle", "https://health.pusan.ac.kr/", '_artclTdRdate','td'])
    # institute_lists.append(['https://uitc.pusan.ac.kr/uitc/28397/subview.do?',"artclTable artclHorNum1","_artclTdTitle", "https://uitc.pusan.ac.kr/", '_artclTdRdate','td'])

    return institute_lists

def get_major_lists():
    major_lists = []
    # 항공우주공하고가,건설융합학부 토목공학전공, 조선해양공학과, 전자공학과, 전기공학과, 재료공학과, 유기시스템공학과, 산업공학과, 도시공학과, 고분자공학과, 건축학과, 화공생명공학부, 환경공학부
    # major_lists.append(['https://aerospace.pusan.ac.kr/aerospace/16375/subview.do?',"artclTable artclHorNum1","_artclTdTitle", "https://aerospace.pusan.ac.kr", '_artclTdRdate','td'])
    # major_lists.append(['https://civil.pusan.ac.kr/civil/16275/subview.do?',"artclTable artclHorNum1","_artclTdTitle", "https://civil.pusan.ac.kr", '_artclTdRdate','td'])
    # major_lists.append(['https://naoe.pusan.ac.kr/naoe/15332/subview.do?',"artclTable artclHorNum1","_artclTdTitle", "https://naoe.pusan.ac.kr", '_artclTdRdate','td'])
    # major_lists.append(['https://ee.pusan.ac.kr/ee/14819/subview.do?',"artclTable artclHorNum1","_artclTdTitle", "https://ee.pusan.ac.kr", '_artclTdRdate','td'])
    # major_lists.append(['https://eec.pusan.ac.kr/eehome/14870/subview.do?',"artclTable artclHorNum1","_artclTdTitle", "https://eec.pusan.ac.kr", '_artclTdRdate','td'])
    # major_lists.append(['https://mse.pusan.ac.kr/mse/38585/subview.do?',"artclTable artclHorNum1","_artclTdTitle", "https://mse.pusan.ac.kr", '_artclTdRdate','td'])
    # major_lists.append(['https://omse.pusan.ac.kr/omse/16246/subview.do?',"artclTable artclHorNum1","_artclTdTitle", "https://omse.pusan.ac.kr", '_artclTdRdate','td'])
    # major_lists.append(['https://ie.pusan.ac.kr/ie/19424/subview.do?',"artclTable artclHorNum1","_artclTdTitle", "https://ie.pusan.ac.kr", '_artclTdRdate','td'])
    # major_lists.append(['https://urban.pusan.ac.kr/urban/17084/subview.do?',"artclTable artclHorNum1","_artclTdTitle", "https://urban.pusan.ac.kr", '_artclTdRdate','td'])
    # major_lists.append(['https://polymer.pusan.ac.kr/polymer/64486/subview.do?',"artclTable artclHorNum1","_artclTdTitle", "https://polymer.pusan.ac.kr", '_artclTdRdate','td'])
    # major_lists.append(['https://archi.pusan.ac.kr/archi/49898/subview.do?',"artclTable artclHorNum1","_artclTdTitle", "https://archi.pusan.ac.kr", '_artclTdRdate','td'])
    # major_lists.append(['https://chemeng.pusan.ac.kr/chemeng/15735/subview.do?',"artclTable artclHorNum1","_artclTdTitle", "https://chemeng.pusan.ac.kr", '_artclTdRdate','td'])
    # major_lists.append(['https://pnuenv.pusan.ac.kr/pnuenv/15177/subview.do',"artclTable artclHorNum1","_artclTdTitle", "https://pnuenv.pusan.ac.kr", '_artclTdRdate','td'])

    return major_lists

def crawlMajor(driver, major_lists):

    try:
        driver.get(major_lists[0])
    except:
        time.sleep(2)
        driver.get(major_lists[0])


    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # 'artclTable artclHorNum1' 클래스를 가진 요소를 찾습니다.
    table = soup.find('table', {'class': major_lists[1]})

    # 테이블 내부의 모든 행을 찾습니다.
    rows = table.find('tbody').find_all('tr')

    non_headline_rows = [row for row in rows if 'headline' not in (row.get('class') or [])]

    data = []

    # 각 행에서 데이터를 수집합니다.
    for row in non_headline_rows:
        title = row.find(major_lists[5], {'class': major_lists[2]}).find('strong').text
        url = major_lists[3]+row.find('a')['href']
        date = row.find('td', {'class': major_lists[4]}).get_text(strip=True)

        data.append({"title": title, "urls": url, "date": date})

    driver.quit()

    print(data)

    return data

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
        num2 =int(num2)+572
        url = f"https://onestop.pusan.ac.kr/page?menuCD=000000000000386&mode=DETAIL&seq={num}"
        url2 = f"https://me.pusan.ac.kr/new/sub05/sub01_01.asp?seq={num2}&db=hakbunotice&page=1&perPage=20&SearchPart=BD_SUBJECT&SearchStr=&page_mode=view"
        date = inner_rows[2].text

        data.append({"title": title, "urls": url, "date": date})
    driver.quit()
    return data


def crawlnstitute(driver, institute_list):

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

    # for institute_list in institute_lists:
    #     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    #     crawlAnnouncement(driver, institute_list)
    #     driver.quit()

    # one_stop_url = "https://onestop.pusan.ac.kr/page?menuCD=000000000000386"
    # crawlOnestop(driver, one_stop_url)
    for major_list in get_major_lists():

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        crawlMajor(driver, major_list)
        driver.quit()


    # save_culedu_announce_to_rds(crawled_data)