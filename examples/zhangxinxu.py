"""
知名CSS博主张鑫旭的博客归档
"""
import re
import looter as lt

domain = 'https://www.zhangxinxu.com'


def crawl(url):
    tree = lt.fetch(url)
    items = tree.css('.type-post')
    for item in items:
        data = {}
        data['title'] = item.css('h2 a::text').extract_first()
        data['url'] = item.css('h2 a::attr(href)').extract_first()
        data['date'] = re.sub(r'年|月|日', '-', item.css('small span.date::text').extract_first())[:-1]
        data['view'] = int(item.css('small::text').re('\d+')[0])
        yield data


if __name__ == '__main__':
    tasklist = [f'{domain}/wordpress/page/{n}/' for n in range(1, 68)]
    total = lt.crawl_all(crawl, tasklist)
    lt.save(total, name='zhangxinxu.csv', sort_by='view', order='desc')
