import requests
import json
import psycopg2
import os
from flask import send_from_directory

# 判断文件是否合法
def allowed_file(filename,allow_rule):
    # allow_rule must be a set, like set(['txt', 'png', 'jpg', 'xls', 'JPG', 'PNG', 'xlsx', 'gif', 'GIF'])
    return '.' in filename and filename.rsplit('.', 1)[1] in allow_rule


# 讀寫資料進 pgdb
def get_data_from_pgdb(pgdb_config,sqls):
    conn = psycopg2.connect(**pgdb_config)
    cursor = conn.cursor()
    cursor.execute(sqls)
    result = cursor.fetchall()
    conn.commit()
    conn.close()
    return result

# 抓取 static 裡的資料
def get_file(dirname,filename):
    path = os.path.join(os.getcwd(),'app','static','page',dirname,'file')
    return send_from_directory(path,filename,as_attachment=True)

