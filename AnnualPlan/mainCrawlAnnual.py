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
    driver.get('https://culedu.pusan.ac.kr/pnuSchdul/culedu/view.do')
    driver.implicitly_wait(3)
    titles = driver.find_elements(By.CLASS_NAME,"_artclTdTitle")


    data=[]
    res=[]

    for title in titles:
        data.append(title.text)

    driver.quit()

    lenHalf = len(data)//2

    for i in range(lenHalf):
        oldCheck= data[2*i]

        if checkOldData(expirationDate,oldCheck):
            continue
        stateCheck = data[2 * i + 1]
        state = doStateCheck(stateCheck)
        split_data = split_date(oldCheck)
        res.append([split_data[0],split_data[1],stateCheck,state])

    return res