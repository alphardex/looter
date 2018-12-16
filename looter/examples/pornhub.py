import time
import re
import json
import requests
import pymongo
import looter as lt
from pprint import pprint
from concurrent import futures

domain = 'https://www.pornhub.com'
client = pymongo.MongoClient()
db = client.pornhub
col = db.video

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36',
    'Referer': 'https://www.pornhub.com/'
}
cookies = lt.read_cookies()


def crawl(url):
    tree = lt.fetch(url, use_cookies=True, headers=headers)
    time.sleep(0.5)
    items = tree.css('.wrap')
    for item in items:
        data = {}
        data['views'] = item.css('span.views var::text').extract_first()
        data['rating'] = int(item.css('.value::text').extract_first()[:-1])
        viewKey = item.css('a::attr(href)').extract_first().split('=')[-1]
        video = requests.get(f'https://{domain}/embed/{viewKey}', cookies=cookies, headers=headers).text
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
    with futures.ThreadPoolExecutor(10) as executor:
        executor.map(crawl, tasklist)
