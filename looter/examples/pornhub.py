import re
import json
import pymongo
import looter as lt
from pprint import pprint
from concurrent import futures

domain = 'https://www.pornhub.com'
client = pymongo.MongoClient()
db = client.pornhub
col = db.video


def crawl(url):
    tree = lt.fetch(url)
    items = tree.cssselect('.wrap')
    for item in items:
        data = dict()
        data['views'] = lt.expand_num(item.cssselect('span.views var')[0].text)
        data['rating'] = int(item.cssselect('.value')[0].text[:-1])
        viewKey = item.cssselect('a')[0].get('href').split('=')[-1]
        video = lt.send_request(f'{domain}/embed/{viewKey}').text
        flashvars = re.findall('var flashvars =(.*?),\n', video)[0]
        info = json.loads(flashvars)
        data['title'] = info.get('video_title')
        data['duration'] = info.get('video_duration')
        data['image'] = info.get('image_url')
        data['link'] = info.get('link_url')
        data['quality_480p'] = info.get('quality_480p')
        pprint(data)
        col.insert_one(data)


if __name__ == '__main__':
    tasklist = [f'{domain}/video?page={n}' for n in range(1, 2273)]
    with futures.ThreadPoolExecutor(50) as executor:
        executor.map(crawl, tasklist)
