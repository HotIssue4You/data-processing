import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud

'''
DB 데이터 불러오기(제목, 뉴스 발행 날짜/시간)

- 30분 이내에 생성된 뉴스만 가져올 것

# chatgpt로 포맷만 설정
# import pymysql
db_config = {
    'host': 'your_host',
    'user': 'your_username',
    'password': 'your_password',
    'database': 'your_database'
}

# MySQL 연결 생성
conn = pymysql.connect(**db_config)
cursor = conn.cursor()

# 현재 시간에서 30분 전 시간 계산
time_threshold = datetime.now() - timedelta(minutes=30)

# 뉴스 기사 제목을 가져오는 쿼리 (업로드 시간이 30분 이내인 것만)
query = "SELECT title FROM news_articles WHERE upload_time >= %s;"

# 쿼리 실행
cursor.execute(query, (time_threshold,))

# 결과 가져오기
news_titles = cursor.fetchall()

# 결과 출력
for title in news_titles:
    print(title[0])
'''

# 데이터 받아오기
data = pd.read_csv("results.csv")
titles = data['title'].to_list()[:300]
titles = ' '.join([title for title in titles])

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

# 워드 클라우드 생성, 이미지 저장 및 시각화
font_path = 'C:\\WINDOWS\\FONTS\\MALGUN.TTF'
wordcloud = WordCloud(width=800, height=400,
                      background_color='white',
                      font_path=font_path).generate(titles)

plt.figure(figsize=(10, 5))
plt.imshow(wordcloud.recolor(colormap='Reds'), interpolation='bilinear')
plt.axis('off')
plt.show()

# 이미지 저장 - savefig(경로)
# plt.savefig('wc.png')