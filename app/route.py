from flask import render_template, redirect, url_for, request, send_from_directory, flash, jsonify
from flask import send_from_directory
import pandas as pd
import datetime
import json
import psycopg2
import sqlalchemy
from app.models.base import *
from app.models.index import *
from app.models.broadcast import *
from app.models.project_bfx import *

pgdb_config={
'host':'34.135.113.78',
'port':5432,
'user':'treestudio',
'password':'treestudio',
'database':'treestudio',
}

def index():
    wiki = get_wiki_recentchange()
    broadcast_list_sql = '''SELECT * FROM broadcast where del_flg <> '1' order by etl_date desc,no desc;'''
    broadcast_list = get_data_from_pgdb(pgdb_config,broadcast_list_sql)[0:5]
    msg_board_sql = '''select * from simple_message_board where name <> '' and message <> '' order by no desc limit 10'''
    msg_board = get_data_from_pgdb(pgdb_config,msg_board_sql)
    testimonials_list_sql = '''SELECT no, name, title, context, pic_url  FROM public.testimonials where del_flg <> 1 order by no desc'''
    testimonials_list = get_data_from_pgdb(pgdb_config,testimonials_list_sql)
    return render_template('index.html', wiki=wiki, msg_board=msg_board,broadcast_list=broadcast_list, testimonials_list=testimonials_list)

def wiki():
    return render_template('wiki.html')

def gitlab():
    return render_template('gitlab.html')

def jira():
    return render_template('jira.html')

def gather():
    return render_template('gather.html')

def hive():
    return render_template('hive.html')

def jupyter():
    return render_template('jupyter.html')

def project_bfx_1():
    return render_template('project_bfx_1.html')

def project_bfx_2():
    leaderboard_list_sql = '''SELECT * FROM project_bfx where del_flg <> '1' order by score desc,no desc;'''
    leaderboard_list = get_data_from_pgdb(pgdb_config,leaderboard_list_sql)
    return render_template('project_bfx_2.html',leaderboard_list=leaderboard_list)

def create_jupyter():
    return render_template('create_jupyter.html')

def broadcast():
    broadcast_list_sql = '''SELECT * FROM broadcast where del_flg <> '1' order by etl_date desc,no desc;'''
    broadcast_list = get_data_from_pgdb(pgdb_config,broadcast_list_sql)
    return render_template('broadcast.html',broadcast_list = broadcast_list)

def page_not_found(e):
    return render_template('404.html'), 404


def test():
    return render_template('test.html')




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


def broadcast_exec():
    conn = psycopg2.connect(**pgdb_config)
    data = json.loads(request.form.get('data'))
    if data['action'] ==1:
        try:
            with conn.cursor() as cursor:
                etl_date = data['date']
                context = data['context']
                url = data['url']
                sql = '''INSERT INTO broadcast("title", "context", "url", "etl_date", del_flg) VALUES ('', %s, %s, %s, 0);'''
                cursor.execute(sql,(context,url,etl_date))
            conn.commit()
            return jsonify({"success": 200, "msg": "提交成功"})
        finally:
            conn.close()
    elif data['action']==2:
        try:
            with conn.cursor() as cursor:
                no = str(data['broadcast_id'])
                sql = '''UPDATE broadcast SET del_flg = 1 where no = %s;''' % no
                cursor.execute(sql)
            conn.commit()
            return jsonify({"success": 200, "msg": "提交成功"})
        finally:
            conn.close()
    elif data['action']==3:
        print(data)
        try:
            with conn.cursor() as cursor:
                no = str(data['broadcast_id'])
                etl_date = data['date']
                context = data['context']
                url = data['url']
                sql = '''UPDATE broadcast SET ("context", "url", "etl_date") = (%s, %s, %s) where no = %s;'''
                cursor.execute(sql,(context,url,etl_date,no))
            conn.commit()
            return jsonify({"success": 200, "msg": "提交成功"})
        finally:
            conn.close()


                

