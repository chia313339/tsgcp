from flask import render_template, redirect, url_for, request, send_from_directory, flash
from flask import send_from_directory

def index():
    return render_template('index.html')

def project_bfx_1():
    return render_template('project_bfx_1.html')

def page_not_found(e):
    return render_template('404.html'), 404