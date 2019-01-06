import os
import eventlet
import datetime
import requests

from flask import Flask, render_template, request, current_app
from flask_socketio import SocketIO, join_room, leave_room
import hashlib
from db_repo import *



application = Flask(__name__)
application.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(application)
mydb=database_flaskr()

op_code_map={'1':'AL','3':'BS','28':'AT','8':'IDX','10':'MS','12':'RL','13':'RG','17':'TD','19':'UN','5':'VD','22':'VF'}
fail_map={'29':'JO','20':'MTD','6':'MTM'}

#****************************************************************************
#test definitions
@application.route('/hello', methods=['GET'])
def hello():
	if request.method == 'GET':
		return 'Hello World!!!'
		
@application.route('/yellow', methods=['GET'])
def yellow():
	if request.method == 'GET':
		return mydb.yellowtest()
#****************************************************************************

		
#****************************************************************************
#exotel definition for ICTD
@application.route('/exotel/', methods=['GET'])
def exotel():
	if request.method == 'GET':
		que=request.query_string.split('&')
		if que[-1]=='digits=%222%22':
			number=que[1][-10:]
			print number
			
			op_code="AT"#WARNING REMOVE THIS
			op_info=requests.get("https://joloapi.com/api/findoperator.php?userid=devansh76&key=326208132556249&mob=%s&type=text" %(str(number)))
			if op_info.text.split(",")[0] in op_code_map:
				op_code=str(op_code_map[op_info.text.split(",")[0]])
				print op_code
				cir_code=str(op_info.text.split(",")[1])
			elif op_info.text.split(",")[0] in fail_map:
				print "non-rechargeable"
			amount=10
			z='{:%Y%m%d%H%M%S}'.format(datetime.datetime.now())
			rech=requests.get("https://joloapi.com/api/recharge.php?mode=1&userid=devansh76&key=326208132556249&operator=%s&service=%s&amount=%s&orderid=%s&type=text" % (op_code,str(number),amount,z))
			print rech.text
			if rech.text.split(',')[0]=='FAILED':
				op_list=['TW','T24S','T24','VC','VGS','VG','VDS','VD','TI','TDS','TD','AL','MS','UNS','UN','RG','RL','VF','IDX','BSS','BS','AT']
				z='{:%Y%m%d%H%M%S}'.format(datetime.datetime.now())
				for i in op_list:
					rech=requests.get("https://joloapi.com/api/recharge.php?mode=1&userid=devansh76&key=326208132556249&operator=%s&service=%s&amount=%s&orderid=%s&type=text" % (str(i),number,amount,z))
					if rech.text.split(',')[0] != 'FAILED':
						break
			mydb.insertExotelData(number,rech.text,z)
		return '200 OK'
#****************************************************************************

		
#****************************************************************************		
#yatra app definitions
@application.route('/yatradata', methods=['POST'])
def yatradata():
	f = request.form
	z='{:%Y%m%d%H%M%S}'.format(datetime.datetime.now())
	if(mydb.yatraDataExists(f['sender_number'],f['receiver_number'])):
		return "Done!"
	else:
		mydb.insertYatraData(f['sender_number'],f['receiver_number'],f['sender_name'].encode("utf-8"),f['receiver_name'].encode("utf-8"),f['datetime'],str(z))
		if(mydb.yatraDataExists(f['sender_number'],f['receiver_number'])):
			return "Done!"
		else:
			return "Not Done!"
#****************************************************************************	
	
	

#****************************************************************************	
#swara app definitions
@application.route('/swaratoken', methods=['POST'])
def swaratoken():
	f = request.get_json()
	z='{:%Y%m%d%H%M%S}'.format(datetime.datetime.now())
	mydb.insertSwaraToken(f['senderBTMAC'],f['receiverBTMAC'],f['filename'],f['appName'],f['phoneNumber'],f['carrierCode'],str(z))
	return str({"reply":'User does not exist'})

@application.route('/swarastat')
def swarastat():
	return current_app.response_class(mydb.getswarastat(), mimetype="application/json")
#****************************************************************************



#****************************************************************************	
#Mobile Satyagraha app CHAT definitions
@application.route('/')
def sessions():
	return render_template('session.html')

def messageReceived(methods=['GET', 'POST']):
	print('message was received!!!')
	
@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
	z='{:%Y%m%d%H%M%S}'.format(datetime.datetime.now())
	json["datetime"]=z
	socketio.emit('my response', json, callback=messageReceived, room=json["problem_id"])
	mydb.insertChatData(json["problem_id"],json["username"],json["message"],z)
	
@application.route('/loadChat/<problem_id>')
def loadChat(problem_id):
	return str(mydb.loadChat(problem_id))
	
@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    print(username + ' has entered the room.' + room)

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    print(username + ' has left the room.' + room)
#****************************************************************************



#****************************************************************************	
#Mobile Satyagraha definitions		
@application.route('/plist')
def plist():
	return str(mydb.fetchAll())

	
@application.route('/pblock/<int:s>/<int:e>')
def pblock(s,e):
	e=e-s
	return str(mydb.fetchBlock(s,e))
	
@application.route('/pqblock/<query>/<int:s>/<int:e>')
def pqblock(query,s,e):
	e=e-s
	return str(mydb.fetchQueryBlock(query,s,e))
	
@application.route('/pitem/<problem_id>')
def pitem(problem_id):
	return str(mydb.fetchOne(problem_id))
	
@application.route('/signup', methods=['POST'])
def signup():
	if request.form['inviteCode']=="SWARA123":
		if mydb.userExists(request.form['username']):
			return 'User Exists'
		else:
			mydb.insertUser(request.form['username'],hashlib.sha256(request.form['password']).hexdigest(),request.form['name'],request.form['email'])
			return 'Successful Signup'
	else:
		return 'Retry'
	
@application.route('/login', methods=['POST'])
def login():
	if not mydb.userExists(request.form['username']):
		return str({"reply":'User does not exist'})
	elif mydb.authenticateUser(request.form['username'],hashlib.sha256(request.form['password']).hexdigest())=="incorrect password":
		return str({"reply":'Login Unsuccessful'})
	else:
		return str({"reply":'Successful Login',"name":mydb.authenticateUser(request.form['username'],hashlib.sha256(request.form['password']).hexdigest())})

@application.route('/getSession', methods=['GET'])
def getSession():
	return str(mydb.getSessionID())

@application.route('/userCount/<problem_id>')
def userCount(problem_id):
	return str(mydb.userCount(problem_id))	

@application.route('/canAdoptProblem/<username>', methods=['POST', 'GET'])
def canAdoptProblem(username):
	if(mydb.canAdoptProblem(username)=="Yes"):
		return "Yes"
	else:
		return "No"

@application.route('/adoptProblem/<username>/<problem_id>')
def adoptProblem(username,problem_id):
	return mydb.adoptProblem(username,problem_id)
	
@application.route('/unAdoptProblem/<username>/<problem_id>')
def unAdoptProblem(username,problem_id):
	return mydb.unAdoptProblem(username,problem_id)

@application.route('/problemAgainstUser/<username>', methods=['POST', 'GET'])
def problemAgainstUser(username):
	return str(mydb.fetchProblemAgainstUser(username))
	
@application.route('/registerComment', methods=['POST'])
def registerComment():
	return mydb.registerComment(request.form['username'],request.form['problem_id'],request.form['comment'])
	
@application.route('/fetchComments/<problem_id>', methods=['POST'])
def fetchComments(problem_id):
	return str(mydb.fetchComments(problem_id))
#****************************************************************************


#APP RUN
#****************************************************************************		
if __name__ == '__main__':
    socketio.run(application, host='0.0.0.0', port=5000)
#****************************************************************************	
	
	
	