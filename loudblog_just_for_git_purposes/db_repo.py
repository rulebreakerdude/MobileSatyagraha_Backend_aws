import MySQLdb
import json
import datetime
import requests

su="1234567891" #Superuser


def pingAndReconnect(self):
	try:
		self.conn.ping()
	except self.conn.OperationalError as e:
		print "Caught An Operational Error... #reconnecting"
		self.conn = MySQLdb.connect(
			host="cgdbaws.cv23wjqihuhm.ap-south-1.rds.amazonaws.com",
			port=3306,
			user="root",
			passwd="CGDBAWSsql"
		)
		self.c=self.conn.cursor()
		self.c.execute('USE flaskdb;')
	
class database_flaskr:

	def __init__(self):
		self.conn = MySQLdb.connect(
			host="cgdbaws.cv23wjqihuhm.ap-south-1.rds.amazonaws.com",
			port=3306,
			user="root",
			passwd="CGDBAWSsql"
		)
		self.c=self.conn.cursor()
		self.c.execute('USE flaskdb;')
		
#****************************************************************************		
	#test definitions	
	def yellowtest(self):
		pingAndReconnect(self)
		db_response=self.c.execute("SELECT * FROM aws_test;")
		db_response=self.c.fetchall()
		return str(db_response)
#****************************************************************************		
		
		
		
#****************************************************************************	
	#Mobile Satyagraha app CHAT definitions
	def insertChatData(self,problem_id,sender,message,datetime):
		pingAndReconnect(self)
		id=""+problem_id+":"+sender
		self.c.execute("INSERT INTO app_chat (problem_id,sender,message,datetime) VALUES (%s,%s,%s,%s);",(problem_id,sender,message,datetime) )
		self.conn.commit()
		
	def loadChat(self,problem_id):
		pingAndReconnect(self)
		db_response=self.c.execute(
			"SELECT * FROM app_chat WHERE problem_id = %s ORDER BY datetime ASC",(problem_id,))
		db_response=self.c.fetchall()
		db_parse=[{"id": str(x[0]),
					"problem_id": x[1], 
					"sender": x[2],
					"message": x[3],
					"datetime": str(x[4])} for x in db_response]
		return json.dumps(db_parse)
#****************************************************************************	



#****************************************************************************		
	#yatra definitions	
	def yatraDataExists(self,sender_number,receiver_number):
		pingAndReconnect(self)
		db_response=self.c.execute("SELECT * FROM yatra_data_2 WHERE sender_number = %s AND receiver_number = %s;",(sender_number,receiver_number) )
		return db_response>0
		
	def insertYatraData(self,sender_number,receiver_number,sender_name,receiver_name,datetime,datetimeServer):
		pingAndReconnect(self)
		self.c.execute("INSERT INTO yatra_data_2 (sender_number,receiver_number,sender_name,receiver_name,datetime,datetimeServer) VALUES (%s,%s,%s,%s,%s,%s);",(sender_number,receiver_number,sender_name,receiver_name,datetime,datetimeServer) )
		self.conn.commit()
		
	def getYatraStat(self):
		pingAndReconnect(self)
		db_response_1=self.c.execute("SELECT count(*) FROM yatra_data_2;")
		db_response_1=self.c.fetchall()
		db_parse_1=[{"Below is the Cumulative Report: Total People Trained:":x[0]} for x in db_response_1]
		
		db_response_2=self.c.execute("SELECT sender_number, max(sender_name), count(*) FROM flaskdb.yatra_data_2 group by sender_number order by (3) desc;")
		db_response_2=self.c.fetchall()
		db_parse_2=[{str(x[0]): "Name: "+x[1]+". People Trained: "+str(x[2])} for x in db_response_2]
		
		db_response_3=self.c.execute("SELECT distinct(substring(datetimeServer,1,8)) FROM flaskdb.yatra_data_2 order by (1) desc;")
		db_response_3=self.c.fetchall()
		last_date=db_response_3[1][0]
		db_parse_3=[{"Daily report for the date":last_date}]
		
		db_response_4=self.c.execute("SELECT sender_number, max(sender_name), count(*) as the_count FROM flaskdb.yatra_data_2 where substring(datetimeServer,1,8)=%s group by sender_number order by the_count desc;",(last_date,))
		db_response_4=self.c.fetchall()
		db_parse_4=[{str(x[0]): "Name: "+x[1]+". People Trained: "+str(x[2])} for x in db_response_4]
		
		db_parse_3.append(db_parse_4[0])
		db_parse_3.append(db_parse_1)
		db_parse_3.append(db_parse_2)
		return json.dumps(db_parse_3, indent=4)
		
	def getYatraSwaraData(self):
		pingAndReconnect(self)
		db_parse={}
		word="Apk"
		db_response_1=self.c.execute("SELECT count(distinct(concat(senderBTMAC, receiverBTMAC, filename))) as count1 FROM flaskdb.bultoo_transfer where filename != %s;",(word,))
		db_response_1=self.c.fetchall()
		db_parse["Total Bultoo Transfers"]=db_response_1[0][0]
		db_response_1=self.c.execute("SELECT count(distinct(concat(senderBTMAC, receiverBTMAC, filename))) as count1 FROM flaskdb.bultoo_transfer where filename = %s;",(word,))
		db_response_1=self.c.fetchall()
		db_parse["Total Apk Transfers"]=db_response_1[0][0]
		db_response_1=self.c.execute("SELECT sum(wallet_amount_pre_try) as earned_money, sum(wallet_amount_post_try) as leftover_money FROM flaskdb.swara_recharges;")
		db_response_1=self.c.fetchall()
		db_parse["Total Amount Spent"]=int(db_response_1[0][0])-int(db_response_1[0][1])
		return json.dumps(db_parse, indent=4)
		
	def yatraWPA(self):
		pingAndReconnect(self)
		self.c.execute("drop table temp1;")
		self.conn.commit()
		self.c.execute("create table temp1 as select receiver_number, sender_number, min(datetimeServer) as datetimeServer, receiver_name from flaskdb.yatra_data_2 group by 1,2 order by 1,2,3 desc;")
		self.conn.commit()
		word=""
		self.c.execute("delete from flaskdb.temp1 where receiver_number = 7985622386 or receiver_number = 6264241440 or receiver_number = 8527837805 or receiver_number = 9717078576 or receiver_number = 3213213211 or sender_number=%s or sender_number=9717078576 or sender_number=6264241440;",(word,))
		self.conn.commit()
		self.c.execute("drop table temp2;")
		self.conn.commit()
		self.c.execute("create table temp2 as select distinct(user) from flaskdb.app_problem_list_backup_2 where status=3 and user in (select receiver_number from temp1);")
		self.conn.commit()
		self.c.execute("drop table temp3;")
		self.conn.commit()
		word="%success%"
		self.c.execute("create table temp3 as select distinct(rf1) as phone_number from flaskdb.swara_recharges where status like %s and rf1 in (select receiver_number from temp1);",(word,))
		self.conn.commit()
		self.c.execute("drop table temp4;")
		self.conn.commit()
		self.c.execute("create table temp4 as select * from temp1 left join temp2 on temp1.receiver_number=temp2.user left join temp3 on temp1.receiver_number = temp3.phone_number;")
		self.conn.commit()
		self.c.execute("drop table temp5;")
		self.conn.commit()
		self.c.execute("create table temp5 as SELECT * FROM flaskdb.temp4 where datetimeServer is NOT NULL;")
		self.conn.commit()
		self.c.execute("drop table temp6;")
		self.conn.commit()
		self.c.execute("create table temp6 as SELECT receiver_number, min(datetimeServer) as ds FROM flaskdb.temp5 group by receiver_number order by (1) desc;")
		self.conn.commit()
		self.c.execute("drop table temp7;")
		self.conn.commit()
		self.c.execute("create table temp7 as select temp5.* from temp6 left join temp5 on temp6.receiver_number = temp5.receiver_number and temp6.ds = temp5.datetimeServer;")
		self.conn.commit()
		self.c.execute("drop table temp8;")
		self.conn.commit()
		self.c.execute("create table temp8 as SELECT sender_number, count(*) as trained, sum(user>0) as point_cgnet, sum(phone_number>0) as point_swara FROM flaskdb.temp7 group by (1);")
		self.conn.commit()
		self.c.execute("drop table temp9;")
		self.conn.commit()
		self.c.execute("create table temp9 as select max(sender_name) as sender_name,sender_number from yatra_data_2 group by (2);")
		self.conn.commit()
		self.c.execute("drop table temp10;")
		self.conn.commit()
		self.c.execute("create table temp10 as select temp9.sender_name,temp8.* from temp8 left join temp9 on temp8.sender_number=temp9.sender_number  order by point_cgnet desc,point_swara desc, trained  desc;")
		self.conn.commit()
		self.c.execute("start transaction;")
		self.conn.commit()		
#****************************************************************************	



#****************************************************************************
	#Learn2Earn definition
	def tryLearn2EarnRechargeFailed(self):
		pingAndReconnect(self)
		word_3=""
		word_1="%no%"
		word_2="4%"
		db_response = self.c.execute("Select tid, phoneNumber, recharge_given, oth_data_1 FROM learn2earn_pilkha_ksheer_call_actions WHERE response_consent > %s and (recharge_given LIKE %s OR oth_data_1 LIKE %s or oth_data_1 is null);",(word_3,word_1,word_2))
		db_response = self.c.fetchall()
		for row in db_response:
			tid=row[0]
			phoneNumber=row[1]
			print "Trying number: "+phoneNumber+" of tid: "+tid
			a=requests.get("http://flask-aws-dev.ap-south-1.elasticbeanstalk.com/learn2earnRechargeNumber/"+tid+"/"+phoneNumber)
			print a.text
			
	def smsReferredUsers(self):
		pingAndReconnect(self)
		#self.c.execute("DELETE FROM l2e_referral_data where phone_number=substring(referred_by,2,10) OR LENGTH(phone_number)<10;")
		#self.conn.commit()
		db_response = self.c.execute("Select phone_number,referred_by,id,oth_data_1 FROM l2e_referral_data WHERE sms_sent is NULL;")
		db_response=self.c.fetchall()
		return db_response
		
	def updateStatusSms(self,id):
		word="yes"
		self.c.execute("UPDATE l2e_referral_data SET sms_sent = %s WHERE (id = %s);",(word,id))
		self.conn.commit()
		
	def getEligibleReferrals(self):
		word="%yes%"
		db_response=self.c.execute("select id,referred_by FROM flaskdb.l2e_referral_data where (recharge_given is NULL or recharge_given not like %s) and concat(0,phone_number) in (select phoneNumber from flaskdb.learn2earn_pilkha_ksheer_call_actions where recharge_given like %s);",(word,word))
		db_response=self.c.fetchall()
		return db_response
#****************************************************************************	



#****************************************************************************
	#exotel definition for ICTD		
	def insertExotelData(self,caller_id,recharge_status,datetime):
		pingAndReconnect(self)
		self.c.execute("INSERT INTO exotel_data (caller_id,recharge_status,datetime) VALUES (%s,%s,%s);",(caller_id,recharge_status,datetime) )
		self.conn.commit()
#****************************************************************************	

		
		
#****************************************************************************		
	#swara app definitions	
	def insertSwaraToken(self, senderBTMAC, receiverBTMAC, filename, appName, phoneNumber, carrierCode, datetime):
		pingAndReconnect(self)
		self.c.execute("INSERT INTO bultoo_transfer (senderBTMAC, receiverBTMAC, filename, appName, phoneNumber, carrierCode, datetime) VALUES (%s,%s,%s,%s,%s,%s,%s);",(senderBTMAC, receiverBTMAC, filename, appName, phoneNumber, carrierCode, datetime) )
		self.conn.commit()
		
	def getswarastat(self):
		pingAndReconnect(self)
		db_response=self.c.execute("SELECT count(*) FROM bultoo_transfer;")
		db_response=int(self.c.fetchall()[0][0])-15
		d={}
		d["Total Stories Shared"]=db_response
		blank=""
		db_response=self.c.execute("SELECT phoneNumber, count(*) FROM bultoo_transfer WHERE phoneNumber != %s and phoneNumber != \"a\" and phoneNumber != \"9717078576\" GROUP BY phoneNumber ORDER BY (2) DESC;",(blank,))
		db_response=self.c.fetchall()
		db_parse=[{str(x[0]):str(x[1])} for x in db_response]
		db_response=self.c.execute("SELECT SUBSTRING(datetime,1,8), count(*) FROM bultoo_transfer WHERE phoneNumber != %s and phoneNumber != \"a\" and phoneNumber != \"9717078576\" GROUP BY (1) ORDER BY (1) DESC;",(blank,))
		db_response=self.c.fetchall()
		db_parse2=[{str(x[0]):str(x[1])} for x in db_response]
		db_parse.extend(db_parse2)
		db_parse.append(d)
		return json.dumps(db_parse,indent=4)
#****************************************************************************	



#****************************************************************************
	#Mobile Satyagraha definitions			
	def insertUser(self,username,password_hash,name,email):
		pingAndReconnect(self)
		self.c.execute("INSERT INTO app_credentials (username, password_hash, name, email) VALUES (%s,%s,%s,%s);",(username,password_hash,name,email))
		self.conn.commit()
		
	def fetchAll(self):
		pingAndReconnect(self)
		db_response=self.c.execute(
			"SELECT id, message_input, user, user, status, tags, posted, title, audio_length FROM app_problem_list WHERE status = 3 AND tags LIKE \'%PROBLEM%\' ORDER BY posted DESC LIMIT 3;")
		db_response=self.c.fetchall()
		db_parse=[{"problem_id": str(x[0]),
					"problem_text": x[1].decode("utf-8"), 
					"phone_number_r": x[2],
					"phone_number_o": x[3],
					"status": str(x[4]),
					"comments": x[5],
					"datetime": str(x[6].strftime("%d %B")),
					"problem_desc": x[7].decode("utf-8"),
					"duration": str(x[8])} for x in db_response]
		return json.dumps(db_parse)
		
	def fetchBlock(self,s,e):
		pingAndReconnect(self)
		blank=""
		song="%SONG%"
		news="%NEWS%"
		culture="%CULTURE%"
		bultoo="%BULTOO%"
		problem="%PROBLEM%"
		coal="%COAL%"
		mining="%MINING%"
		education="%EDUCATION%"
		food="%FOOD%"
		forest="%FOREST%"
		land="%LAND%"
		electricity="%ELECTRICITY%"
		water="%WATER%"
		handpump="%HANDPUMP%"
		nrega="%NREGA%"
		db_response=self.c.execute(
			"SELECT id, message_input, user, user, status, tags, posted, title, audio_length FROM app_problem_list WHERE tags not like %s and tags not like %s and tags not like %s and tags not like %s and (tags LIKE %s or tags LIKE %s or tags LIKE %s or tags LIKE %s or tags LIKE %s or tags LIKE %s or tags LIKE %s or tags LIKE %s or tags LIKE %s or tags LIKE %s or tags LIKE %s) and id not in (select problem_id from app_users_per_problem2 where user1 != %s and user2 != %s) ORDER BY posted DESC LIMIT %s, %s;" 
			,(song,news,culture,bultoo,problem,coal,mining,education,food,forest,land,electricity,water,handpump,nrega,blank,blank,s,e))
		db_response=self.c.fetchall()
		db_parse=[{"problem_id": str(x[0]),
					"problem_text": x[1].decode("utf-8"), 
					"phone_number_r": x[2],
					"phone_number_o": x[3],
					"status": str(x[4]),
					"comments": x[5],
					"datetime": str(x[6].strftime("%d %B")),
					"problem_desc": x[7].decode("utf-8"),
					"duration": str(x[8])} for x in db_response]
		return json.dumps(db_parse)
		
	def fetchQueryBlock(self,query,s,e):
		pingAndReconnect(self)
		query="%"+query.encode("utf-8")+"%"
		song="%SONG%"
		news="%NEWS%"
		culture="%CULTURE%"
		bultoo="%BULTOO%"
		problem="%PROBLEM%"
		coal="%COAL%"
		mining="%MINING%"
		education="%EDUCATION%"
		food="%FOOD%"
		forest="%FOREST%"
		land="%LAND%"
		electricity="%ELECTRICITY%"
		water="%WATER%"
		handpump="%HANDPUMP%"
		nrega="%NREGA%"
		db_response=self.c.execute(
			"SELECT id, message_input, user, user, status, tags, posted, title, audio_length FROM app_problem_list WHERE (message_input like %s or tags like %s or title like %s) and tags not like %s and tags not like %s and tags not like %s and tags not like %s and (tags LIKE %s or tags LIKE %s or tags LIKE %s or tags LIKE %s or tags LIKE %s or tags LIKE %s or tags LIKE %s or tags LIKE %s or tags LIKE %s or tags LIKE %s or tags LIKE %s) ORDER BY posted DESC LIMIT %s, %s;" 
			,(query,query,query,song,news,culture,bultoo,problem,coal,mining,education,food,forest,land,electricity,water,handpump,nrega,s,e))
		db_response=self.c.fetchall()
		db_parse=[{"problem_id": str(x[0]),
					"problem_text": x[1].decode("utf-8"), 
					"phone_number_r": x[2],
					"phone_number_o": x[3],
					"status": str(x[4]),
					"comments": x[5],
					"datetime": str(x[6].strftime("%d %B")),
					"problem_desc": x[7].decode("utf-8"),
					"duration": str(x[8])} for x in db_response]
		return json.dumps(db_parse)
		
	def fetchProblemAgainstUser(self,username):
		pingAndReconnect(self)
		if str(username) == su: #Superuser
			db_response_2=self.c.execute(
				"SELECT id, message_input, user, user, status, tags, posted, title, audio_length FROM app_problem_list WHERE id in (SELECT problem_id FROM ms_su_problems);")
			db_response_2=self.c.fetchall()
			db_parse=[{"problem_id": str(x[0]),
						"problem_text": x[1].decode("utf-8"), 
						"phone_number_r": x[2],
						"phone_number_o": x[3],
						"status": str(x[4]),
						"comments": x[5],
						"datetime": str(x[6].strftime("%d %B")),
						"problem_desc": x[7].decode("utf-8"),
						"duration": str(x[8])} for x in db_response_2]
			return json.dumps(db_parse)
			
		db_response_1=self.c.execute(
			"SELECT * FROM app_problems_per_user WHERE username = %s;",(username,))
		db_response_1=self.c.fetchall()
		if(len(db_response_1)>0):
			db_response=self.c.execute(
				"SELECT id, message_input, user, user, status, tags, posted, title, audio_length FROM app_problem_list WHERE id = %s OR id = %s;" ,(db_response_1[0][1],db_response_1[0][2]))
			db_response=self.c.fetchall()
			db_parse=[{"problem_id": str(x[0]),
						"problem_text": x[1].decode("utf-8"), 
						"phone_number_r": x[2],
						"phone_number_o": x[3],
						"status": str(x[4]),
						"comments": x[5],
						"datetime": str(x[6].strftime("%d %B")),
						"problem_desc": x[7].decode("utf-8"),
						"duration": str(x[8])} for x in db_response]
			return json.dumps(db_parse)
		
	def fetchTest(self):
		pingAndReconnect(self)
		db_response=self.c.execute("SELECT message_input FROM app_problem_list WHERE status = 3 ORDER BY posted DESC LIMIT 3;")
		db_response=self.c.fetchall()
		db_parse=[[x[0].decode("utf-8")] for x in db_response]
		return db_parse
		
	def fetchOne(self, problem_id):
		pingAndReconnect(self)
		db_response=self.c.execute("SELECT id, message_input, user, user, status, tags, posted, title, audio_length FROM app_problem_list WHERE id = %s;",(problem_id,))
		db_response=self.c.fetchall()
		db_parse=[{"problem_id": str(x[0]),
					"problem_text": x[1].decode("utf-8"), 
					"phone_number_r": x[2],
					"phone_number_o": x[3],
					"status": str(x[4]),
					"comments": x[5],
					"datetime": str(x[6].strftime("%d %B")),
					"problem_desc": x[7].decode("utf-8"),
					"duration": str(x[8])} for x in db_response][0]

		return json.dumps(db_parse)
		
	def registerComment(self,username,problem_id,comment):
		pingAndReconnect(self)
		z='{:%Y%m%d%H%M%S}'.format(datetime.datetime.now())
		self.c.execute("INSERT INTO app_comments (username, problem_id, comments, datetime) VALUES (%s,%s,%s,%s);",(username,problem_id,comment.encode("utf-8"),z))
		self.conn.commit()
		return "Done"
		
	def fetchComments(self,problem_id):
		pingAndReconnect(self)
		db_response=self.c.execute("SELECT * FROM app_comments WHERE problem_id = %s ORDER BY datetime DESC;",(problem_id,))
		db_response=self.c.fetchall()
		db_parse=[{"username": str(x[0]),
					"problem_id": str(x[1]), 
					"comments": str(x[2]),
					"datetime": str(x[3])} for x in db_response]
		return json.dumps(db_parse)
		
	def userExists(self,username):
		pingAndReconnect(self)
		db_response=self.c.execute("SELECT DISTINCT username FROM app_credentials WHERE username = %s ;",(username,))
		return db_response>0
		
	def authenticateUser(self,username,password_hash):
		pingAndReconnect(self)
		db_response=self.c.execute("SELECT DISTINCT name FROM app_credentials WHERE username = %s and password_hash = %s;",(username,password_hash))
		db_response=self.c.fetchall()
		if len(db_response)>0:
			return db_response[0][0]
		else:
			return "incorrect password"
		
	def canAdoptProblem(self,username):
		pingAndReconnect(self)
		db_response=self.c.execute("SELECT * FROM app_problems_per_user WHERE username = %s;",(username,))
		db_response=self.c.fetchall()
		if(len(db_response)==0 or str(username) == su):#Superuser
			return "Yes"
		elif db_response[0][1] is '': 
			return "Yes"
		elif db_response[0][2] is '':
			return "Yes"
		else:
			return "No"
	
	def userCount(self,problem_id):
		pingAndReconnect(self)
		db_response=self.c.execute("SELECT * FROM app_users_per_problem2 WHERE problem_id = %s;",(problem_id,))
		db_response=self.c.fetchall()
		if(len(db_response)==0):
			return 0
		elif db_response[0][1] is not '' and db_response[0][2] is not '':
			return 2
		elif db_response[0][1] is '' and db_response[0][2] is '':
			return 0
		else:
			return 1
			
	def adoptProblem(self,username,problem_id):
		pingAndReconnect(self)
		if str(username) == su: #Superuser
			self.c.execute("INSERT INTO ms_su_problems (problem_id) VALUES (%s);",(problem_id,))
			self.conn.commit()
			response="Adopted"
			return response
			
		db_response=self.c.execute("SELECT * FROM app_users_per_problem2 WHERE problem_id = %s;",(problem_id,))
		db_response=self.c.fetchall()
		if(len(db_response)==0):
			self.c.execute("INSERT INTO app_users_per_problem2 (problem_id, user1, user2) VALUES (%s,%s,%s);",(problem_id,username,''))
			self.conn.commit()
			response="Adopted"
		elif db_response[0][1] is '' and  db_response[0][2] is '':
			self.c.execute("UPDATE app_users_per_problem2 SET user1 = %s WHERE (problem_id = %s);",(username,problem_id))
			self.conn.commit()
			response= "Adopted"
		#elif db_response[0][2] is '':
		#	self.c.execute("UPDATE app_users_per_problem2 SET user2 = %s WHERE (problem_id = %s);",(username,problem_id))
		#	self.conn.commit()
		#	response= "Adopted"
		else:
			response= "Users Full"
		if response != "Users Full":
			database_flaskr.registerProblemAgainstUser(self,username,problem_id)
		return response
	
	def registerProblemAgainstUser(self,username,problem_id):
		pingAndReconnect(self)
		db_response=self.c.execute("SELECT * FROM app_problems_per_user WHERE username = %s;",(username,))
		db_response=self.c.fetchall()
		if(len(db_response)==0):
			self.c.execute("INSERT INTO app_problems_per_user (username, problem1, problem2) VALUES (%s,%s,%s);",(username,problem_id,''))
			self.conn.commit()
		elif db_response[0][1] is '': 
			self.c.execute("UPDATE app_problems_per_user SET problem1 = %s WHERE (username = %s);",(problem_id,username))
			self.conn.commit()
		elif db_response[0][2] is '':
			self.c.execute("UPDATE app_problems_per_user SET problem2 = %s WHERE (username = %s);",(problem_id,username))
			self.conn.commit()
			
	def unAdoptProblem(self,username,problem_id):
		pingAndReconnect(self)
		if str(username) == su: #Superuser
			self.c.execute("DELETE from ms_su_problems WHERE (problem_id = %s);",(problem_id,))
			self.conn.commit()
			response= "UnAdopted"
			return response
		
		db_response=self.c.execute("SELECT * FROM app_users_per_problem2 WHERE problem_id = %s;",(problem_id,))
		db_response=self.c.fetchall()
		if db_response[0][1]==username:
			self.c.execute("UPDATE app_users_per_problem2 SET user1 = %s WHERE (problem_id = %s);",('',problem_id))
			self.conn.commit()
			response= "UnAdopted"
		elif db_response[0][2]==username:
			self.c.execute("UPDATE app_users_per_problem2 SET user2 = %s WHERE (problem_id = %s);",('',problem_id))
			self.conn.commit()
			response= "UnAdopted"
		else:
			response= "Was it really your problem?"
		if response != "Was it really your problem?":
			database_flaskr.deRegisterProblemAgainstUser(self,username,problem_id)
		return response
	
	def deRegisterProblemAgainstUser(self,username,problem_id):
		pingAndReconnect(self)
		db_response=self.c.execute("SELECT * FROM app_problems_per_user WHERE username = %s;",(username,))
		db_response=self.c.fetchall()
		if db_response[0][1]==problem_id: 
			self.c.execute("UPDATE app_problems_per_user SET problem1 = %s WHERE (username = %s);",('',username))
			self.conn.commit()
		elif db_response[0][2]==problem_id:
			self.c.execute("UPDATE app_problems_per_user SET problem2 = %s WHERE (username = %s);",('',username))
			self.conn.commit()
#****************************************************************************			
	