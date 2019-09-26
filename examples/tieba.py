"""
百度贴吧的帖子，用HTML注释反爬，把注释去掉再解析HTML就行
"""
import looter as lt
from pprint import pprint
import requests
from parsel import Selector

domain = 'https://tieba.baidu.com'
keyword = 'bilibili'


def crawl(url):
    text = requests.get(url, headers=lt.DEFAULT_HEADERS).text
    text = text.replace('<!--', '').replace('-->', '')
    tree = Selector(text=text)
    items = tree.css('ul#thread_list li.j_thread_list')
    for item in items:
        data = {}
        data['title'] = item.css('a.j_th_tit::text').extract_first()
        data['abstract'] = item.css('.threadlist_abs::text').extract_first().strip()
        data['url'] = f"{domain}{item.css('a.j_th_tit::attr(href)').extract_first()}"
        data['author'] = item.css('a.frs-author-name::text').extract_first()
        data['reply'] = int(item.css('span.threadlist_rep_num::text').extract_first())
        data['date'] = item.css('.threadlist_reply_date::text').extract_first().strip()
        yield data


if __name__ == '__main__':
    tasklist = [f'{domain}/f?kw={keyword}&ie=utf-8&pn={n}' for n in range(501)]
    total = lt.crawl_all(crawl, tasklist)
    lt.save(total, name=f'tieba_{keyword}.csv', sort_by='reply', order='desc', no_duplicate=True)
