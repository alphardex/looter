import asyncio
import looter as lt
from pprint import pprint

domain = 'https://nyaa.si'


async def crawl(url):
    tree = await lt.async_fetch(url)
    posts = tree.css('tr.default')
    for post in posts:
        data = {}
        data['name'] = post.css('td[colspan="2"] a::attr(title)').extract()[-1]
        data['category'] = post.css('td[style="padding:0 4px;"] a::attr(title)').extract()[-1]
        link_and_magnet = post.css('td.text-center')[0]
        data['link'] = f"{domain}{link_and_magnet.css('a::attr(href)').extract_first()}"
        data['magnet'] = link_and_magnet.css('a::attr(href)').extract()[1]
        data['size'] = post.css('td.text-center::text').extract()[3]
        data['date'] = post.css('td.text-center::text').extract()[4]
        data['seeders'] = int(post.css('td.text-center::text').extract()[5])
        data['leechers'] = int(post.css('td.text-center::text').extract()[6])
        data['downloads'] = int(post.css('td.text-center::text').extract()[7])
        pprint(data)


if __name__ == '__main__':
    tasklist = [f'{domain}/?p={i}' for i in range(1, 500)]
    loop = asyncio.get_event_loop()
    result = [crawl(task) for task in tasklist]
    loop.run_until_complete(asyncio.wait(result))
