import os
import json
import re
import pytest
import requests
import looter as lt


domain = 'konachan.com'
broken_domain = 'konichee.com'

# test main functions


@pytest.mark.ok
def test_fetch():
    tree = lt.fetch(f'{domain}/post')
    imgs = tree.css('a.directlink::attr(href)').extract()
    assert len(imgs) > 0 and isinstance(imgs[0], str)
    assert not lt.fetch(broken_domain)


@pytest.mark.ok
def test_links():
    res = requests.get(lt.ensure_schema(f'{domain}/post'))
    r = lt.links(res)
    search_imgs = lt.links(res, search='image')
    re_imgs = lt.links(res, pattern='.*/image/.*')
    assert isinstance(r, list)
    assert '#' not in r and '' not in r
    assert len(set(r)) == len(r)
    assert all(['image' in img for img in search_imgs])
    assert all(['image' in img for img in re_imgs])


@pytest.mark.ok
def test_save_as_json():
    data = [{'rank': 2, 'name': 'python'}, {'rank': 1, 'name': 'js'}, {'rank': 3, 'name': 'java'}]
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


@pytest.mark.ok
def test_login():
    params = {'df': 'mail126_letter', 'from': 'web', 'funcid': 'loginone', 'iframe': '1', 'language': '-1', 'passtype': '1', 'product': 'mail126',
              'verifycookie': '-1', 'net': 'failed', 'style': '-1', 'race': '-2_-2_-2_db', 'uid': 'webscraping123@126.com', 'hid': '10010102'}
    postdata = {'username': 'webscraping123@126.com', 'savelogin': '1',
                'url2': 'http://mail.126.com/errorpage/error126.htm', 'password': '0up3VmfKCh22'}
    url = "https://mail.126.com/entry/cgi/ntesdoor?"
    res, ses = lt.login(url, postdata, params=params)
    index_url = re.findall(r'href = "(.*?)"', res.text)[0]
    index = ses.get(index_url)
    message_count = re.findall(
        r"('messageCount'.*?).*?('unreadMessageCount'.*?),", index.text)[0]
    assert message_count[0] == "'messageCount'"
    assert not lt.login(broken_domain, postdata)


# test utils

@pytest.mark.ok
def test_ensure_schema():
    assert lt.ensure_schema(domain).startswith('http')
    assert not lt.ensure_schema(f'http://{domain}').startswith('https')
    assert lt.ensure_schema('//fuckshit.png').startswith('https://')


@pytest.mark.ok
def test_read_cookies():
    url = 'http://httpbin.org/cookies'
    cookies = lt.read_cookies(filename='./looter/examples/cookies.txt')
    r = requests.get(url, cookies=cookies)
    assert dict(cookies.items()) == r.json()['cookies']
