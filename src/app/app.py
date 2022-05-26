from flask import Flask, render_template, request, url_for, redirect, jsonify
import requests
import os
import random
from flask_socketio import SocketIO

app = Flask(__name__)
app.config.from_pyfile('config.py')
data = {'access_token': '',
        'token_type': '',
        'expires_in': '',
        'codes': []
        }

socketio = SocketIO(app)

@app.route("/", methods=['GET', 'POST'])
def home():
    print("home")
    return render_template('home.html')

@app.route("/host/<room_id>", methods=['GET', 'POST'])
def host(room_id):
    return render_template('host.html', room_id=room_id)

@app.route("/party/<room_id>", methods=['GET', 'POST'])
def guest(room_id):
    return render_template('guest.html', room_id=room_id)

@app.route("/api/callback", methods=['GET', 'POST'])
def callback():
    print("callback args")
    access_token = request.args.get("access_token")
    token_type = request.args.get("token_type")
    expires_in = request.args.get("expires_in")
    print(access_token)
    print(token_type)
    print(expires_in)
    url = 'https://accounts.spotify.com/api/token'
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
    response = ""

    request_body = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
    }
    try:
        response = requests.post(
            url =url,
            data=request_body
        )
    except Exception as e:
        print("Error getting Oauth Token")
        print(e)

    print(response)
    print(response.text)

    json_response = response.json()

    data['access_token'] = json_response['access_token']
    data['token_type'] = json_response['token_type']
    data['expires_in'] = json_response['expires_in']

    # return a redirect to the host page with the room_id set to the uuid
    return redirect(url_for('host', room_id=generate_party_code()))

@app.route('/api/joinroom')
def join_rooom():
    roomcode = request.args.get("roomcode")
    print('attempted to join room')
    print(roomcode)
    if len(roomcode) == 4:
        print("success")
        return jsonify(status=200)
    print("failure")
    return jsonify(status=400)

@socketio.on('createRoom')
def create_room(room_code):
    pass

@socketio.on('joinRoom')
def create_room(room_code):
    pass

@socketio.on('addSong')
def create_room(room_code):
    pass

def generate_party_code():
    id = ''
    for i in range(4):
        id += random.choice(app.config['ALPHANUMERIC'])
    print(id)
    return id