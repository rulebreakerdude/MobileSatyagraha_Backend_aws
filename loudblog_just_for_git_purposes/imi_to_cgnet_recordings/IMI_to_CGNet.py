import ftplib
import subprocess
from db_repo import *
import smtplib
#from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from mutagen.mp3 import MP3

mydb=database_flaskr()
MY_ADDRESS = 'cgnetmail2019@gmail.com'
PASSWORD = 'QWERTYCGTECH123'


s = smtplib.SMTP_SSL(host='smtp.gmail.com', port=465)
s.ehlo()
s.set_debuglevel(1)
s.login(MY_ADDRESS, PASSWORD)
email='cgnetswaratest@gmail.com'


session = ftplib.FTP('59.162.167.59','Cgnet','mdy8YtLIzxf2')
session.cwd("/Recordings")
unsyncedFiles = mydb.getCGSwaraUnsyncedNumberData()
for row in unsyncedFiles:
	print row
	ref_id=row[0]
	phoneNumber=row[1]
	filetocopy = ref_id+'.wav'
	localfile = open('temp.wav', 'wb')
	try:
		session.retrbinary('RETR ' + filetocopy, localfile.write)
		localfile.close()
		subprocess.call(['lame', 'temp.wav', '%s.mp3' %(ref_id)])
		localmp3=open('%s.mp3' %(ref_id), 'rb')
		time='{:%Y%m%d%H%M%S}'.format(datetime.datetime.now())
		length=str(MP3(ref_id+'.mp3').info.length)
		subject = "Swara-Main|app|" + length + "|DRAFT|" + phoneNumber + "|unk|" + time + "|PUBLIC";
		message = "Recording sent from IMI cloud IVR"
		msg = MIMEMultipart()
		msg['From'] = MY_ADDRESS
		msg['To'] = email
		msg['Subject'] = subject
		msg.attach(MIMEText(message, 'plain'))
		part = MIMEBase('application', 'octet-stream')
		part.set_payload((localmp3).read())
		encoders.encode_base64(part)
		part.add_header('Content-Disposition', "attachment; filename= %s.mp3" %(ref_id))
		msg.attach(part)
		s.sendmail(msg['From'],msg['To'],msg.as_string())
		subprocess.call(['rm','%s.mp3' %(ref_id)])
		mydb.setCGSwaraSyncedNumberData(ref_id)
	except ftplib.error_perm:
		print filetocopy+' not present'
	

session.quit()
