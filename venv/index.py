from flask import Flask, render_template, jsonify, request, url_for, flash, redirect, request, session
import flask
#from flask_socketio import SocketIO
import time
from datetime import timedelta

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
timeout = 10
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=timeout)


#deletes session after timeout minutes
#as of right now, it will not timeout unless you refresh or close tab

activeUsers = []

@app.route('/')
def home():
	if not session.get("user"):
		print("here")
		return redirect("/login")
	if not session.get("user") in activeUsers: #if I restart flask
		print("here2")
		return redirect("/login")
	user = session.get('user', None)
	print(user)
	pusher_client.trigger('messaging', 'updateUsers', activeUsers) 
	#sometimes activeUsers don't display on startup
	flask.session.modified = True #should reset session timer
	return render_template('baseMerge.html', user=user)

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@app.route("/logout", methods=['GET', 'POST'])
def logout():
	removed = session.get('user')
	if (request.method=='POST'):
		print('entered')
		removed = request.form.get('user')
	print('logged out with: ')
	print(removed)
	if removed in activeUsers:
		activeUsers.remove(removed)
	pusher_client.trigger('messaging', 'updateUsers', activeUsers)
	session["user"] = None
	session.clear()
	#print('redirecting')
	return redirect(url_for("login"))
	#

	#return redirect("/")

@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	#print(request.form)
	if request.method == 'POST':
		if request.form['email'] in activeUsers:
			error = 'User already exists. Please try again.'
		elif request.form['pass'] != 'admin' and request.form['pass'] != 'onions': #request.form['email'] != 'admin@gmail' or 
			#temporary fix for duplicate usernames
			print('Incorrect')
			error = 'Invalid Credentials. Please try again.'
		else:
			print('Correct')
			session['user'] = request.form['email']
			activeUsers.append(session['user'])
			return redirect("/")
	return render_template('login.html', error=error)

# @app.route('/login', methods=['GET', 'POST'])
# def login():
# 	try:
# 		print(request.form)
# 		error = None
# 		if request.form['email'] != 'admin@gmail' or request.form['pass'] != 'admin':
# 			error = 'Invalid Credentials. Please try again.'
# 			print('here')
# 		else:
# 			print('Correct')
# 			return redirect(url_for('base'))
# 	except Exception as e:
# 		print(e)
# 		return jsonify({'result' : 'failure'})
# 	print('here2')
# 	return render_template('login.html', error=error)

@app.route('/message', methods=['GET', 'POST'])
def message():
	try:
		if not session.get("user"):
			print("here3")
			return jsonify({'result' : 'failure'})
		# if not session.get("user") in activeUsers: #if I restart flask
		# 	print("here4")
		# 	return redirect(url_for('home'))
		print(request.form)
		username = request.form.get('user')
		message = request.form.get('msg')
		print(username)
		print(message)
		
		flask.session.modified = True #should reset session timeout timer when message is sent
		pusher_client.trigger('messaging', 'my-event', {'user' : username, 'msg': message, 'activeUsers': activeUsers, 'sender': session.get('user')})
		#sending list of activeUsers to see if current user is still there
		return jsonify({'result' : 'success'})
    
	except Exception as e:
		print(e)
		return jsonify({'result' : 'success'})




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

