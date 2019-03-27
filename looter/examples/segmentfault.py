import asyncio
from datetime import datetime
import pymysql
import looter as lt

domain = 'https://segmentfault.com'
connection = pymysql.connect(
    host='localhost',
    db='techattic',
    charset='utf8mb4',
    user='test',
    password='test123')
cursor = connection.cursor()


async def crawl(url):
    tree = await lt.async_fetch(url)
    items = tree.css('.stream-list .stream-list__item')
    for item in items:
        title = item.css('h2.title a::text').extract_first()
        author = item.css('ul.author li span a::text').extract_first()
        source = f"{domain}{item.css('h2.title a::attr(href)').extract_first()}"
        vote = int(item.css('span.stream__item-zan-number::text').extract_first())
        site = 'segmentfault'
        date = datetime.utcnow()
        view = 0
        comment = 0
        collect = int(item.css('span.blog--bookmark__text').re_first(r'\d+'))
        row = (title, author, source, vote, site, date, view, comment, collect)
        print(row)
        try:
            cursor.execute(
                'INSERT INTO `article` (`title`, `author`, `source`, `vote`, `site`, `date`, `view`, `comment`, `collect`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
                row)
            connection.commit()
        except Exception as e:
            print(e)


if __name__ == '__main__':
    tasklist = [f'{domain}/blogs/hottest/monthly?page={n}' for n in range(1, 137)]
    loop = asyncio.get_event_loop()
    result = [crawl(task) for task in tasklist]
    loop.run_until_complete(asyncio.wait(result))
    cursor.close()
    connection.close()
