"""
阮一峰的博客文章，按留言数排序
"""
import looter as lt
from pprint import pprint

domain = 'http://www.ruanyifeng.com'
categories_texts = [
    '散文', '观点与感想', '算法与数学', '开发者手册', '理解计算机', 'JavaScript', '周刊', '创业', '译文集',
    '科技爱好者', '文学爱好者', '英语爱好者', '剪贴板', '笔记本', '杂物间', 'Joel谈软件', 'USENET'
]


def get_categories():
    tree = lt.fetch('http://www.ruanyifeng.com/blog/archives.html')
    categories = tree.css('.module-categories ul.module-list li a::attr(href)').re('.*?/blog/\D+/')
    return categories


def get_total(categories):
    total = []
    for category in categories:
        tree = lt.fetch(category)
        links = tree.css('a::attr(href)').re('.*?/blog/\d+/\d+/.*')
        hints = tree.css('span.hint::text').extract()
        hints = [hint[1:][:-1].split('@') for hint in hints]
        titles = [title for title in tree.css('li a::text').extract() if title not in categories_texts]
        data = [{'title': title, 'url': link, 'comments': int(hint[0]), 'date': hint[1]} for title, link, hint in zip(titles, links, hints)]
        pprint(data)
        total.extend(data)
    return total


if __name__ == '__main__':
    categories = get_categories()
    total = get_total(categories)
    lt.save(total, name='ruanyifeng.csv', sort_by='comments', order='desc')
