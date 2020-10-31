import os

from flask import Flask, render_template, url_for


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
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

    # a simple page that says hello
    @app.route('/', methods = ['GET'])
    def index():
        return render_template('base.html')

    from . import db
    db.init_app(app)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='localhost', port=5000, debug=True)