from konlpy.tag import Kkma
from konlpy.tag import Okt
import tiktoken


kkma = Kkma()
okt = Okt()
def get_token_count(text):
    tokens = okt.morphs(text)
    return len(tokens)

def get_token_count_tiktoken(sentence, model_name='gpt-3.5-turbo'):
    model = tiktoken.model.load(model_name=model_name)
    tokenizer = tiktoken(model)
    token_list = tokenizer.tokenize(sentence)
    return len(token_list)

def split_text(content, max_length):
    sentences = kkma.sentences(content)
    parts = []
    current_part = []
    current_length = 0

    for sentence in sentences:
        sentence_length = get_token_count(sentence)
        if current_length + sentence_length <= max_length:
            current_part.append(sentence)
            current_length += sentence_length
        else:
            parts.append(' '.join(current_part))
            current_part = [sentence]
            current_length = sentence_length

    if current_part:
        parts.append(' '.join(current_part))

    return parts
