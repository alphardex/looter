"""
konachan上的二次元壁纸原图链接
"""
from pathlib import Path
import looter as lt

domain = 'https://konachan.net'


def crawl(url):
    tree = lt.fetch(url)
    imgs = tree.css('a.directlink::attr(href)').extract()
    yield imgs


if __name__ == '__main__':
    tasklist = [f'{domain}/post?page={i}' for i in range(1, 1000)]
    total = lt.crawl_all(crawl, tasklist)
    Path('konachan.txt').write_text('\n'.join(total))
