from .base import *
import requests
import json
import psycopg2

def get_wiki_recentchange():
    url = "https://gitlab.com/chia313339/treestudio/-/raw/main/data.txt"
    result = requests.get(url)
    result.encoding = 'utf8'
    return json.loads(result.json())


def simple_message_board():
    conn = psycopg2.connect(**pgdb_config)
    try:
        with conn.cursor() as cursor:
            now = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            data = json.loads(request.form.get('data'))
            name = data['name']
            message = data['message']
            sql = '''INSERT INTO simple_message_board("name", "message", "datetime") VALUES (%s, %s, %s);'''
            cursor.execute(sql,(name,message,now))
        conn.commit()
        return jsonify({"success": 200, "msg": "提交成功", "date":now})
    finally:
        conn.close()

