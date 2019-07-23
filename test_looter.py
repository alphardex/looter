import os
import json
from pathlib import Path
import pytest
import looter as lt

domain = 'https://konachan.com'
broken_domain = 'https://konichee.com'

read_json = lambda path: json.loads(Path(path).read_text())

# test main functions


@pytest.mark.ok
def test_fetch():
    tree = lt.fetch(f'{domain}/post')
    imgs = tree.css('a.directlink::attr(href)').extract()
    assert len(imgs) > 0 and isinstance(imgs[0], str)
    assert not lt.fetch(broken_domain)


@pytest.mark.ok
def test_save():
    # sort_by
    unordered_data = [{'r': 2}, {'r': 3}, {'r': 1}]
    lt.save(unordered_data, name='ordered.json', sort_by='r')
    ordered_data = read_json('ordered.json')
    assert ordered_data[0]['r'] == 1
    os.remove('ordered.json')

    # no_duplicate
    dup_data = [{'a': 1}, {'a': 1}, {'b': 2}]
    lt.save(dup_data, name='unique.json', no_duplicate=True)
    unique_data = read_json('unique.json')
    assert len(dup_data) > len(unique_data)
    os.remove('unique.json')
