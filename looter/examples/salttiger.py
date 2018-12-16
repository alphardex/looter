from pprint import pprint
import looter as lt

domain = 'https://salttiger.com'


def crawl(url):
    tree = lt.fetch(url)
    items = tree.css('ul.car-monthlisting li')
    total = []
    for item in items:
        data = {}
        data['name'] = item.css('a::text').extract_first()
        data['url'] = item.css('a::attr(href)').extract_first()
        data['comments'] = int(item.css('span::text').re_first(r'(\d+)'))
        pprint(data)
        total.append(data)
    return total


if __name__ == '__main__':
    task = f'{domain}/archives/'
    result = crawl(task)
    lt.save_as_json(result, name='salttiger.json', sort_by='comments')
