import requests
from bs4 import BeautifulSoup
import time

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


def crawl_main():
    # 웹페이지 URL
    url = "https://www.pusan.ac.kr/kor/CMS/Contents/Contents.do?mCode=MN003"

    # 페이지를 요청하고 HTML을 가져옵니다
    response = requests.get(url)
    html = response.text

    # BeautifulSoup 객체 생성
    soup = BeautifulSoup(html, 'html.parser')

    # div 태그에서 class가 c-tab01인 모든 요소를 찾습니다
    divs = soup.find_all('div', {'class': 'c-tab01'})

    # 결과를 저장할 리스트
    result_urls = []
    result_names = []

    # 각 div 태그에 대해 반복합니다
    for div in divs:
        # div 내부의 모든 a 태그를 찾습니다
        a_tags = div.find_all('a')

        # 각 a 태그에 대해 반복합니다
        for a in a_tags:
            # a 태그의 href 속성 값과 text 값을 리스트로 만들어 results에 추가합니다
            result_urls.append(a['href'])
            result_names.append(a.text)


    return (result_urls, result_names)


def crawl_college(result):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # 결과를 저장할 새로운 리스트
    result_urls = result[0]
    result_names = result[1]
    i=0
    # 각 결과에 대해 반복합니다
    for result in result_urls:

        sub_url = result
        sub_response = requests.get(sub_url)
        sub_html = sub_response.text

        # BeautifulSoup 객체를 생성합니다
        sub_soup = BeautifulSoup(sub_html, 'html.parser')

        # ul 태그에서 class가 gradu-list인 모든 요소를 찾습니다
        uls = sub_soup.find('ul', {'class': 'gradu-list'})
        lis = uls.find_all('li')
        print(result_names[i])
        result_list = []
        i+=1
        for li in lis:
            major_name = li.find('a').text
            driver.get(li.find('a')['href'])
            final_url = driver.current_url
            split_url = final_url.split("/", 3)
            middle_url = "/".join(split_url[:3])
            response = requests.get(final_url)
            html = response.text
            sub_soup = BeautifulSoup(html, 'html.parser')
            a_tag = sub_soup.find('a', {'class': 'recentBbsMore'})
            # 만약 a 태그가 있다면, 그것의 href 값을 가져옵니다
            if a_tag:
                result_list.append([middle_url + a_tag['href'], middle_url, major_name])
            else:
                result_list.append(["수동 추가 요망",middle_url, major_name])
            # 결과를 출력합니다
        print(result_list)
    return


def test():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    uls = [['http://bkorea.pusan.ac.kr/', '국어국문학과'], ['http://japan.pusan.ac.kr/', '일어일문학과'], ['http://french.pusan.ac.kr/', '불어불문학과'], ['http://russia.pusan.ac.kr/', '노어노문학과'], ['http://china.pusan.ac.kr/', '중어중문학과'], ['http://pnuenglish.pusan.ac.kr/', '영어영문학과'], ['http://german.pusan.ac.kr/', '독어독문학과'], ['http://hanmun.pusan.ac.kr/', '한문학과'], ['http://linguistics.pusan.ac.kr/', '언어정보학과'], ['http://history.pusan.ac.kr/', '사학과'], ['http://philosophy.pusan.ac.kr/', '철학과'], ['https://archaeology.pusan.ac.kr/archaeology/index..do', '고고학과']]
    result = []
    inner_results = []

    for ul in uls:
        # ul 내부의 모든 a 태그를 찾습니다
        driver.get(ul[0])
        final_url = driver.current_url
        response = requests.get(final_url)
        time.sleep(1)
        html = response.text
        sub_soup = BeautifulSoup(html, 'html.parser')
        a_tag = sub_soup.find('a', {'class': 'recentBbsMore'})
        # 만약 a 태그가 있다면, 그것의 href 값을 가져옵니다
        if a_tag:
            result.append([ul[0][:-1]+a_tag['href'],ul[1]])
        else:
            result.append(["수동 추가 요망",ul[1]])

        # inner_results를 결과에 추가합니다

        # 결과를 출력합니다
    print(result)
    return


crawl_college(crawl_main())