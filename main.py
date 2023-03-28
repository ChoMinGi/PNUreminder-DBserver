# Selenium
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select


from AmazonRDSManage.connectRDS import connectRDS
from AnnualPlan.mainCrawlAnnual import crawlAnnualplan
from AnnualPlan.importAnnualPlanDB import importAnnualPlan

from NearRoom.importNearRoomDB import importNearRoom

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)



def crawlDropdown():
    # 웹 페이지 접속
    driver.get('https://onestop.pusan.ac.kr/page?menuCD=000000000000368')
    driver.implicitly_wait(3)
    dropdown = Select(driver.find_elements(By.XPATH,'//*[@id="SCH_BLD_CD"]'))
    items=dropdown.select_by_index(1)
    return items

def checkFirstElement():
    # db 앞 원소 비교후 바뀐 내용이 없으면 후처리 작동제한
    return

def main():



# For Building annualPlan
    # annualLists=crawlAnnualplan(driver)
    # importAnnualPlan(annualLists)

    importNearRoom()

    return

main()
