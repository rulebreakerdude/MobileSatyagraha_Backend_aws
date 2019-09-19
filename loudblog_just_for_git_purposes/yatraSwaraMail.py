import smtplib

from string import Template

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from db_repo import *

MY_ADDRESS = 'cgnetmail2019@gmail.com'
PASSWORD = 'QWERTYCGTECH123'
mydb=database_flaskr()
print mydb.getYatraSwaraData()
def main():
	# set up the SMTP server
	s = smtplib.SMTP_SSL(host='smtp.gmail.com', port=465)
	#s.starttls()
	s.ehlo()
	s.set_debuglevel(1)
	s.login(MY_ADDRESS, PASSWORD)
	emails=['sharma.alok.jr@gmail.com','smitashu@gmail.com','devansh76@gmail.com','vipin@cgnet.in']

	# For each contact, send the email:
	for email in emails:
		msg = MIMEMultipart()		# create a message

		# add in the actual person name to the message template
		message = "PFB the Cumulative report for Yatra-Swara data\n\n" + mydb.getYatraSwaraData()

		# Prints out the message body for our sake
		print(message)

		# setup the parameters of the message
		msg['From']=MY_ADDRESS
		msg['To']=email
		msg['Subject']="This is TEST"
		
		# add in the message body
		msg.attach(MIMEText(message, 'plain'))
		
		# send the message via the server set up earlier.
		s.sendmail(msg['From'],msg['To'],message)
		del msg
		
	# Terminate the SMTP session and close the connection
	s.quit()
	
if __name__ == '__main__':
	main()