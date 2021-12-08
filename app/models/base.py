import requests
import json
import psycopg2
import os
import datetime
import pandas as pd
import sqlalchemy
from flask import send_from_directory
from flask import render_template, redirect, url_for, request, flash, jsonify
from psycopg2.extras import RealDictCursor
from google.cloud import storage

# pgdb_config={
# 'host':'34.135.113.78',
# 'port':5432,
# 'user':'treestudio',
# 'password':'treestudio',
# 'database':'treestudio',
# }

# 正式環境DB
pgdb_config={
'host':'34.80.244.193',
'port':5432,
'user':'treestudio',
'password':'treestudio',
'database':'treestudio',
}


CLOUD_STORAGE_BUCKET = 'treebucket202112'


# ipynb轉html並上傳upload_gcp
def ipynb2html(ipynb_name,uploaded_file,gcp_path,file_path=None):
    tmp_path = os.path.join(os.getcwd(),'app','static','page','tmp')
    if file_path:
        tmp_path = file_path
    uploaded_file.save(os.path.join(tmp_path,ipynb_name+".ipynb"))
    os.system("cd "+tmp_path+"; "+"jupyter nbconvert "+ipynb_name+".ipynb --to html;")

    gcs = storage.Client()
    bucket = gcs.get_bucket(CLOUD_STORAGE_BUCKET)
    blob = bucket.blob(gcp_path+'/'+ipynb_name+'.html')
    blob.upload_from_filename(os.path.join(tmp_path,ipynb_name+'.html'))
    return blob.public_url



# 上傳gcp cloud
def upload_gcp(filename,uploaded_file,gcp_path):
    tmp_path = os.path.join(os.getcwd(),'app','static','page','tmp')
    uploaded_file.save(os.path.join(tmp_path,filename))
    # Create a Cloud Storage client.
    gcs = storage.Client()
    # Get the bucket that the file will be uploaded to.
    bucket = gcs.get_bucket(CLOUD_STORAGE_BUCKET)
    # Create a new blob and upload the file's content.
    blob = bucket.blob(gcp_path+'/'+filename)
    blob.upload_from_filename(os.path.join(tmp_path,filename))
    # The public URL can be used to directly access the uploaded file via HTTP.
    return blob.public_url




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

