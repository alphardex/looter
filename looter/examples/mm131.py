import re
import looter as lt
from concurrent import futures

domain = 'http://www.mm131.com'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    'Referer': 'http://www.mm131.com/'  # 必须设定referer，否则会被重定向为qq图片
}

def crawl(url):
    tree = lt.fetch(url)
    imgs = tree.cssselect('dl.list-left dd')[:-1]
    for img in imgs:
        link = img.cssselect('a')[0].get('href')
        bango = link.split('/')[-1][:-5]
        detail = lt.fetch(link)
        pagination = detail.cssselect('.content-page .page-ch')[0].text
        max_page = int(re.findall(r'\d+', pagination)[0])
        img_urls = [f'http://img1.mm131.me/pic/{bango}/{n}.jpg' for n in range(1, max_page+1)]
        lt.async_save_imgs(img_urls, headers=headers)


if __name__ == '__main__':
    tasklist = [*[f'{domain}/xinggan/'] ,*[f'{domain}/xinggan/list_6_{n}.html' for n in range(2, 153)]]
    with futures.ThreadPoolExecutor(50) as executor:
        executor.map(crawl, tasklist)
