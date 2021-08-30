from .base import *
from flask import request, jsonify, render_template, redirect, url_for
import datetime
from sklearn.metrics import accuracy_score
import pandas as pd
import os



def ipynb2html(path,filename):
    os.system("cd "+path+"; "+"jupyter nbconvert "+filename+".ipynb --to html;")
    os.system("cd "+path+"; "+"jupyter nbconvert "+filename+".ipynb --to html;")

def evaluation_metrics(y_true, y_pred):
    result = accuracy_score(y_true, y_pred)
    return result

def bfx_score(path,filename):
    y_pred = pd.read_csv(os.path.join(path, filename+'.csv'))
    y_ture = pd.read_csv(os.path.join(path, 'bfx_answer.csv'))
    result = evaluation_metrics(y_ture['Y_PRED'],y_pred['Y_PRED'])
    return result

def project_bfx_evaluation():
    path = os.path.join(os.getcwd(),'app','static','page','project_bfx','file')
    name = request.form['bfx_name']
    des = request.form['bfx_des']
    f_csv = request.files['bfx_csv']
    f_nb = request.files['bfx_nb']
    update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lastname = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    filename = str(name +"_"+ lastname)
    # 上傳資料、計算分數
    if f_nb:
        try:
            f_csv.save(os.path.join(path, filename+'.csv'))
            f_nb.save(os.path.join(path, filename+'.ipynb'))
            print("有nb")
            ipynb2html(path,filename)
            score = bfx_score(path,filename)
            sqls = '''INSERT INTO project_bfx(name, csv_file, nb_file, des, score, etl_date, del_flg) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', 0);''' % (name, filename+'.csv', filename+'.ipynb', des, score, update_time)
        finally:
            print('done')
    else:
        try:
            f_csv.save(os.path.join(path, filename+'.csv'))
            print("只有csv")
            score = bfx_score(path,filename)
            sqls = '''INSERT INTO project_bfx(name, csv_file, nb_file, des, score, etl_date, del_flg) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', 0);''' % (name, filename+'.csv', '', des, score, update_time)
        finally:
            print('done')
    # 寫入DB"
    try:
        write_db(pgdb_config,sqls)
    finally:
            print('done')
    # 回傳結果
    return redirect(url_for('project_bfx_2'))