import os
import json
import pytest
import requests
import looter as lt

domain = 'https://konachan.com'
broken_domain = 'https://konichee.com'

# test main functions


@pytest.mark.ok
def test_fetch():
    tree = lt.fetch(f'{domain}/post')
    imgs = tree.css('a.directlink::attr(href)').extract()
    assert len(imgs) > 0 and isinstance(imgs[0], str)
    assert not lt.fetch(broken_domain)


@pytest.mark.ok
def test_links():
    res = requests.get(f'{domain}/post')
    r = lt.links(res)
    assert isinstance(r, list)
    assert '#' not in r and '' not in r
    assert len(set(r)) == len(r)

    search_imgs = lt.links(res, search='image')
    assert all(['image' in img for img in search_imgs])

    re_imgs = lt.links(res, pattern='.*/image/.*')
    assert all(['image' in img for img in re_imgs])


@pytest.mark.ok
def test_save_as_json():
    data = [{
        'rank': 2,
        'name': 'python'
    }, {
        'rank': 1,
        'name': 'js'
    }, {
        'rank': 3,
        'name': 'java'
    }]
    lt.save_as_json(data, sort_by='rank')
    with open('data.json', 'r') as f:
        ordered_data = json.loads(f.read())
    assert ordered_data[0]['rank'] == 1
    os.remove('data.json')

    dup_data = [{'a': 1}, {'a': 1}, {'b': 2}]
    lt.save_as_json(dup_data, no_duplicate=True)
    with open('data.json', 'r') as f:
        unique_data = json.loads(f.read())
    assert len(dup_data) > len(unique_data)
    os.remove('data.json')
