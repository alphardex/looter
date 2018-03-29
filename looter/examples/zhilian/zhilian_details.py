import json
import looter as lt
from concurrent import futures
from pprint import pprint

domain = 'http://sou.zhaopin.com'
total = []

def get_tasklist(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.loads(f.read())
    tasklist = [job['link'] for job in data]
    return tasklist


def crawl(url):
    tree = lt.fetch(url)
    data = dict()
    cols = ['salary', 'place', 'date', 'nature', 'experience', 'degree', 'amount', 'category']
    for i, col in enumerate(cols):
        data[col] = tree.cssselect('ul.terminal-ul li')[i].cssselect('strong')[0].text
    data['salary'] = "".join(data['salary'].split())
    del data['place']
    data['date'] = tree.cssselect('ul.terminal-ul li')[2].cssselect('strong #span4freshdate')[0].text
    data['category'] = tree.cssselect('ul.terminal-ul li')[7].cssselect('strong a')[0].text
    detail = tree.cssselect('.tab-inner-cont p')
    data['detail'] = ''.join([p.text for p in detail if p.text]).strip()
    pprint(data)
    total.append(data)


if __name__ == '__main__':
    tasklist = get_tasklist('zhilian_jobs.json')
    tasklist.reverse()
    with futures.ThreadPoolExecutor(40) as executor:
        executor.map(crawl, tasklist)
    lt.save_as_json(total, name='zhilian_details')