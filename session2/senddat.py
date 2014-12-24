import json,urllib,urllib2
ip="http://10.1.10.150:9000"
def send(data):
	global ip
	dat=data#json.dumps(data)
	request = urllib2.Request(ip)
	request.add_header('Content-type', 'text/plain')
	response = urllib2.urlopen(request,dat)
	#print response,type(response)
	ret= response.read()
	retv=json.loads(ret)
	return retv
