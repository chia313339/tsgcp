from flask import Flask
from app.route import *

def create_app():
    app = Flask(__name__)
    app.config['JSON_AS_ASCII'] = False
    app.config['SECRET_KEY'] = 'thisisabookandimsupersmart123456'
    app.add_url_rule('/', 'index', index, methods=['GET', 'POST'])
    app.add_url_rule('/index', 'index', index, methods=['GET', 'POST'])
    app.add_url_rule('/wiki', 'wiki', wiki, methods=['GET', 'POST'])
    app.add_url_rule('/gitlab', 'gitlab', gitlab, methods=['GET', 'POST'])
    app.add_url_rule('/jira', 'jira', jira, methods=['GET', 'POST'])
    app.add_url_rule('/gather', 'gather', gather, methods=['GET', 'POST'])
    app.add_url_rule('/jupyter', 'jupyter', jupyter, methods=['GET', 'POST'])
    app.add_url_rule('/broadcast', 'broadcast', broadcast, methods=['GET', 'POST'])
    app.add_url_rule('/create_jupyter', 'create_jupyter', create_jupyter, methods=['GET', 'POST'])
    app.add_url_rule('/hive', 'hive', hive, methods=['GET', 'POST'])
    app.add_url_rule('/food_order', 'food_order', food_order, methods=['GET', 'POST'])
    app.add_url_rule('/food_setting', 'food_setting', food_setting, methods=['GET', 'POST'])
    app.add_url_rule('/project_bfx_1', 'project_bfx_1', project_bfx_1, methods=['GET', 'POST'])
    app.add_url_rule('/project_bfx_2', 'project_bfx_2', project_bfx_2, methods=['GET', 'POST'])
    app.add_url_rule('/gmp_poc', 'gmp_poc', gmp_poc, methods=['GET', 'POST'])
    app.register_error_handler(404, page_not_found)
    app.add_url_rule('/test', 'test', test, methods=['GET'])
    app.add_url_rule('/simple_message_board', 'simple_message_board', simple_message_board, methods=['POST'])
    app.add_url_rule('/broadcast_exec', 'broadcast_exec', broadcast_exec, methods=['POST'])
    app.add_url_rule('/get_file/<dirname>/<filename>', 'get_file', get_file, methods=['GET','POST'])
    app.add_url_rule('/project_bfx_evaluation', 'project_bfx_evaluation', project_bfx_evaluation, methods=['POST'])
    app.add_url_rule('/add_store_menu', 'add_store_menu', add_store_menu, methods=['POST'])
    app.add_url_rule('/edit_store_menu', 'edit_store_menu', edit_store_menu, methods=['POST'])
    app.add_url_rule('/del_store_menu', 'del_store_menu', del_store_menu, methods=['POST'])
    app.add_url_rule('/add_order_setting', 'add_order_setting', add_order_setting, methods=['POST'])
    app.add_url_rule('/add_order_list', 'add_order_list', add_order_list, methods=['POST'])
    app.add_url_rule('/del_order_info', 'del_order_info', del_order_info, methods=['POST'])
    app.add_url_rule('/del_order_item', 'del_order_item', del_order_item, methods=['POST'])
    app.add_url_rule('/quick_summary', 'quick_summary', quick_summary, methods=['POST'])
    app.add_url_rule('/paid_money', 'paid_money', paid_money, methods=['POST'])
    app.add_url_rule('/get_order_list/<order_no>', 'get_order_list', get_order_list, methods=['GET'])
    return app
