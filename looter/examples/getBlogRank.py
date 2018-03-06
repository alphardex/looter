import re
import json
import looter as lt
from pprint import pprint
from concurrent import futures
from operator import itemgetter

domain = 'http://data.alexa.com'
total_rank = []

def get_targets(url):
    src = lt.get_source(url)
    links = src.cssselect('table tbody tr td:nth-child(3) a')
    return [link.get('href') for link in links]


def crawl(url):
    src = lt.send_request(url).text
    reach_rank = re.findall('REACH[^\d]*(\d+)', src)
    popularity_rank = re.findall('POPULARITY[^\d]*(\d+)', src)
    if reach_rank and popularity_rank:
        data = {}
        site = url.split('=')[-1]
        data['site'] = site
        data['reach'] = reach_rank[0]
        data['popularity'] = popularity_rank[0]
        total_rank.append(data)


if __name__ == '__main__':
    targets = get_targets('https://github.com/tuna/blogroll/blob/master/README.md')
    tasklist = list(f'{domain}/data?cli=10&dat=snbamz&url={target}' for target in targets)
    with futures.ThreadPoolExecutor(20) as executor:
        executor.map(crawl, tasklist)
    r = sorted(total_rank, key=itemgetter('popularity'))
    with open('blogRank.json', 'w') as f:
        f.write(json.dumps(r))