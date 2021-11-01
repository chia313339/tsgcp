from flask import render_template, redirect, url_for, request, send_from_directory, flash, jsonify
from flask import send_from_directory
import pandas as pd
import datetime
import json
import psycopg2
import sqlalchemy
from datetime import date
from app.models.base import *
from app.models.index import *
from app.models.broadcast import *
from app.models.project_bfx import *
from app.models.project_embez import *
from app.models.food import *


def index():
    wiki = get_wiki_recentchange()
    broadcast_list_sql = '''SELECT * FROM broadcast where del_flg <> '1' order by etl_date desc,no desc;'''
    broadcast_list = get_data_from_pgdb(pgdb_config,broadcast_list_sql)[0:5]
    msg_board_sql = '''select no, name, message, datetime + interval '8 hour' as dt from simple_message_board where name <> '' and message <> '' order by simple_message_board.datetime desc limit 10'''
    msg_board = get_data_from_pgdb(pgdb_config,msg_board_sql)
    testimonials_list_sql = '''SELECT no, name, title, context, pic_url  FROM public.testimonials where del_flg <> 1 order by no desc'''
    testimonials_list = get_data_from_pgdb(pgdb_config,testimonials_list_sql)

    order_owner = ["客智科","工程組","商智科"][(abs(date.today() - date(2021,10,10)).days//7)%3]

    try:
        order_info = get_order_info()[0]
    except:
        order_info = None
    return render_template('index.html', wiki=wiki, msg_board=msg_board,broadcast_list=broadcast_list, testimonials_list=testimonials_list,order_info=order_info,order_owner=order_owner)

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

def food_order():
    order_info = get_order_info()
    order_list = []
    for idx, val in enumerate(order_info):
        tmp = get_order_list(val[0])
        order_list.append(tmp)
    return render_template('food_order.html',order_info = order_info,order_list=order_list)

def food_setting():
    store_info_list = show_store()
    return render_template('food_setting.html', store_info_list=store_info_list)

def project_bfx_1():
    return render_template('project_bfx_1.html')

def project_bfx_2():
    leaderboard_list_sql = '''SELECT * FROM project_bfx where del_flg <> '1' order by acc_part_overall desc,no desc;'''
    leaderboard_list = get_data_from_pgdb(pgdb_config,leaderboard_list_sql)
    return render_template('project_bfx_2.html',leaderboard_list=leaderboard_list)

def project_bfx_3():
    leaderboard_list_sql = '''SELECT * FROM project_bfx2 where del_flg <> '1' order by acc_part_overall desc,no desc;'''
    leaderboard_list = get_data_from_pgdb(pgdb_config,leaderboard_list_sql)
    return render_template('project_bfx_3.html',leaderboard_list=leaderboard_list)


def project_embez_1():
    return render_template('project_embez_1.html')

def project_embez_2():
    leaderboard_list_sql = '''SELECT * FROM project_embez where del_flg <> '1' order by auc desc,no desc;'''
    leaderboard_list = get_data_from_pgdb(pgdb_config,leaderboard_list_sql)
    return render_template('project_embez_2.html',leaderboard_list=leaderboard_list)

def create_jupyter():
    return render_template('create_jupyter.html')

def broadcast():
    broadcast_list_sql = '''SELECT * FROM broadcast where del_flg <> '1' order by etl_date desc,no desc;'''
    broadcast_list = get_data_from_pgdb(pgdb_config,broadcast_list_sql)
    return render_template('broadcast.html',broadcast_list = broadcast_list)

def gmp_poc():
    return render_template('gmp_poc.html')

def page_not_found(e):
    return render_template('404.html'), 404


def test():
    return render_template('test.html')







                

