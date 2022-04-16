from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/shipments')
def shipments():
    return render_template('shipments.html')


@app.route('/manage')
def manage():
    return render_template('manage.html')


if __name__ == '__main__':
    app.run()
