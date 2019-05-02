"""
知乎最高点赞的视频排行
"""
import os
import json
from pprint import pprint
from concurrent import futures
import requests
from looter import DEFAULT_HEADERS, save

domain = 'https://www.zhihu.com'
total = []
encoding = 'utf-8'


def crawl(url):
    items = requests.get(url, headers=DEFAULT_HEADERS).json()['data']
    for item in items:
        target = item['target']
        question = target.get('question')
        if not question or not target.get('topic_thumbnails_extra_info'):
            continue
        data = {}
        data['title'] = question['title']
        data['source'] = f"{domain}/question/{question['id']}/answer/{target['id']}"
        data['vote'] = target['voteup_count']
        pprint(data)
        total.append(data)


def generate():
    with open('data.json', encoding=encoding) as i, open('zhihu_top_video.md', 'w', encoding=encoding) as o:
        data = json.loads(i.read())
        o.writelines(f"{i+1}. [{d['title']}]({d['source']})赞数：{d['vote']}\n" for i, d in enumerate(data))


if __name__ == '__main__':
    tasklist = [f'{domain}/api/v4/topics/19776749/feeds/essence?&offset={10 * n}&limit=10' for n in range(100)]
    with futures.ThreadPoolExecutor(50) as executor:
        executor.map(crawl, tasklist)
    save(total, sort_by='vote', order='desc')
    generate()
    os.remove('data.json')
