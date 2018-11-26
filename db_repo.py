import MySQLdb
import json
import datetime


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
		
	def insertYatraData(self,sender_number,receiver_number,sender_name,receiver_name,datetime):
		pingAndReconnect(self)
		self.c.execute("INSERT INTO yatra_data_2 (sender_number,receiver_number,sender_name,receiver_name,datetime) VALUES (%s,%s,%s,%s,%s);",(sender_number,receiver_number,sender_name,receiver_name,datetime) )
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
		land="%LAND=%"
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
		
	def insertUser(self,username,password_hash,name,email):
		pingAndReconnect(self)
		self.c.execute("INSERT INTO app_credentials (username, password_hash, name, email) VALUES (%s,%s,%s,%s);",(username,password_hash,name,email))
		self.conn.commit()
		
	def registerComment(self,username,problem_id,comment):
		pingAndReconnect(self)
		self.c.execute("INSERT INTO app_comments (username, problem_id, comments) VALUES (%s,%s,%s);",(username,problem_id,comment.encode("utf-8")))
		self.conn.commit()
		return "Done"
		
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
		if(len(db_response)==0):
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
		db_response=self.c.execute("SELECT * FROM app_users_per_problem2 WHERE problem_id = %s;",(problem_id,))
		db_response=self.c.fetchall()
		if(len(db_response)==0):
			self.c.execute("INSERT INTO app_users_per_problem2 (problem_id, user1, user2) VALUES (%s,%s,%s);",(problem_id,username,''))
			self.conn.commit()
			response="Adopted"
		elif db_response[0][1] is '':
			self.c.execute("UPDATE app_users_per_problem2 SET user1 = %s WHERE (problem_id = %s);",(username,problem_id))
			self.conn.commit()
			response= "Adopted"
		elif db_response[0][2] is '':
			self.c.execute("UPDATE app_users_per_problem2 SET user2 = %s WHERE (problem_id = %s);",(username,problem_id))
			self.conn.commit()
			response= "Adopted"
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
	