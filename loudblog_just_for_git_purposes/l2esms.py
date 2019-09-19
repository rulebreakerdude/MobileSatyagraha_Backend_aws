# -*- coding: utf-8 -*-
'''
Set the following parameters with appropriate values
senderAddress
address
message
'''


import json
import httplib
import urllib
import datetime
import requests
from db_repo import *

mydb=database_flaskr()
rows=mydb.smsReferredUsers()
for row in rows:
	phoneNumber=row[0]
	referredBy=row[1][1:]
	id=row[2]
	channel=row[3]
	if channel=="halbi":
		numb="04071514095"
	else:
		numb="04071514050"
	if phoneNumber != referredBy:
			mydb.updateStatusSms(id)
			msgtext="क्या आपको १० रुपया का फ्री मोबाइल रिचार्ज चाहिए? तो तुरंत "+numb+" पे मिस्ड कॉल करे और दंतेवाड़ा उपचुनाव के बारे में तीन सवालों का सही उत्तर दो। सिर्फ आपको नहीं, अपने दोस्त, जिसका नंबर "+referredBy+" हैं, को भी रिचार्ज मिलेगा!"
			apiurl= "http://api-openhouse.imimobile.com/smsmessaging/1/outbound/tel%3A%2BCGNETS/requests"
			#JSON object to be sent in the POST body.
			rawdata = {"outboundSMSMessageRequest":{"address":["tel:"+phoneNumber],"senderAddress":"tel:CGNETS","outboundSMSTextMessage":{"message":msgtext},"messageType":"4"}}
			data1 = json.dumps(rawdata)
			headers = {"key": "01b8ab23-78cd-4317-bf41-95dd22fcece0","Content-type": "application/json","Accept": "application/json"}
			conn = httplib.HTTPConnection('api-openhouse.imimobile.com', timeout=100)
			conn.request("POST", "/smsmessaging/1/outbound/tel%3A%2BCGNETS/requests", data1, headers)
			response = conn.getresponse()
			print "================================================================="
			print 'header is = ', headers
			print 'apiurl is = ', apiurl
			print 'rawdata is = ', rawdata
			print 'encodeddata is = ', data1
			print 'conn is = ', conn
			print 'con.rqst is = ', conn.request
			print 'response is = ', response.read()
			print 'resp.stat is = ', response.status
			print 'resp.reason is = ', response.reason
			print "================================================================="
