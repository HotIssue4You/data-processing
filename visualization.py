import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
from PIL import Image
import io

from django.utils import timezone
from django.http import Http404, HttpResponseServerError
from django.db.utils import OperationalError
from .models import Article
from datetime import datetime, timedelta
import pytz

'''
- 시각화 자료 : wordcloud, barplot, donutchart

수정할 사항은 모두 "#"으로 주석 처리
- 디자인, 폰트 경로, 날짜 형식, 이미지 크기 등
'''

'''
- get_titles_within_thirty_minutes_from_django
<파라미터>
date : 날짜("2024-01-01"), str
time : 시간("15:30"), str
type : 'title' or 'noun_title', 시각화를 위한 열 선택

<역할>
date/time에 따른 30분 이내의 'title' or 'noun_title' 열의 시리즈를 리스트로 변환해서 반환

<예외 처리>
1. 올바른 형식의 date/time이 아닐 경우 : 현재 utc 시간으로 작동
2. 입력한 시간에 기사가 존재하지 않을 경우 : 404 code 반환
3. 데이터베이스 연결 오류가 발생할 경우 : 500 Code 반환
'''
def get_titles_within_thirty_minutes_from_django(date=None, time=None, type='title'):
    # date/time의 형식은 달라질 수 있음
    try:
        date = datetime.strptime(date, '%Y-%m-%d').date()
        time = datetime.strptime(time, '%H:%M').time()
    except:
        date = datetime.now(pytz.utc).date()
        time = datetime.now(pytz.utc).time()

    input_datetime = timezone.make_aware(datetime.combine(date, time))
    thirty_minutes_ago = input_datetime - timedelta(minutes=30)

    try:
        queryset = Article.objects.filter(created_at__lte=input_datetime, created_at__gte=thirty_minutes_ago)
        titles = list(queryset.values_list(type, flat=True))
    except OperationalError as e:
        raise HttpResponseServerError("Database connection error: {}".format(e))
    
    if len(titles) == 0:
        raise Http404("No articles found within the last 30 minutes.")
    
    return titles

'''
- parse_titles
<파라미터>
titles : 'title' or 'noun_title' 리스트
(get_titles_within_thirty_minutes_from_django을 거친 데이터)

<역할>
제목 단위를 단어 단위로 쪼개 리스트로 반환
'''
def parse_titles(titles):
    return ' '.join(title for title in titles).split()

'''
- generate_binary
<역할>
현재 생성한 그래프를 바이너리로 변환하여 반환
(모든 그래프에 들어가서 함수로 만듦)

<예외 처리>
1. 이미지 저장-읽기 과정에서 오류가 발생할 경우 : 500 Code 반환
'''
def generate_binary():
    try:
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        img_binary = buf.read()
        plt.close()
        return img_binary
    except OSError as e:
        raise HttpResponseServerError("Error while saving image: {}".format(e))

'''
- make_binary_wordcloud_with_titles
<파라미터>
date : 날짜("2024-01-01"), str
time : 시간("15:30"), str

<역할>
date/time에 따른 30분 이내의 'title' 데이터를 활용한 워드 클라우드 바이너리 반환
'''
def make_wordcloud_with_title(date=None, time=None, *args):
    titles_list = get_titles_within_thirty_minutes_from_django(date, time, 'title')
    titles = parse_titles(titles_list)
    noun_counter = Counter(titles)
    top_nouns = dict(noun_counter.most_common(100))

    # 폰트 변경 가능
    font_path = "./mainpage/static/fonts/ChosunNm.ttf"
    wordcloud = WordCloud(width=800, height=400,
                        background_color='white',
                        font_path=font_path,
                        colormap = 'summer').generate_from_frequencies(top_nouns)

    # figsize(크기), recolor(색깔) 조절 필요
    plt.figure(figsize=(10, 5)) 
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')

    return generate_binary()

'''
- make_barplot_with_noun_frequency
<파라미터>
date : 날짜("2024-01-01"), str
time : 시간("15:30"), str

<역할>
date/time에 따른 30분 이내의 'noun_title' 데이터를 활용한 빈도수 막대 그래프 바이너리 반환
'''

def make_barplot_with_frequency_of_noun_title(date=None, time=None, *args):
    noun_titles_list = get_titles_within_thirty_minutes_from_django(date, time, 'noun_title')
    noun_titles = parse_titles(noun_titles_list)
    noun_counter = Counter(noun_titles)
    top_nouns = dict(noun_counter.most_common(10))

    plt.rc("font", family= "Malgun Gothic") 
    plt.rc("axes", unicode_minus = False)

    # figsize(크기), style(디자인), label 수정 필요
    sns.set_theme(font ='Malgun Gothic',
                  rc = {'axes.unicode_minus' : False},
                  style ='whitegrid')
    plt.figure(figsize=(10, 5))
    sns.barplot(x = list(top_nouns.keys()), y = list(top_nouns.values()))
    plt.xlabel('단어')
    plt.ylabel('빈도수')
    plt.title('뉴스 제목 단어 빈도수')
    
    return generate_binary()

'''
- make_donutchart_with_noun_ratio
<파라미터>
date : 날짜("2024-01-01"), str
time : 시간("15:30"), str

<역할>
date/time에 따른 30분 이내의 'noun_title' 데이터를 활용한 비율 도넛 차트 바이너리 반환

<예외 처리>
1. 단어 개수가 10개 미만인 경우 : 단어 전체로 그래프 생성
'''
def make_donutchart_with_ratio_of_noun_title(date=None, time=None, *args):
    noun_titles_list = get_titles_within_thirty_minutes_from_django(date, time, 'noun_title')
    noun_titles = parse_titles(noun_titles_list)
    noun_counter = Counter(noun_titles)
    top_nouns = dict(noun_counter)

    plt.rc("font", family= "Malgun Gothic") 
    plt.rc("axes", unicode_minus = False)

    # figsize(크기), style(디자인), label 수정 필요
    sns.set_theme(font ='Malgun Gothic',
                  rc = {'axes.unicode_minus' : False},
                  style ='whitegrid')
    plt.figure(figsize=(10, 5))
    
    data = list(top_nouns.values())
    labels = list(top_nouns.keys())

    if len(data) < 10:
        plt.pie(data, labels=labels, autopct='%1.1f%%', startangle=90)
    else:
        total = sum(data)
        top_10_data = data[:10]
        top_10_labels = labels[:10]

        other_data = [total - sum(top_10_data)]
        other_labels = ['기타']

        # 상위 10개 데이터와 기타 데이터를 합쳐서 도넛 차트 그리기
        plt.pie(top_10_data + other_data, labels=top_10_labels + other_labels, autopct='%1.1f%%', startangle=90)

    # 도넛 차트에 중앙에 원 추가하기
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    plt.gca().add_artist(centre_circle)
    plt.title('단어 빈도에 따른 비율')
    plt.axis('equal')

    return generate_binary()

'''
- change_binary_to_image
<역할>
바이너리 -> 이미지 변환 테스트를 위한 함수

<사용 예시>
a = make_barplot_with_noun_frequency(date, time)
change_binary_to_image(a)
'''
def change_binary_to_image(binary_data):
    image = Image.open(io.BytesIO(binary_data))
    image.show()