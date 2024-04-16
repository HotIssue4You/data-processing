import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud
import io
from django.utils import timezone
from datetime import timedelta

'''
명사 추출 작업

- 일단 없이 진행
- 추후에 필요하다고 생각되면 추가

# from konlpy.tag import Okt
# from collections import Counter
# Okt = Okt()
# nouns = Okt.nouns(titles)
# noun_counter = Counter(nouns)
# top_nouns = dict(noun_counter.most_common(100))
# print(top_nouns)
'''


from myapp.models import MyModel

def get_data_from_external_source():
    thirty_minutes_ago = timezone.now() - timedelta(minutes=30)

    # 30분 이내의 데이터 추출
    queryset = MyModel.objects.filter(created_at__gte=thirty_minutes_ago)

    df = pd.DataFrame(list(queryset.values()))

    return df

def make_binary_wordcloud_with_titles(titles):
    font_path = 'C:\\WINDOWS\\FONTS\\MALGUN.TTF'
    wordcloud = WordCloud(width=800, height=400,
                        background_color='white',
                        font_path=font_path).generate(titles)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud.recolor(colormap='Reds'), interpolation='bilinear')
    plt.axis('off')

    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    img_binary = img_buffer.read()
    plt.close()

    return img_binary

def make_binary_wordcloud_with_counter(counter):
    font_path = 'C:\\WINDOWS\\FONTS\\MALGUN.TTF'
    wordcloud = WordCloud(width=800, height=400,
                        background_color='white',
                        font_path=font_path).generate_from_frequencies(counter)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud.recolor(colormap='Reds'), interpolation='bilinear')
    plt.axis('off')

    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    img_binary = img_buffer.read()
    plt.close()
    
    return img_binary

# 이미지 저장 - savefig(경로)
# plt.savefig('wc.png')