import pandas as pd
import re


def process(title):
    """
    기사 제목으로부터 '[포토 뉴스]'와 같은 헤더를 지우고, 모든 특수문자를 지움.
    :param title:
    :return:
    """
    title = remove_header(title)
    return remove_specialChar(title)

def remove_header(title):
    """
    기사 제목으로부터 '[포토 뉴스]', '[카드 뉴스]'와 같은 헤더를 지움
    :param title:
    :return:
    """
    pattern = r'\[[^]]*\]'
    return re.sub(pattern=pattern, repl='', string=title)

def remove_specialChar(title):
    """
    기사 제목으로부터 모든 특수 문자("-=+,#/\?:^.@*\"※~ㆍ!』‘|\(\)\[\]`\'…》\”\“\’·")를 지움
    :param title:
    :return:
    """
    pattern = '[-=+,#/\?:^.@*\"※~ㆍ!』‘|\(\)\[\]`\'…》\”\“\’·]'
    return re.sub(pattern=pattern, repl='', string=title)


"""
코드 확인용 메인 함수
"""
# def main():
#     data = pd.read_csv('results.csv')
#     for title in data['title']:
#         print(f"before processing: {title}")
#         print(f"after processing: {process(title)}")
#
# if __name__ == "__main__":
#     main()