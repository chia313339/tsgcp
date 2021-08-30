from .base import *
from flask import request, jsonify, render_template, redirect, url_for
import json
import psycopg2
import pandas as pd
import os


# def add_order_list(item):
#     data = json.loads(request.form.get('data'))
#     order_no = data['order_no']
#     store_no = data['store_no']
#     order_name = data['order_name']
#     item_name = data['item_name']
#     item_price = data['item_price']
#     item_num = ['item_num']
#     item_remark = data['item_remark']
    


# def get_order_list(order_no):
#     sqls = ''''''


def get_order_info():
    sqls = '''SELECT order_no, order_store_no, order_owner, order_deadline, order_remark, A.update_time, store_name, store_class, store_add, store_tel, pic_file, store_remark, store_menu, star, order_times
	FROM public.food_order_setting A left join public.food_store_menu B on order_store_no = store_no
	WHERE A.del_flg <>1 and order_deadline > current_date'''
    order_info = get_data_from_pgdb(pgdb_config,sqls)
    print(order_info)
    return order_info

# 新增訂單
def add_order_setting():
    # 抓表單內容
    data = json.loads(request.form.get('data'))
    order_no = data['order_no']
    order_store_no = data['order_store_no']
    order_owner = data['order_owner']
    order_deadline = data['order_deadline']
    order_deadline = datetime.datetime.strptime(order_deadline, '%Y-%m-%d %H:%M:%S')
    order_remark = data['order_remark']
    update_time = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    print(data)
    sqls = '''INSERT INTO public.food_order_setting(order_no, order_store_no, order_owner, order_deadline, order_remark, update_time, del_flg) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s');''' % (order_no, order_store_no, order_owner, order_deadline, order_remark, update_time, 0)
    try:
        write_db(pgdb_config,sqls)
        print('成功更新')
    except Exception as e:
        print('更新失敗')
        print(e)

    return redirect(url_for('food_setting'))


# 新增店家
def add_store_menu():
    path = os.path.join(os.getcwd(),'app','static','page','food','img')
    # 抓表單內容
    store_no = request.form['store_no']
    store_name = request.form['store_name']
    store_class = request.form['store_class']
    store_tel = request.form['store_tel']
    store_add = request.form['store_add']
    store_remark = request.form['store_remark']
    pic1_file = request.files['pic1_file']
    store_menu = request.form['store_menu']
    update_time = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    pic1_file_name = 'nopic'

    # 看有無圖片
    if pic1_file:
        pic1_file_name = str(store_no)
        pic1_file.save(os.path.join(path, pic1_file_name+'.jpg'))
    
    # 不用解析菜單，直接存text
    # 寫入DB
    sqls = '''INSERT INTO food_store_menu(store_no, store_name, store_class, store_add, store_tel, pic_file, store_remark, store_menu, star, order_times, update_time, del_flg) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');''' % (store_no, store_name, store_class, store_add, store_tel, pic1_file_name, store_remark, store_menu, 0, 0, update_time, '0')
    try:
        write_db(pgdb_config,sqls)
        print('成功更新')
    except Exception as e:
        print('更新失敗')
        print(e)

    return redirect(url_for('food_setting'))

# 修改店家
def edit_store_menu():
    path = os.path.join(os.getcwd(),'app','static','page','food','img')
    # 抓表單內容
    store_no = request.form['new_store_no']
    store_name = request.form['new_name']
    store_tel = request.form['new_tel']
    store_add = request.form['new_add']
    store_remark = request.form['new_remark']
    pic1_file = request.files['new_pic']
    store_menu = request.form['new_menu']
    update_time = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    pic1_file_name = str(store_no)

    # # 看有無圖片
    if pic1_file:
        pic1_file.save(os.path.join(path, pic1_file_name+'.jpg'))
    
    # # 不用解析菜單，直接存text
    # # 寫入DB
    sqls = '''UPDATE public.food_store_menu SET store_add='%s', store_tel='%s', pic_file='%s', store_remark='%s', store_menu='%s', update_time='%s' WHERE store_no='%s';''' % (store_add, store_tel, pic1_file_name, store_remark, store_menu, update_time, store_no)
    try:
        write_db(pgdb_config,sqls)
        print('成功更新')
    except Exception as e:
        print('更新失敗')
        print(e)

    return redirect(url_for('food_setting'))


# 刪除店家
def del_store_menu():
    store_no = request.form['new_store_no']
    sqls = '''UPDATE public.food_store_menu SET del_flg='%s' WHERE store_no='%s';''' % (1, store_no)
    try:
        write_db(pgdb_config,sqls)
        print('成功更新')
    except Exception as e:
        print('更新失敗')
        print(e)

    return redirect(url_for('food_setting'))


# 顯示店家
def show_store():
    sqls = '''SELECT store_no, store_name, store_class, store_add, store_tel, pic_file, store_remark, store_menu, star, order_times, update_time FROM public.food_store_menu where del_flg <> 1 order by update_time desc'''
    store_info = get_data_from_pgdb(pgdb_config,sqls)
    return store_info