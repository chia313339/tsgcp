import requests
import json
import psycopg2

def get_wiki_recentchange():
    url = "https://gitlab.com/chia313339/treestudio/-/raw/main/data.txt"
    result = requests.get(url)
    result.encoding = 'utf8'
    return json.loads(result.json())


def get_message_board(pgdb_config):
    conn = psycopg2.connect(**pgdb_config)
    cursor = conn.cursor()
    cursor.execute('''select * from simple_message_board where name <> '' and message <> '' order by no desc limit 10''')
    result = cursor.fetchall()
    conn.commit()
    conn.close()
    return result

