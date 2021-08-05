from flask import Flask
from app.route import *

def create_app():
    app = Flask(__name__)
    app.add_url_rule('/', 'index', index, methods=['GET', 'POST'])
    app.add_url_rule('/index', 'index', index, methods=['GET', 'POST'])
    app.add_url_rule('/project_bfx_1', 'project_bfx_1', project_bfx_1, methods=['GET', 'POST'])
    app.register_error_handler(404, page_not_found)

    return app
