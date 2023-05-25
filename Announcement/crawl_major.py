from datetime import time
import time
from bs4 import BeautifulSoup

import logging

logging.basicConfig(filename='major_lv_log.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def crawl_major(driver, middle_url, major_url):

    try:
        driver.get(major_url)
    except Exception as e:
        logging.error(f"Error during getting page {major_url}, retrying. Error: {str(e)}")
        time.sleep(2)
        try:
            driver.get(major_url)
        except Exception as e:
            logging.error(f"Error during retry of getting page {major_url}. Error: {str(e)}")
            driver.quit()
            return

    try:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        table = soup.find('table', {'class': "artclTable artclHorNum1"})
        rows = table.find('tbody').find_all('tr')

        non_headline_rows = [row for row in rows if 'headline' not in (row.get('class') or [])]

        data = []
        for row in non_headline_rows:
            title = row.find('td', {'class': "_artclTdTitle"}).find('strong').text
            url = middle_url+row.find('a')['href']
            date = row.find('td', {'class': '_artclTdRdate'}).get_text(strip=True)

            data.append({"title": title, "urls": url, "date": date})

        driver.quit()


    except Exception as e:
        logging.error(f"major_crawl_error at {major_url}. Error: {str(e)}")
        driver.quit()
        return

    logging.info(data)
    return data
