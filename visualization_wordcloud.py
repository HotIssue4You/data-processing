import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud
import io
from django.utils import timezone
from datetime import timedelta
from .models import Article

def get_titles_within_thirty_minutes_from_django():
    thirty_minutes_ago = timezone.now() - timedelta(minutes=30)

    # 30분 이내의 데이터 추출
    queryset = Article.objects.filter(created_at__gte=thirty_minutes_ago)

    df = pd.DataFrame(list(queryset.values()))['title']
    return df.to_list()

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