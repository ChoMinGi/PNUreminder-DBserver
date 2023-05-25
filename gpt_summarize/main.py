import openai

from bs4 import BeautifulSoup

# API 키 설정

def get_each_html(driver,title, url):
    driver.get(url)
    driver.implicitly_wait(10)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    content = soup.find('div', {'class': 'artclView'}).get_text(strip=True)

    # 본문 내용을 여러 부분으로 나눕니다.
    # parts = split_text(content, MAX_LENGTH)
    #
    # # 각 부분을 요약합니다.
    # for part in parts:
    #     summarized_part = summarize_text(title, part)
    #     print(summarized_part)
    try:
        summarized_part = summarize_text(title, content)
        return summarized_part
    except:
        return


def summarize_text(title,text):
    openai.api_key = "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"
    # 요약할 텍스트 입력
    prompt = f"제목 : {title} 내용:{text}\n\n 이 게시글을 사용자가 검색으로 접근하거나 이 게시글이 필요한 사용자에게 이 글을 설명할 수 있는 키워드를 5개에서 8개 사이로 보여줘 출력 형식은 키워드 사이에 , 를 추가해서 설명없이 출력하게 해주세요."

    # 요청을 위한 파라미터 설정
    params = {
        "engine": "text-davinci-003",
        "prompt": prompt,
        "max_tokens": 200,
        "n": 5,
        "stop": None,
        "temperature": 0.5,
    }

    # GPT API 요청
    response = openai.Completion.create(**params)

    # 요약 결과 추출 및 반환
    summary = response.choices[0].text.strip()
    return summary

