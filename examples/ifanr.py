"""
爱范儿的文章，按点赞数排序
"""
import requests
import looter as lt

domain = 'https://www.ifanr.com'


def crawl(url):
    item_data_list = []
    items = requests.get(url, headers=lt.DEFAULT_HEADERS).json()['objects']
    for item in items:
        item_data = {}
        item_data['title'] = item['post_title']
        item_data['category'] = item['post_category']
        item_data['created_at'] = item['created_at_format']
        item_data['url'] = item['post_url']
        item_data_list.append(item_data)
    ids = ','.join(item['post_id'] for item in items)
    stat_data_list = []
    stats = requests.get(
        f'https://sso.ifanr.com/api/v5/wp/article/stats/?limit=50&post_id__in={ids}',
        headers=lt.DEFAULT_HEADERS).json()['objects']
    for stat in stats:
        stat_data = {}
        stat_data['favorite_count'] = stat['favorite_count']
        stat_data['like_count'] = stat['like_count']
        stat_data['share_count'] = stat['share_count']
        stat_data_list.append(stat_data)
    data_list = [{**data[0], **data[1]} for data in zip(item_data_list, stat_data_list)]
    yield data_list


if __name__ == '__main__':
    tasklist = [
        f'https://sso.ifanr.com//api/v5/wp/web-feed/?published_at__lte=2019-05-25+07%3A00%3A11&limit=20&offset={n * 20}'
        for n in range(1900)
    ]
    total = lt.crawl_all(crawl, tasklist)
    lt.save(total, name='ifanr.csv', no_duplicate=True, sort_by='like_count', order='desc')
