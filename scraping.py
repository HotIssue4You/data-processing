import requests
import pandas as pd
import datetime
from pytz import timezone
from bs4 import BeautifulSoup as bs


def get_news_data(url, user_agent, df):
    res = requests.get(url, user_agent)
    soup = bs(res.text, "lxml")
    news_list = soup.find("ul", "list_news _infinite_list").find_all("li", "bx")
    for news in news_list:
        news_contents = news.find("a", "news_tit")
        news_info = news.find_all("span", "info")
        time_info = news_info[-1]
        minutes = int(time_info.text[:-3])
        current = datetime.datetime.now(timezone('Asia/Seoul'))
        created_at = current - datetime.timedelta(minutes=minutes)
        df.loc[len(df)] = [news_contents['title'], created_at, news_contents['href'], time_info.text]



def main():
    url = ("https://search.naver.com/search.naver?where=news&query=%EB%89%B4%EC%8A%A4&sm=tab_opt&sort=1&photo=0&field"
           "=0&pd=0&ds=&de=&docid=&related=0&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so"
           "%3Add%2Cp%3Aall&is_sug_officeid=0&office_category=0&service_area=0")
    user_agent = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/83.0.4103.97 Safari/537.36"}
    df = pd.DataFrame(columns=['title', 'created_at', 'link_url', 'time_offset'])
    try:
        get_news_data(url, user_agent, df)
    except (KeyError, ValueError):
        df.to_csv("results3.csv")
        return

    df.to_csv("results3.csv")


if __name__ == "__main__":
    main()
