from flask import Flask, render_template
from constants import *

app = Flask(__name__)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/shipments')
def shipments():
    return render_template('shipments.html')


@app.route('/shipments/create')
def shipments_create():
    return render_template('shipments/create.html')


@app.route('/manage')
def manage():
    return render_template('manage.html')


@app.route('/manage/create')
def manage_create():
    return render_template('manage/create.html')


@app.route('/manage/edit')
def manage_edit():
    return render_template('manage/edit.html')


@app.route('/manage/delete')
def manage_delete():
    return render_template('manage/delete.html')


if __name__ == '__main__':
    app.run()
