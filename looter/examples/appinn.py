"""
小众软件，按评价数排序
"""
import asyncio
import looter as lt
from pprint import pprint

domain = 'https://www.appinn.com'
categories = ['windows', 'chrome']
total = []


async def crawl(url):
    tree = await lt.async_fetch(url)
    items = tree.css('section#latest-posts article.post-box')
    for item in items:
        data = {}
        data['title'] = item.css('a::attr(title)').extract_first()
        data['url'] = item.css('a::attr(href)').extract_first()
        data['date'] = item.css('span.thetime span::text').extract_first()
        data['comments'] = int(item.css("a[itemprop='interactionCount']::text").extract_first())
        pprint(data)
        total.append(data)


if __name__ == '__main__':
    tasklist = [f'{domain}/category/{category}/page/{n}/' for n in range(1, 21) for category in categories]
    loop = asyncio.get_event_loop()
    result = [crawl(task) for task in tasklist]
    loop.run_until_complete(asyncio.wait(result))
    lt.save(total, name='appinn.csv', sort_by='comments', order='desc')
