import asyncio
import looter as lt
from pprint import pprint

domain = 'https://www.javbus.pw'

async def crawl(url):
    tree = await lt.async_fetch(url)
    items = tree.cssselect('#waterfall .item')
    for item in items:
        data = dict()
        data['name'] = item.cssselect('img')[0].get('title')
        data['cover'] = item.cssselect('img')[0].get('src')
        data['link'] = item.cssselect('.movie-box')[0].get('href')
        data['bango'] = item.cssselect('date')[0].text
        data['date'] = item.cssselect('date')[1].text
        pprint(data)


if __name__ == '__main__':
    tasklist = [f'{domain}/page/{i}' for i in range(1, 90)]
    loop = asyncio.get_event_loop()
    result = [crawl(task) for task in tasklist]
    loop.run_until_complete(asyncio.wait(result))