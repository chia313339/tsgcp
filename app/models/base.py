import requests
import json
import psycopg2
import os
import datetime
import pandas as pd
import sqlalchemy
from flask import send_from_directory
from flask import render_template, redirect, url_for, request, flash, jsonify

pgdb_config={
'host':'34.135.113.78',
'port':5432,
'user':'treestudio',
'password':'treestudio',
'database':'treestudio',
}

# 判断文件是否合法
def allowed_file(filename,allow_rule):
    # allow_rule must be a set, like set(['txt', 'png', 'jpg', 'xls', 'JPG', 'PNG', 'xlsx', 'gif', 'GIF'])
    return '.' in filename and filename.rsplit('.', 1)[1] in allow_rule


# 讀pgdb資料 
def get_data_from_pgdb(pgdb_config,sqls):
    conn = psycopg2.connect(**pgdb_config)
    cursor = conn.cursor()
    cursor.execute(sqls)
    result = cursor.fetchall()
    conn.commit()
    conn.close()
    return result

# 執行pgdb的SQL
def write_db(pgdb_config,sqls):
    conn = psycopg2.connect(**pgdb_config)
    cursor = conn.cursor()
    cursor.execute(sqls)
    conn.commit()
    conn.close()

# 抓取 static 裡的資料
def get_file(dirname,filename):
    path = os.path.join(os.getcwd(),'app','static','page',dirname,'file')
    return send_from_directory(path,filename,as_attachment=True)

