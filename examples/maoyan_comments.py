"""
猫眼电影影评，以复联4为例，先把时间节点都爬下来，再组合成url用线程池爬，这样效率更高
"""
import arrow
import requests
import looter as lt
from pprint import pprint
from pathlib import Path
from concurrent import futures

domain = 'http://m.maoyan.com'
movie_id = '248172'  # 复仇者联盟4
total_timestamps = []
total_items = []


def get_timestamps():
    start_time = arrow.now().format()[:-6]  # 开爬时间，默认为今天
    end_time = '2019-04-30 00:00:00'  # 爬到时间
    while arrow.get(start_time) > arrow.get(end_time):
        url = f'{domain}/mmdb/comments/movie/{movie_id}.json?_v_=yes&offset=0&startTime={start_time}'
        start_time = requests.get(url).json()['cmts'][-1]['startTime']
        print(start_time)
        total_timestamps.append(start_time)
    Path('maoyan_comment_timestamps.txt').write_text('\n'.join(total_timestamps))


def crawl(url):
    items = requests.get(url, headers=lt.DEFAULT_HEADERS).json()['cmts']
    for item in items:
        data = {}
        data['nick_name'] = item['nickName']
        data['score'] = item['score']
        data['content'] = item['content']
        data['city_name'] = item['cityName']
        pprint(data)
        total_items.append(data)


if __name__ == '__main__':
    get_timestamps()
    start_times = Path('maoyan_comment_timestamps.txt').read_text().split('\n')
    tasklist = [f'{domain}/mmdb/comments/movie/{movie_id}.json?_v_=yes&offset=0&startTime={t}' for t in start_times]
    with futures.ThreadPoolExecutor(50) as executor:
        executor.map(crawl, tasklist)
    lt.save(total_items, name='maoyan_comments.csv', no_duplicate=True)
