import looter as lt
from concurrent import futures

domain = 'https://www.doutula.com'

def crawl(url):
    tree = lt.fetch(url)
    links = tree.cssselect('img.lazy')
    links = [link.get('data-original') for link in links]
    lt.save_imgs(links)


if __name__ == '__main__':
    tasklist = [f'{domain}/article/list/?page={i}' for i in range(1, 551)]
    with futures.ThreadPoolExecutor(50) as executor:
        executor.map(crawl, tasklist)