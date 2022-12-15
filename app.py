from flask import Flask, render_template, jsonify, request, url_for, flash, redirect, request
from flask_socketio import SocketIO
import time

import json
#from threading import Timer
from threading import Thread

#import threading


app = Flask(__name__)

app.config['SECRET_KEY'] = 'f03a2ea0b16bfc14f0af5ed54553f84a0877604ca3e9fa25'
socketio = SocketIO(app)


@app.route('/')
def home():
    return render_template('base.html')

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')



@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
	print('received my event: ' + str(json))
	user = json.get("user_name")
    
	if (key_to_name.__contains__(user)) :
		
		json["user_name"] = key_to_name.get(user)
		socketio.emit('my response', json, callback=messageReceived)
		
		
	else:
		
		json["user_name"] = "Private message: " + json["user_name"]
		socketio.emit('my response', json, callback=messageReceived, room=clients[0])   

if __name__ == '__main__':
    socketio.run(app, debug=True, port = 5000, host = "0.0.0.0")

