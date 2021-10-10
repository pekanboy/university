from flask import Flask, render_template
from dbHandler.routes import dbHandler

app = Flask(__name__)
app.register_blueprint(dbHandler, url_prefix='/db')


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='localhost', port=8080)
