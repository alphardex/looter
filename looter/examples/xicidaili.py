import looter as lt
from concurrent import futures

domain = 'http://www.xicidaili.com'
proxies = []

def crawl(url):
    tree = lt.fetch(url)
    items = tree.cssselect('table tr')[1:]
    for item in items:
        schema = item.cssselect('td')[-5].text.lower()
        ip = item.cssselect('td')[1].text
        port = item.cssselect('td')[2].text
        proxy = f'{schema}://{ip}:{port}'
        print(proxy)
        proxies.append(proxy)


if __name__ == '__main__':
    tasklist = [f'{domain}/nn/{i}' for i in range(1, 100)]
    with futures.ThreadPoolExecutor(20) as executor:
        executor.map(crawl, tasklist)
    lt.save_as_json(proxies, name='proxies')