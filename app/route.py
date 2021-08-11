from flask import render_template, redirect, url_for, request, send_from_directory, flash
from flask import send_from_directory
from app.models.index import *

def index():
    wiki = get_wiki_recentchange()
    return render_template('index.html', wiki = wiki)

def wiki():
    return render_template('wiki.html')

def gitlab():
    return render_template('gitlab.html')

def jira():
    return render_template('jira.html')

def hive():
    return render_template('hive.html')

def jupyter():
    return render_template('jupyter.html')

def project_bfx_1():
    return render_template('project_bfx_1.html')

def project_bfx_2():
    return render_template('project_bfx_2.html')

def create_jupyter():
    return render_template('create_jupyter.html')

def page_not_found(e):
    return render_template('404.html'), 404