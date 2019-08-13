"""
爬取百度指数的某一时间段内的特定关键词的所有指数
"""
import time
import looter as lt
import requests
import pandas as pd
import arrow
from loguru import logger

words = []  # 关键词列表
start_date = '2018-01-29'
end_date = '2018-12-31'
kinds = ['all', 'pc', 'wise']
domain = 'http://index.baidu.com'
headers = {
    'Host':
    'index.baidu.com',
    'Connection':
    'keep-alive',
    'X-Requested-With':
    'XMLHttpRequest',
    'User-Agent':
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
    'Cookie':
    'BD_UPN=12314753; ORIGIN=2; ISSW=1; ISSW=1; BAIDUID=F0F664464891FF22022016FEED575109:FG=1; PSTM=1558524896; BIDUPSID=C9733DAACC84E56AF9FED0BDDAADA245; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BDUSS=lZaZ3I2RzZnN2QtN3doRjlOcnpKMDRYOUJvVDFxVFl-WmFZODVwYTlKLW5MQ0JkSVFBQUFBJCQAAAAAAAAAAAEAAABBGFGnsOvU2MH39fwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKef-Fynn~hcQ; bdindexid=2cka9urn2rk1o4dmnsueadarc7; H_PS_PSSID=1468_21103_29237_28519_29098_29368_28832_29220; BD_HOME=1; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; delPer=0; BD_CK_SAM=1; PSINO=2; H_PS_645EC=22aaZNHp8tp6Pqs1f3AIplUyT%2F67VGrp%2B2iogcH66TNgP6TYyCWal3%2BTHPaWCW6LDeS3'
}
total = []
name = f'popularity({start_date}-{end_date})'
logger.add(f'{name}.log')


def decrypt(key, data):
    m = list(key)
    v = data
    d = dict(zip(m[:len(m) // 2:], m[len(m) // 2::]))
    return ''.join(map(lambda x: d[x], v))


def crawl(word):
    try:
        url = f'{domain}/api/SearchApi/index'
        params = {
            'word': word,
            'startDate': arrow.get(start_date).naive,
            'endDate': arrow.get(end_date).naive,
            'area': 0
        }
        data = requests.get(url, params=params, headers=headers).json()
        uniqid = data['data']['uniqid']
        user_indexes = data['data']['userIndexes'][0]
        key = requests.get(f'{domain}/Interface/api/ptbk?uniqid={uniqid}', headers=headers).json()['data']
        encrypted_data = {kind: user_indexes[kind]['data'] for kind in kinds}
        decrypted_data = {kind: decrypt(key, d).split(',') for kind, d in encrypted_data.items()}
        date_range = pd.date_range(start_date, end_date).to_native_types()
        result = []
        for kind, indexes in decrypted_data.items():
            rows = [{
                'kind': kind,
                'date': date,
                'index': index,
                'keyword': word
            } for date, index in zip(date_range, indexes)]
            result.extend(rows)
            logger.info((rows[0], rows[-1]))
        total.extend(result)
        time.sleep(5)
    except Exception as e:
        logger.error(f'{word}抓取失败')


if __name__ == '__main__':
    [crawl(word) for word in words]
    lt.save(total, name=f'{name}.csv')
