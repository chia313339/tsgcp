import requests
import json

def get_wiki_recentchange():
    url = "https://gitlab.com/chia313339/treestudio/-/raw/main/data.txt"
    result = requests.get(url)
    result.encoding = 'utf8'
    return json.loads(result.json())