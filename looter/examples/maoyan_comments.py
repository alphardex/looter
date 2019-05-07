"""
猫眼电影影评，以复联4为例
"""
import requests
import looter as lt
from pprint import pprint
from concurrent import futures

domain = 'http://m.maoyan.com'
movie_id = '248172' # 复仇者联盟4
start_time = '2019-04-24%2002:56:46' # 上映时间
total = []


def crawl(url):
    items = requests.get(url, headers=lt.DEFAULT_HEADERS).json()['cmts']
    for item in items:
        data = {}
        data['nick_name'] = item['nickName']
        data['score'] = item['score']
        data['content'] = item['content']
        data['city_name'] = item['cityName']
        pprint(data)
        total.append(data)


if __name__ == '__main__':
    tasklist = [f'{domain}/mmdb/comments/movie/{movie_id}.json?_v_=yes&offset={15 * n}&startTime={start_time}' for n in range(80)]
    with futures.ThreadPoolExecutor(50) as executor:
        executor.map(crawl, tasklist)
    lt.save(total, name='maoyan_comments.csv', no_duplicate=True)
