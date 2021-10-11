from flask import Flask, render_template, url_for
from dbHandler.routes import dbHandler, config

app = Flask(__name__)
app.register_blueprint(dbHandler, url_prefix='/db')

app.config['QUERYS'] = config


@app.route('/')
def index():
    return render_template('dateUser.html', querys=app.config['QUERYS'])


if __name__ == '__main__':
    app.run(host='localhost', port=8080)
