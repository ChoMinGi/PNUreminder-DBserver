from selenium.webdriver.common.by import By

from datetime import datetime
from datetime import timedelta

def checkOldData(due,data):
    str_datetime = str(data[:10])
    format = "%Y.%m.%d"
    dt_datetime = datetime.strptime(str_datetime,format)
    if due-dt_datetime>timedelta(0):
        return 1
    else:
        return 0

def split_date(whole_date):
    start_end = []
    start_end.append(whole_date[:10])
    start_end.append(whole_date[13:])
    return  start_end

def doStateCheck(context):
    # 학부, 신입생, 타대생, 대학원, 휴.복학생
    if "휴·복학" in context:
        state = 5
    elif "대학원" in context:
        state = 4
    elif "타대생" in context:
        state = 3
    elif "신입생" in context:
        state = 2
    elif "학부" in context:
        state = 1
    else:
        state = 0
    return state

def crawlAnnualplan(driver):

    expirationStdDay = 90
    expirationDate = datetime.today() - timedelta(expirationStdDay)

    lenHalf=0
    # Get HTML
    # driver.get('https://culedu.pusan.ac.kr/pnuSchdul/culedu/view.do')
    print("Web page loading...")
    driver.get('https://www.pusan.ac.kr/kor/CMS/Haksailjung/view.do?mCode=MN076')
    driver.implicitly_wait(5)

    # th 태그의 텍스트를 추출
    th_elements = driver.find_elements(By.CSS_SELECTOR, ".acacal-tbl th.term")
    th_texts = [elem.text for elem in th_elements if elem.text.strip() != '']

    # td 태그의 텍스트를 추출
    td_elements = driver.find_elements(By.CSS_SELECTOR, ".acacal-tbl td.text")
    td_texts = [elem.text for elem in td_elements if elem.text.strip() != '']
    res=[]

    driver.quit()

    for i in range(len(th_elements)):
        if checkOldData(expirationDate,th_texts[i]):
            continue
        state = doStateCheck(td_texts[i])
        split_data = split_date(th_texts[i])
        res.append([split_data[0],split_data[1],td_texts[i],state])
        print(res)
    return res