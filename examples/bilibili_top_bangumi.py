"""
bilibili番剧排行榜
"""
from pprint import pprint
from concurrent import futures
import requests
import arrow
import looter as lt

domain = 'https://bangumi.bilibili.com'
total = []


def crawl(url):
    items = requests.get(url).json()['result']['data']
    for item in items:
        data = {}
        data['番名'] = item['title']
        data['链接'] = item['link']
        order = item['order']
        score = order.get('score')
        data['评分'] = float(score[:-1]) if score else 0.0
        data['放松日期'] = arrow.get(order['pub_date']).naive
        season_id = item['season_id']
        data['id'] = season_id
        season = requests.get(f'{domain}/ext/web_api/season_count?season_id={season_id}&season_type=1').json()['result']
        data['追番人数'] = season['favorites']
        data['播放量'] = season['views']
        data['硬币数'] = season['coins']
        data['弹幕数'] = season['danmakus']
        pprint(data)
        total.append(data)


if __name__ == '__main__':
    tasklist = [f'{domain}/media/web_api/search/result?order=3&sort=0&page={n}&season_type=1&pagesize=30' for n in range(1, 106)]
    with futures.ThreadPoolExecutor(20) as executor:
        executor.map(crawl, tasklist)
    lt.save(total, name='bilibili_top_bangumi.csv', sort_by='追番人数', order='desc')
