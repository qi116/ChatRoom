from flask import Flask, render_template, jsonify, request, url_for, flash, redirect, request
#from flask_socketio import SocketIO
import time

import json

import pusher


pusher_client = pusher.Pusher(
  app_id='1526772',
  key='ee9c18f3062cb4ecdf9d',
  secret='56bb69f38505ab003966',
  cluster='us3',
  ssl=True
)




app = Flask(__name__)

app.config['SECRET_KEY'] = 'f03a2ea0b16bfc14f0af5ed54553f84a0877604ca3e9fa25'
#socketio = SocketIO(app)


@app.route('/', methods = ['POST', 'GET'])
def home():
	#pusher_client.trigger('messaging', 'my-event', {'user': 'hello world', 'msg': 'hi there'})

	return render_template('base.html')

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@app.route('/message', methods=['GET', 'POST'])
def message():
	try:
		print(request.form)
		username = request.form.get('user')
		message = request.form.get('msg')
		print(username)
		print(message)
		

		pusher_client.trigger('messaging', 'my-event', {'user' : username, 'msg': message})

		return jsonify({'result' : 'success'})
    
	except Exception as e:
		print(e)
		return jsonify({'result' : 'failure'})
@app.route('/success/<name>')
def success(name):
   return 'welcome %s' % name


# @socketio.on('my event')
# def handle_my_custom_event(json, methods=['GET', 'POST']):
# 	print('received my event: ' + str(json))
# 	user = json.get("user_name")
    
	
# @socketio.on('message')
# def receive_message(json, methods=['GET', 'POST']):
# 	print('message: ' + str(json))
# 	socketio.emit('post message', json, callback=messageReceived)


if __name__ == '__main__':
   app.run(debug = True)

