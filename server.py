from flask import Flask, request
from datetime import datetime


DATETIME_FORMAT = '%d-%m-%Y %H:%M:%S'

app = Flask(__name__)
messages = []
users = {}


@app.route('/')
def index():
    return '<h1>Hello world</h1>'


@app.route('/status')
def index_view():
    return {
        'status': True,
        'time': datetime.now().strftime(DATETIME_FORMAT),
        'messages_len': len(messages),
        'users_len': len(users),
    }


@app.route('/messages')
def messages_view():
    after = float(request.args['after'])
    new_messages = [mes for mes in messages if mes['time'] > after]
    return {'messages': new_messages}


@app.route('/auth', methods=['POST'])
def auth_view():
    user = request.json['user']
    password = request.json['password']

    if user in users and users[user] != password:
        return {'ok': False}

    users[user] = password

    return {'ok': True}


@app.route('/send', methods=['POST'])
def send_view():
    user = request.json['user']
    password = request.json['password']
    granted = user in users and users.get(user) == password
    if granted is False:
        return {'ok': False}

    text = request.json['text']
    messages.append({'user': user, 'text': text, 'time': datetime.now().timestamp()})

    return {'ok': True}


app.run()
