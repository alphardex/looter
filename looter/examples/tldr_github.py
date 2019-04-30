import time
from pathlib import Path
from pprint import pprint
import requests
from looter import save

url = 'https://api.github.com/search/repositories?q={q}&order=desc'
headers = {'Authorization': 'token 5cc53c27e2f1e76af222c058651bda84c11ebda8'}
total = []

def crawl(task: str):
    try:
        json = requests.get(url.format(q=task), headers=headers).json()
        pprint(json)
        if json.get('message'):
            time.sleep(10)
        item = json.get('items', [None])[0]
        data = {}
        data['task'] = task
        if item:
            data['repo_name'] = item.get('full_name')
            data['repo_url'] = f"https://github.com/{item.get('full_name')}"
            data['stars'] = item.get('stargazers_count')
            data['forks'] = item.get('forks_count')
            data['watchers'] = item.get('watchers_count')
            pprint(data)
            total.append(data)
    except Exception as e:
        print(f'[Err] {e}')


if __name__ == "__main__":
    tasklist = Path(r'tldr_github.txt').read_text().split(', ')
    [crawl(task) for task in tasklist]
    save(total, name='tldr_github.csv', sort_by='stars', no_duplicate=True, order='desc')
