"""
konachan上的二次元壁纸原图链接
"""
from concurrent import futures
from pathlib import Path
import looter as lt

domain = 'https://konachan.net'
total = []


def crawl(url):
    tree = lt.fetch(url)
    imgs = tree.css('a.directlink::attr(href)').extract()
    total.extend(imgs)


if __name__ == '__main__':
    tasklist = [f'{domain}/post?page={i}' for i in range(1, 1000)]
    with futures.ThreadPoolExecutor(50) as executor:
        executor.map(crawl, tasklist)
    Path('konachan.txt').write_text('\n'.join(total))
