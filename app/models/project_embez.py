from .base import *
from flask import request, jsonify, render_template, redirect, url_for
import datetime
from sklearn.metrics import accuracy_score
import pandas as pd
import numpy as np
import math
import os



def evaluation_metrics_embez(df_Y,df_predict):
    '''
    RCALL-PERCENT Curve AUC (1000 切點)
    '''
    try:
        df_ass = pd.merge(df_Y,df_predict, on=['AGENT_ID_SAS','APC_ID_SAS','DATA_DATE'],how='left')
        p = 1/1000
        df_ass = df_ass.sort_values(by=['SCORE'],ascending=False)
        df_ass['target_cum'] = df_ass['Y'].cumsum()
        df_ass = df_ass.reset_index(drop=True)
        df_ass['num'] = pd.Series(range(1,len(df_ass)+1))
        df_ass['success_n']= len(df_ass[df_ass['Y']==1])
        df_ass['recall'] = df_ass['target_cum']/df_ass['success_n']
        assess = pd.DataFrame()
        recall_auc = 0
        for i in np.arange(p,1+p,p):
            recall_auc = recall_auc + df_ass.loc[math.floor(i*len(df_ass))-1].recall 
    except:
        recall_auc = 0
    return round(recall_auc/1000,4)

def embez_score(filename):
    y_pred = pd.read_csv("https://storage.googleapis.com/treebucket2021/files/embez/"+filename+".csv")
    y_ture = pd.read_csv("https://storage.googleapis.com/treebucket2021/files/embez/embez_answer.csv")
    result = evaluation_metrics_embez(y_ture,y_pred)
    return result


def project_embez_evaluation():
    gcp_path = os.path.join('files','embez')
    name = request.form['embez_name']
    des = request.form['embez_des']
    f_csv = request.files['embez_csv']
    f_nb = request.files['embez_nb']
    update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lastname = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    filename = str("embez_"+ lastname)

    # 上傳資料、計算分數
    if f_nb:
        try:
            csv_url = upload_gcp(str(filename+".csv"),f_csv,gcp_path)
            nb_url = ipynb2html(filename,f_nb,gcp_path)
            print("有nb")
            score = embez_score(filename)
            sqls = '''INSERT INTO project_embez(name, csv_file, nb_file, des, auc, etl_date, del_flg) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', 0);''' % (name, csv_url, nb_url, des, score, update_time)
        finally:
            print('done')
    else:
        try:
            csv_url = upload_gcp(str(filename+".csv"),f_csv,gcp_path)
            print("只有csv")
            score = embez_score(filename)
            sqls = '''INSERT INTO project_embez(name, csv_file, nb_file, des, auc, etl_date, del_flg) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', 0);''' % (name, csv_url, '', des, score, update_time)
        finally:
            print('done')
    # 寫入DB"
    try:
        write_db(pgdb_config,sqls)
    finally:
            print('done')
    # 回傳結果
    return redirect(url_for('project_embez_2'))
