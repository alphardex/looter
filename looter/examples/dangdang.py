import looter as lt
from pprint import pprint
from concurrent import futures

domain = 'http://category.dangdang.com'

def get_tasklist(url):
    res = lt.send_request(url)
    categories = lt.links(res, search='/cp')
    tasklist = [f'{domain}/pg{n}-{c[1:]}' for c in categories for n in range(1, 101)]
    return tasklist


def crawl(url):
    tree = lt.fetch(url)
    items = tree.cssselect('ul.bigimg li')
    for item in items:
        data = dict()
        data['title'] = item.cssselect('a')[0].get('title').strip()
        data['detail'] = item.cssselect('a')[0].get('href')
        data['price'] = float(item.cssselect('p.price .search_now_price')[0].text[1:])
        data['author'] = item.cssselect('p.search_book_author a')[0].get('title')
        data['date'] = item.cssselect('p.search_book_author span')[1].text.strip()[1:]
        data['press'] = item.cssselect('p.search_book_author a')[-1].text
        data['comments'] = int(item.cssselect('p.search_star_line a')[0].text[:-3])
        pprint(data)


if __name__ == '__main__':
    tasklist = get_tasklist(f'{domain}/pg1-cp01.00.00.00.00.00.html')
    with futures.ThreadPoolExecutor(20) as executor:
        executor.map(crawl, tasklist)