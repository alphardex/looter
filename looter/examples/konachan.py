import asyncio
from pathlib import Path
import looter as lt

domain = 'https://konachan.net'
total = []


async def crawl(url):
    tree = await lt.async_fetch(url)
    imgs = tree.css('a.directlink::attr(href)').extract()
    total.extend(imgs)


if __name__ == '__main__':
    tasklist = [f'{domain}/post?page={i}' for i in range(1, 50)]
    loop = asyncio.get_event_loop()
    result = [crawl(task) for task in tasklist]
    loop.run_until_complete(asyncio.wait(result))
    Path('konachan.txt').write_text('\n'.join(total))
