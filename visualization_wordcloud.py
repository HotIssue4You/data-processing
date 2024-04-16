import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud
import io
from datetime import datetime, timedelta
from django.utils import timezone
from .models import Article

def get_titles_within_thirty_minutes_from_django(date, time):

    # date, time 형식에 따라 변경(현재는 문자열로 입력, 예시 : ("2024-01-01", "15:30"))
    date = datetime.strptime(date, '%Y-%m-%d').date()
    time = datetime.strptime(time, '%H:%M').time()
    input_datetime = timezone.make_aware(datetime.combine(date, time))

    thirty_minutes_ago = input_datetime - timedelta(minutes=30)

    queryset = Article.objects.filter(created_at__lte=input_datetime, created_at__gte=thirty_minutes_ago)

    titles = list(queryset.values_list('title', flat=True))
    return titles

def parse_titles(titles):
    return ' '.join(title for title in titles)

def make_binary_wordcloud_with_titles():
    titles_list = get_titles_within_thirty_minutes_from_django()
    titles = parse_titles(titles_list)

    # 폰트 경로(font_path) 설정 필요, 설정 안하면 글자 깨짐
    font_path = 'C:\\WINDOWS\\FONTS\\MALGUN.TTF'
    wordcloud = WordCloud(width=800, height=400,
                        background_color='white',
                        font_path=font_path).generate(titles)

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