"""
dribbble最火的shot
"""
import looter as lt

domain = 'https://dribbble.com'


def crawl(url):
    tree = lt.fetch(url)
    items = tree.css('li.shot-thumbnail')
    for item in items:
        data = {}
        data['title'] = item.css('a strong::text').extract_first()
        data['url'] = f"{domain}{item.css('a::attr(href)').extract_first()}"
        data['author'] = item.css('.display-name::text').extract_first()
        data['fav'] = int(item.css('span.toggle-fav::text').extract_first().strip())
        data['comment'] = int(item.css('li.cmnt span::text').extract_first().strip())
        yield data


if __name__ == '__main__':
    tasklist = [f'{domain}/shots/popular?timeframe=ever&page={n}&per_page=24' for n in range(1, 51)]
    total = lt.crawl_all(crawl, tasklist)
    lt.save(total, name='dribbble.csv', sort_by='fav', no_duplicate=True, order='desc')
