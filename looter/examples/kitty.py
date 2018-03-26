import asyncio
import looter as lt
from pprint import pprint

domain = 'https://www.torrentkitty.tv'
keyword = 'uncensored'
limit = 500

async def crawl(url):
    tree = await lt.async_fetch(url)
    items = tree.cssselect('table#archiveResult tr')[1:]
    for item in items:
        data = dict()
        data['name'] = item.cssselect('td.name')[0].text
        data['size'] = item.cssselect('td.size')[0].text
        data['date'] = item.cssselect('td.date')[0].text
        data['detail'] = domain + item.cssselect('a[rel="information"]')[0].get('href')
        data['magnet'] = item.cssselect('a[rel="magnet"]')[0].get('href')
        pprint(data)


if __name__ == '__main__':
    tasklist = [f'{domain}/search/{keyword}/{i}' for i in range(1, limit)]
    loop = asyncio.get_event_loop()
    result = [crawl(task) for task in tasklist]
    loop.run_until_complete(asyncio.wait(result))