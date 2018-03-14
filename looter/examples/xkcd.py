import looter as lt
from concurrent import futures

domain = 'https://xkcd.com'

def crawl(url):
    tree = lt.fetch(url)
    links = tree.cssselect('#comic img')
    lt.save_imgs(links)


if __name__ == '__main__':
    tasklist = [f'{domain}/{i}' for i in range(1, 1960)]
    with futures.ThreadPoolExecutor(50) as executor:
        executor.map(crawl, tasklist)