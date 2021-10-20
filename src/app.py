from flask import Flask, render_template
from dbHandler.query_routes import dbHandler

app = Flask(__name__)
app.register_blueprint(dbHandler, url_prefix='/query')

isAuth = False


@app.route('/')
def index():
    return render_template('index.html', isAuth=isAuth)


@app.route('/exit')
def exit():
    return "Спасибо, до свидания!"


if __name__ == '__main__':
    app.run(host='localhost', port=8043)
