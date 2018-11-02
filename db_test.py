from db_repo import *
mydb=database_flaskr()
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
