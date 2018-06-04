import looter as lt
from pprint import pprint
from concurrent import futures

domain = 'https://www.zhipin.com'

def crawl(url):
    tree = lt.fetch(url)
    items = tree.cssselect('.job-list ul li')
    for item in items:
        data = dict()
        data['title'] = item.cssselect('.job-title')[0].text
        data['url'] = domain + item.cssselect('.info-primary h3 a')[0].get('href')
        data['company'] = item.cssselect('.company-text h3 a')[0].text
        data['salary'] = item.cssselect('.info-primary h3 a .red')[0].text
        data['detail'] = item.cssselect('.detail-bottom-text')[0].text
        pprint(data)


if __name__ == '__main__':
    tasklist = [f'{domain}/c101190400/h_101190400/?query=Python&page={n}&ka=page-{n}' for n in range(1, 31)]
    with futures.ThreadPoolExecutor(40) as executor:
        executor.map(crawl, tasklist)
