"""
A simple linear spider, you can crawl whole site slowly with it.
""" 
import looter as lt
def download(url):
    src = lt.get_source(url)
    links = src.cssselect('a.directlink')
    lt.save_imgs(links)

if __name__ == '__main__':
    tasklist = reversed(list(f'https://konachan.net/post?page={9777-i}' for i in range(1, 9777)))
    r = [download(task) for task in tasklist]
