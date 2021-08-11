from flask import Flask
from app.route import *

def create_app():
    app = Flask(__name__)
    app.add_url_rule('/', 'index', index, methods=['GET', 'POST'])
    app.add_url_rule('/index', 'index', index, methods=['GET', 'POST'])
    app.add_url_rule('/wiki', 'wiki', wiki, methods=['GET', 'POST'])
    app.add_url_rule('/gitlab', 'gitlab', gitlab, methods=['GET', 'POST'])
    app.add_url_rule('/jira', 'jira', jira, methods=['GET', 'POST'])
    app.add_url_rule('/gather', 'gather', gather, methods=['GET', 'POST'])
    app.add_url_rule('/jupyter', 'jupyter', jupyter, methods=['GET', 'POST'])
    app.add_url_rule('/create_jupyter', 'create_jupyter', create_jupyter, methods=['GET', 'POST'])
    app.add_url_rule('/hive', 'hive', hive, methods=['GET', 'POST'])
    app.add_url_rule('/project_bfx_1', 'project_bfx_1', project_bfx_1, methods=['GET', 'POST'])
    app.add_url_rule('/project_bfx_2', 'project_bfx_2', project_bfx_2, methods=['GET', 'POST'])
    app.register_error_handler(404, page_not_found)

    return app
