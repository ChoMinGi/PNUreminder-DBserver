from datetime import time
import time
from bs4 import BeautifulSoup
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