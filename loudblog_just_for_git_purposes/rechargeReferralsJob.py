import requests
from db_repo import *
mydb=database_flaskr()
rows=mydb.getEligibleReferrals()
for row in rows:
	id=row[0]
	number=row[1]
	if id==2:
		rech=requests.get("http://flask-aws-dev.ap-south-1.elasticbeanstalk.com/l2eReferralRecharge/"+str(id)+"/"+str(number))
		print rech