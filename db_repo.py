import MySQLdb
import json
import datetime

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
	#Learn2Earn Definitions
	def insertLearn2EarnRecordNumberData(self,tid,phoneNumber,datetime):
		pingAndReconnect(self)
		self.c.execute("INSERT INTO learn2earn_pilkha_ksheer_call_actions (tid,phoneNumber,datetime_of_call) VALUES (%s,%s,%s);",(tid,phoneNumber,datetime) )
		self.conn.commit()
		
	def insertLearn2EarnRechargeData(self,phoneNumber,recharge_status,datetime):
		pingAndReconnect(self)
		self.c.execute("INSERT INTO learn2earn_pilkha_ksheer_call_actions (phoneNumber,recharge_status,datetime_of_recharge) VALUES (%s,%s,%s);",(phoneNumber,recharge_status,datetime) )
		self.conn.commit()
#****************************************************************************	



#****************************************************************************		
	#CGSwara Definitions
	def insertCGSwaraRecordNumberData(self,phoneNumber,datetime):
		pingAndReconnect(self)
		self.c.execute("INSERT INTO CGSwara_IMI_call_log (phoneNumber,datetime_of_api_call) VALUES (%s,%s);",(phoneNumber,datetime) )
		self.conn.commit()
		
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
		db_parse_2=[{"Total People Trained:":x[0]} for x in db_response_1]
		db_response=self.c.execute("SELECT sender_number, max(sender_name), count(*) FROM flaskdb.yatra_data_2 group by sender_number order by (3) desc;")
		db_response=self.c.fetchall()
		db_parse=[{str(x[0]): "Name: "+x[1]+". People Trained: "+str(x[2])} for x in db_response]
		db_parse_2.append(db_parse)
		return json.dumps(db_parse_2, indent=4)
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
	