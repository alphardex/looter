"""
我看过的电影在豆瓣上的归档
"""
import looter as lt

domain = 'https://movie.douban.com'
MAX_PAGE = 4


def crawl(url):
    tree = lt.fetch(url)
    items = tree.css('.list-view .item')
    for item in items:
        data = {}
        data['title'] = item.css('a::text').extract_first().strip()
        data['url'] = item.css('a::attr(href)').extract_first().strip()
        intro = item.css('span.intro::text').extract_first()
        data['date'] = intro[:10]
        data['intro'] = intro
        yield data


if __name__ == '__main__':
    tasklist = [
        f'{domain}/people/158535797/collect?start={n * 30}&sort=time&rating=all&filter=all&mode=list'
        for n in range(0, MAX_PAGE)
    ]
    total = lt.crawl_all(crawl, tasklist)
    lt.save(total, name='douban_movie_archive.csv')
