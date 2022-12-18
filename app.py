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
    
	
@socketio.on('message')
def receive_message(json, methods=['GET', 'POST']):
	print('message: ' + str(json))
	socketio.emit('post message', json, callback=messageReceived)


#if __name__ == '__main__':
 #   socketio.run(app, debug=True, port = 5000, host = "0.0.0.0")

