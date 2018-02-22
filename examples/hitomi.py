import looter as lt
from pprint import pprint
from concurrent import futures

domain = 'https://hitomi.la'
limit = 10

def crawl(url):
    src = lt.get_source(url)
    posts = src.cssselect('.cg')
    for post in posts:
        data = dict()
        title = post.cssselect('h1 a')[0]
        data['name'] = title.text
        data['url'] = domain + title.get('href')
        data['artist'] = post.cssselect('.artist-list')[0].text.strip()
        dj_content = post.cssselect('.dj-content .dj-desc')[0]
        td = dj_content.cssselect('tr td')
        data['series'] = td[1].text.strip() or 'N/A'
        data['type'] = td[3].cssselect('a')[0].text.strip()
        data['language'] = td[5].text.strip()
        data['tags'] = ', '.join([tag.text for tag in td[7].cssselect('.relatedtags ul li a')]) or 'N/A'
        data['date'] = post.cssselect('.dj-content p.cg-date')[0].text
        pprint(data)
        # You can define your save_data function in advance and call it here :)


if __name__ == '__main__':
    tasklist = list(f'{domain}/type/gamecg-all-{limit-i}.html' for i in range(1, limit))
    with futures.ThreadPoolExecutor(10) as executor:
        executor.map(crawl, tasklist)