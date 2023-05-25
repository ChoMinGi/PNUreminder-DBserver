from datetime import time
import time
from bs4 import BeautifulSoup
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