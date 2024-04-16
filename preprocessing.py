import pandas as pd
import re


def process(data):
    """
    1. 기사 목록들로부터 중복 기사들을 유니크하게 만들고,
    2. 각 기사 제목으로부터 '[포토 뉴스]'와 같은 헤더를 지우고,
    3. 모든 특수문자를 지움.
    * 순서 바뀌면 안됨
    :param data:
    :return 전처리 완료된 기사 목록(제목, 게시 시간):
    """
    unique_data = to_unique(data)
    processed_data = pd.DataFrame(columns=['title', 'created_at'])
    for idx, row in unique_data.iterrows():
        header_removed = remove_header(row['title'])
        processed_title = remove_specialChar(header_removed)
        processed_data.loc[len(processed_data)] = [processed_title, row['created_at']]
    return processed_data

def to_unique(data):
    return data.drop_duplicates(subset='title')

def remove_header(title):
    """
    기사 제목으로부터 '[포토 뉴스]', '[카드 뉴스]'와 같은 헤더를 지움
    :param title:
    :return 헤더를 지운 기사 제목:
    """
    pattern = r'\[[^]]*\]'
    return re.sub(pattern=pattern, repl='', string=title)

def remove_specialChar(title):
    """
    기사 제목으로부터 모든 특수 문자("-=+,#/\?:^.@*\"※~ㆍ!』‘|\(\)\[\]`\'…》\”\“\’·")를 지움
    :param title:
    :return 특수 문자를 지운 기사 제목:
    """
    pattern = '[-=+,#/\?:^.@*\"※~ㆍ!』‘|\(\)\[\]`\'…》\”\“\’·]'
    return re.sub(pattern=pattern, repl='', string=title)


"""
코드 확인용 메인 함수
"""
def main():
    data = pd.read_csv('results.csv')
    processed = process(data)
    for title in processed['title']:
        print(title)


if __name__ == "__main__":
    main()