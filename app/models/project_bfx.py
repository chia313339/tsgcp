from .base import *
from flask import request, jsonify, render_template, redirect, url_for
import datetime
from sklearn.metrics import accuracy_score
import pandas as pd


pgdb_config={
'host':'34.135.113.78',
'port':5432,
'user':'treestudio',
'password':'treestudio',
'database':'treestudio',
}

def evaluation_metrics(y_true, y_pred):
    result = accuracy_score(y_true, y_pred)
    return result

def bfx_score(path,filename):
    y_pred = pd.read_csv(os.path.join(path, filename+'.csv'))
    y_ture = pd.read_csv(os.path.join(path, 'bfx_answer.csv'))
    result = evaluation_metrics(y_ture['Y_PRED'],y_pred['Y_PRED'])
    return result

def write_db(pgdb_config,sqls):
    conn = psycopg2.connect(**pgdb_config)
    cursor = conn.cursor()
    cursor.execute(sqls)
    conn.commit()
    conn.close()


def project_bfx_evaluation():
    path = os.path.join(os.getcwd(),'app','static','page','project_bfx','file')
    name = request.form['bfx_name']
    des = request.form['bfx_des']
    f_csv = request.files['bfx_csv']
    f_nb = request.files['bfx_nb']
    update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = str(name +"_"+ update_time)
    # 上傳資料、計算分數
    if f_nb:
        f_csv.save(os.path.join(path, filename+'.csv'))
        f_nb.save(os.path.join(path, filename+'.ipynb'))
        print("有nb")
        score = bfx_score(path,filename)
        sqls = '''INSERT INTO project_bfx(name, csv_file, nb_file, des, score, etl_date, del_flg) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', 0);''' % (name, filename+'.csv', filename+'.ipynb', des, score, update_time)
    else:
        f_csv.save(os.path.join(path, filename+'.csv'))
        print("只有csv")
        score = bfx_score(path,filename)
        sqls = '''INSERT INTO project_bfx(name, csv_file, nb_file, des, score, etl_date, del_flg) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', 0);''' % (name, filename+'.csv', '', des, score, update_time)
    # 寫入DB"
    write_db(pgdb_config,sqls)
    # 回傳結果
    return redirect(url_for('project_bfx_2'))