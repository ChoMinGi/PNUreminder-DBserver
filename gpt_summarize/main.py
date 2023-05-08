import openai

# API 키 설정


def summarize_text(title,text):
    openai.api_key = "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"
    # 요약할 텍스트 입력
    prompt = f"제목 : {title} 내용:{text}\n\n 이 게시글을 사용자가 검색으로 접근하거나 이 게시글이 필요한 사용자에게 이 글을 설명할 수 있는 키워드를 5개에서 8개 사이로 보여줘 출력 형식은 키워드 사이에 , 를 추가해서 설명없이 출력하게 해주세요."

    # 요청을 위한 파라미터 설정
    params = {
        "engine": "text-davinci-002",
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
    print(summary)
    return summary

# 사용 예시
