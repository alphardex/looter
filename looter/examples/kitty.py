import asyncio
import looter as lt
from pprint import pprint

domain = 'https://www.torrentkitty.tv'
keyword = 'uncensored'
limit = 500


async def crawl(url):
    tree = await lt.async_fetch(url)
    items = tree.css('table#archiveResult tr')[1:]
    for item in items:
        data = {}
        data['name'] = item.css('td.name::text').extract_first()
        data['size'] = item.css('td.size::text').extract_first()
        data['date'] = item.css('td.date::text').extract_first()
        data['detail'] = domain + item.css('a[rel="information"]::attr(href)').extract_first()
        data['magnet'] = item.css('a[rel="magnet"]::attr(href)').extract_first()
        pprint(data)


if __name__ == '__main__':
    tasklist = [f'{domain}/search/{keyword}/{i}' for i in range(1, limit)]
    loop = asyncio.get_event_loop()
    result = [crawl(task) for task in tasklist]
    loop.run_until_complete(asyncio.wait(result))
