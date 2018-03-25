import json
import looter as lt
from concurrent import futures
from operator import itemgetter

domain = 'https://github.com/tuna/blogroll/blob/master/README.md'
total_rank = []

def get_tasklist(url):
    tree = lt.fetch(url)
    links = tree.cssselect('table tbody tr td:nth-child(3) a')
    return [link.get('href') for link in links]


def crawl(url):
    rank = lt.alexa_rank(url)
    if rank:
        data = {}
        data['site'] = rank[0]
        data['reach'] = int(rank[1])
        data['popularity'] = int(rank[2])
        total_rank.append(data)


if __name__ == '__main__':
    tasklist = get_tasklist(domain)
    with futures.ThreadPoolExecutor(20) as executor:
        executor.map(crawl, tasklist)
    lt.save_as_json(total_rank, name='BlogRank', sort_by='popularity')