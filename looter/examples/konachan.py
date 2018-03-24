import looter as lt

domain = 'https://konachan.net'

def crawl(url):
    tree = lt.fetch(url)
    imgs = tree.cssselect('a.directlink')
    lt.async_save_imgs(imgs)


if __name__ == '__main__':
    tasklist = [f'{domain}/post?page={i}' for i in range(1, 9777)]
    result = [crawl(task) for task in tasklist]