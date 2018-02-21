"""
A simple concurrent spider, you can crawl whole site with it at a high speed.
""" 
from concurrent import futures
from miniko_batch import download

if __name__ == '__main__':
    tasklist = reversed(list(f'https://konachan.net/post?page={9777-i}' for i in range(1, 9777)))
    with futures.ThreadPoolExecutor(20) as executor:
        executor.map(download, tasklist)