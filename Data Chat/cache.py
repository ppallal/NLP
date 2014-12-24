import json
cacheData = {}
def cacheInit():
	f = open("cache.json","w")	
	global cacheData
	cacheData = json.parse(f.read())

def cacheUpdate(org,model,value):
	global cacheData
	 	
	
	if(org in cacheData):
		cacheData[org][model] = value
	else:
		cacheData[org]={}
		cacheData[org][model] = value

def chacheGet(org,model):
	global cacheData
	if(model==None):
		if(org['fullData']):
					
	if(org in cacheData and model in cacheData[org]):
		return cacheData[org][model]
	else:
		false
