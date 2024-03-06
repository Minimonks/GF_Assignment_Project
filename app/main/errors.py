from flask import render_template
from .routes import main

#Tied to blueprint - custom 404 error.
@main.app_errorhandler(404)
def page_not_found(e):
    return render_template(".404.html"), 404
@main.app_errorhandler(429)
def too_many_requests(e):
    return render_template(".429.html"), 429
# @main.route('/test/', methods=['GET'])
# def index():
#     return render_template('index.html')