import pymongo
import looter as lt
from pprint import pprint
from concurrent import futures

domain = 'https://sou.zhaopin.com'
client = pymongo.MongoClient()
db = client.zhilian
col = db.python

def crawl(url):
    response = lt.send_request(url).json()
    if response['code'] == 200:
        results = response['data']['results']
        for result in results:
            col.insert_one(result)


if __name__ == '__main__':
    tasklist = [f'https://fe-api.zhaopin.com/c/i/sou?start={n * 100}&pageSize=100&cityId=489&workExperience=-1&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&kw=python&kt=3&lastUrlQuery=%7B%22p%22:3,%22jl%22:%22489%22,%22kw%22:%22python%22,%22kt%22:%223%22%7D' for n in range(61)]
    with futures.ThreadPoolExecutor(50) as executor:
        executor.map(crawl, tasklist)