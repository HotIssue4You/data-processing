import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import io
from datetime import datetime, timedelta
from django.utils import timezone
from collections import Counter
from .models import Article
from PIL import Image

'''
- 시각화 자료 : wordcloud, barplot, donutchart

수정할 사항은 모두 "#"으로 주석 처리
- 디자인, 폰트 경로, 날짜 형식, 이미지 크기 등
'''

'''
- get_titles_within_thirty_minutes_from_django
date : 날짜("2024-01-01"), str
time : 시간("15:30"), str
type : 'title' or 'noun_title', 시각화를 위한 열 선택

date/time에 따른 30분 이내의 'title' or 'noun_title' 열의 시리즈를 리스트로 변환해서 반환
'''
def get_titles_within_thirty_minutes_from_django(date, time, type='title'):
    # date/time의 형식은 달라질 수 있음
    date = datetime.strptime(date, '%Y-%m-%d').date()
    time = datetime.strptime(time, '%H:%M').time()
    input_datetime = timezone.make_aware(datetime.combine(date, time))

    thirty_minutes_ago = input_datetime - timedelta(minutes=30)

    queryset = Article.objects.filter(created_at__lte=input_datetime, created_at__gte=thirty_minutes_ago)

    titles = list(queryset.values_list(type, flat=True))
    return titles

'''
- parse_titles
titles : 'title' or 'noun_title' 리스트
(get_titles_within_thirty_minutes_from_django을 거친 데이터)

제목 단위를 단어 단위로 쪼개 리스트로 반환
'''
def parse_titles(titles):
    return ' '.join(title for title in titles).split()

'''
- make_binary_wordcloud_with_titles
date : 날짜("2024-01-01"), str
time : 시간("15:30"), str

date/time에 따른 30분 이내의 'title' 데이터를 활용한 워드 클라우드 바이너리 반환
'''
def make_binary_wordcloud_with_titles(date, time):
    titles_list = get_titles_within_thirty_minutes_from_django(date, time)
    titles = parse_titles(titles_list)
    noun_counter = Counter(titles)
    top_nouns = dict(noun_counter.most_common(100))

    # 폰트 경로(font_path) 설정 필요, 설정 안하면 글자 깨짐
    font_path = 'C:\\WINDOWS\\FONTS\\MALGUN.TTF'
    wordcloud = WordCloud(width=800, height=400,
                        background_color='white',
                        font_path=font_path).generate_from_frequencies(top_nouns)

    # figsize(크기), recolor(색깔) 조절 필요
    plt.figure(figsize=(10, 5)) 
    plt.imshow(wordcloud.recolor(colormap='Reds'), interpolation='bilinear')
    plt.axis('off')

    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    img_binary = img_buffer.read()
    plt.close()

    return img_binary

'''
- make_barplot_with_noun_frequency
date : 날짜("2024-01-01"), str
time : 시간("15:30"), str

date/time에 따른 30분 이내의 'noun_title' 데이터를 활용한 빈도수 막대 그래프 바이너리 반환
'''
def make_barplot_with_noun_frequency(date, time):
    noun_titles_list = get_titles_within_thirty_minutes_from_django(date, time, 'noun_title')
    noun_titles = parse_titles(noun_titles_list)
    noun_counter = Counter(noun_titles)
    top_nouns = dict(noun_counter.most_common(100))

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
    fig = plt.gcf()
    
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    binary_data = buf.read()
    plt.close()

    return binary_data

'''
- make_donutchart_with_noun_ratio
date : 날짜("2024-01-01"), str
time : 시간("15:30"), str

date/time에 따른 30분 이내의 'noun_title' 데이터를 활용한 비율 도넛 차트 바이너리 반환
'''
def make_donutchart_with_noun_ratio(date, time):
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

    total = sum(data)
    top_10_data = data[:10]
    top_10_labels = labels[:10]
    top_10_percentage = sum(top_10_data) / total * 100

    other_data = [total - sum(top_10_data)]
    other_labels = ['기타']
    other_percentage = 100 - top_10_percentage

    fig, ax = plt.subplots()
    ax.pie(top_10_data + other_data, labels=top_10_labels + other_labels, autopct='%1.1f%%', startangle=90)
    centre_circle = plt.Circle((0,0),0.70,fc='white')
    fig.gca().add_artist(centre_circle)
    ax.set_title('단어 빈도에 따른 비율')
    ax.axis('equal')
    
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    binary_data = buf.read()
    plt.close()
    
    return binary_data

'''
- change_binary_to_image
바이너리 -> 이미지 변환 테스트를 위한 함수

<사용 예시>
a = make_barplot_with_noun_frequency(date, time)
change_binary_to_image(a)
'''
def change_binary_to_image(binary_data):
    image = Image.open(io.BytesIO(binary_data))
    image.show()