import os
from datetime import timedelta
from flask import Flask, render_template, url_for, redirect, session, request, send_from_directory

from .client import Client

NAME_KEY = 'name'

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    app.secret_key = 'hiandrei'

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'tables.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError as e:
        print("[EXCEPTION OSERROR_mkdir_instancePath]", e)

    # Favicon
    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico', mimetype='image/vnd.microsoft.icon')
    
    # home page
    @app.route('/home')
    @app.route('/', methods = ['GET'])
    def home():
        if NAME_KEY not in session:
           return redirect(url_for('login'))

        return render_template('index.html', **{"login":True, "session":session})

    #background process for clicking
    @app.route('/run', methods=['GET'])
    def run(url=None):
        message = request.args.get('val')

        print(message)
        print("clicked")
        
        return ("nothing")

    # login
    @app.route('/login', methods = ['POST', 'GET'])
    def login():
        if request.method == "POST":
            print(request.form)
            session[NAME_KEY] = request.form["inputName"]
            return redirect(url_for("home"))
        return render_template('login.html', **{'session':session})

    # logout
    @app.route('/logout')
    def logout():
        session.pop(NAME_KEY, None)
        return redirect(url_for('login'))

    #from . import db
    #db.init_app(app)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='localhost', port=5000, debug=True)