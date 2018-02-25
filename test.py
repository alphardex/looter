import looter as lt
from concurrent import futures

domain = ''

def crawl(url):
    src = lt.get_source(url)
    links = src.cssselect()
    lt.save_imgs(links)


if __name__ == '__main__':
    tasklist = list()
    with futures.ThreadPoolExecutor(20) as executor:
        executor.map(crawl, tasklist)