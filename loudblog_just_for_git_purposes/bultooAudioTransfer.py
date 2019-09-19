import requests
import subprocess



a=requests.get("http://flask-aws-dev.ap-south-1.elasticbeanstalk.com/pblockswara/BULTOO/0/20")
b=eval(a.text)
for x in range(0,len(b)):
	p_id=b[x]["audio_file"]
	p_audio=requests.get("http://cgnetswara.org/audio/"+str(p_id)+".mp3")
	with open("test.mp3","wb") as f:
		f.write(p_audio.content)
	subprocess.call(['aws','s3','cp','test.mp3','s3://cgstories/'+str(p_id)+".mp3"])
	subprocess.call(['aws', 's3api', 'put-object-acl', '--bucket', 'cgstories', '--key', str(p_id)+".mp3", '--acl', 'public-read'])
