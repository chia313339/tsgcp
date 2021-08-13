import requests
import json
import psycopg2

def get_broadcast(pgdb_config):
    conn = psycopg2.connect(**pgdb_config)
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM broadcast where del_flg <> '1' order by etl_date desc,no desc;''')
    result = cursor.fetchall()
    conn.commit()
    conn.close()
    return result
