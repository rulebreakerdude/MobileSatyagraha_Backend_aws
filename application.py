import os
import eventlet
import datetime
import requests
import json

from flask import Flask, render_template, request, current_app, Response
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
#Learn2Earn Definitions
@application.route('/learn2earnRecordNumber/<tid>/<phoneNumber>', methods=['GET'])
def learn2earnRecordNumber(tid,phoneNumber):
	if request.method == 'GET':
		z='{:%Y%m%d%H%M%S}'.format(datetime.datetime.now())
		mydb.insertLearn2EarnRecordNumberData(tid,phoneNumber,z)
	return Response('1', mimetype="text/dtmf;charset=UTF-8")
	
@application.route('/learn2earnRedirector/<tid>', methods=['GET'])
def learn2earnRedirector(tid):
	if request.method == 'GET':
		direction = mydb.learn2earnRedirector(tid)
	return Response(direction, mimetype="text/dtmf;charset=UTF-8")
	
@application.route('/l2eUpdateQuestionResponse/<tid>/<question>/<response>', methods=['GET'])
def l2eUpdateQuestionResponse(tid,question,response):
	if request.method == 'GET':
		mydb.l2eUpdateQuestionResponse(tid,question,response)
	return Response('1', mimetype="text/dtmf;charset=UTF-8")
		
@application.route('/learn2earnRechargeNumber/<tid>/<phoneNumber>', methods=['GET'])
def learn2earnRechargeNumber(tid,phoneNumber):
	if request.method == 'GET':
		HLR(tid,phoneNumber[1:])
	return Response('1', mimetype="text/dtmf;charset=UTF-8")
	
def HLR(tid,number):
	local_HLR=mydb.getHLRData(number)
	if not local_HLR[0]:
		dict_HLR_op_code={}
		dict_HLR_op_code_new={}
		with open('HLR.json') as f:
			dict_HLR_op_code = json.load(f)
		HLR_to_op={'aircel':'1','bsnl':'3','airtel':'28','vodafone':'22','docomo':'17','reliance':'13','idea':'8','uninor':'19','videocon':'5'}
		op_code_map={'1':'AL','3':'BS','28':'AT','8':'IDX','10':'MS','12':'RL','13':'RG','17':'TD','19':'UN','5':'VD','22':'VF'}
		for mccmnc in dict_HLR_op_code:
			lookup_query=dict_HLR_op_code[mccmnc]
			for op in HLR_to_op:
				if op in lookup_query:
					dict_HLR_op_code_new[mccmnc]=op_code_map[HLR_to_op[op]]
		PWD="uTb5-CYC%-WTqm-MBaY-!aAT-ApSq"
		hlr_response=requests.get("https://www.hlr-lookups.com/api/?action=submitSyncLookupRequest&msisdn=+91%s&username=devansh76-api-3874a453262b&password=%s" %(str(number),PWD))
		h_r=json.loads(hlr_response.text)
		mccmnc=h_r["results"][0]["mccmnc"]
		if mccmnc in dict_HLR_op_code_new:
			mydb.insertHLRData(number,dict_HLR_op_code_new[mccmnc])
			mydb.insertLearn2EarnOpCodeData(tid,dict_HLR_op_code_new[mccmnc])
			recharge_HLR(tid,number,dict_HLR_op_code_new[mccmnc])
		else:
			mydb.insertLearn2EarnOpCodeData(tid,mccmnc)
	else:
		op_code=local_HLR[1]
		mydb.insertLearn2EarnOpCodeData(tid,op_code)
		recharge_HLR(tid,number,op_code)
		
def recharge_HLR(tid,number,op_code):
	amount=10
	z='{:%Y%m%d%H%M%S}'.format(datetime.datetime.now())
	rech=requests.get("https://joloapi.com/api/recharge.php?mode=1&userid=devansh76&key=326208132556249&operator=%s&service=%s&amount=%s&orderid=%s&type=text" % (op_code,str(number),amount,z))
	print rech.text
	mydb.insertLearn2EarnRechargeData(tid,rech.text,z)
	
def recharge_new(number):
	print number
	op_code="VF"#WARNING REMOVE THIS
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
		op_list=['VF','IDX','BSS','BS','AT','TW','T24S','T24','VC','VGS','VG','VDS','VD','TI','TDS','TD','AL','MS','UNS','UN','RG','RL']
		z='{:%Y%m%d%H%M%S}'.format(datetime.datetime.now())
		for i in op_list:
			rech=requests.get("https://joloapi.com/api/recharge.php?mode=1&userid=devansh76&key=326208132556249&operator=%s&service=%s&amount=%s&orderid=%s&type=text" % (str(i),number,amount,z))
			if rech.text.split(',')[0] != 'FAILED':
				break
	mydb.insertLearn2EarnRechargeData(number,rech.text,z)

#****************************************************************************




#****************************************************************************
#CGSwara Definitions
@application.route('/CGSwaraRecordNumber/<phoneNumber>', methods=['GET'])
def CGSwaraRecordNumber(phoneNumber):
	if request.method == 'GET':
		z='{:%Y%m%d%H%M%S}'.format(datetime.datetime.now())
		mydb.insertCGSwaraRecordNumberData(phoneNumber,z)
	return Response('1', mimetype="text/dtmf;charset=UTF-8")
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
			
#yatra app definitions
@application.route('/getYatraStat', methods=['GET'])
def getYatraStat():
	f = request.form
	return current_app.response_class(mydb.getYatraStat(), mimetype="application/json")
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
	
	
	