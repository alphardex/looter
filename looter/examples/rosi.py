import looter as lt
from concurrent import futures

domain = 'http://www.rosi.cc'

def crawl(url):
    tree = lt.fetch(url)
    imgs = tree.cssselect('ul.b_ul li a img')
    lt.save_imgs(imgs, random_name=True)


if __name__ == '__main__':
    video = [f'{domain}/x/sp/list_10_{i}' for i in range(1, 18)]
    mousefold = [f'{domain}/x/app/list_12_{i}' for i in range(1, 42)]
    underwear = [f'{domain}/x/rosi/list_1_{i}' for i in range(1, 179)]
    tasklist = [*video, *mousefold, *underwear]
    with futures.ThreadPoolExecutor(20) as executor:
        executor.map(crawl, tasklist)