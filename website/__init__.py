import os
from datetime import timedelta
from flask import Flask, render_template, url_for, redirect, session, request, send_from_directory, jsonify
from threading import Thread
import time

from .client import Client

NAME_KEY = 'name'
client = None
messages = []

# create and configure the app
app = Flask(__name__, instance_relative_config=True)

app.secret_key = 'hiandrei'

def disconnect():
    '''To disconnect the client from the server
    :return: None'''
    
    global client
    if client:
        client.disconnect()


# Favicon
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

# home page
@app.route('/home')
@app.route('/', methods=['GET'])
def home():
    global client

    if NAME_KEY not in session:
        return redirect(url_for('login'))

    client = Client(session[NAME_KEY])
    return render_template('index.html', **{"login": True, "session": session})

# background process for clicking
@app.route('/run_messageSender', methods=['GET'])
def run_messageSender(url=None):
    global client

    message = request.args.get('val')

    if client != None:
        client.send_message(message)

    return 'none'

# login
@app.route('/login', methods=['POST', 'GET'])
def login():
    '''Main login page to login with name
    :return: html template'''
    global client
    client.disconnect()

    if request.method == "POST":
        print(request.form)
        session[NAME_KEY] = request.form["inputName"]
        return redirect(url_for("home"))

    return render_template('login.html', **{'session': session})

# logout
@app.route('/logout')
def logout():
    session.pop(NAME_KEY, None)

    return redirect(url_for('login'))


@app.route('/get_messages')
def get_messages():
    return jsonify({"messages":messages})

def update_messages():
    '''Gets and updates messages for the whole server'''

    global messages

    while True:

        time.sleep(0.1)
        if not client: continue
        new_messages = client.get_messages()
        messages.extend(new_messages)

        for message in new_messages:
            if message == "exit":
                break


if __name__ == '__main__':
    Thread(target=update_messages).start()
    app.run(debug=True, adress='localhost', port='5000')
