import json

dataMap = {}
def setDm(relName,value):

	for i in range(len(value)):
		try: 
			value.remove("Others")
		except ValueError:
			break
	
	value.sort()
	value = "-".join(value)
	global dataMap		
	if(relName in dataMap.keys()):
		if(value in dataMap[relName].keys()):
			dataMap[relName][value] += 1
		else:
			dataMap[relName][value] = 1
	else:
		dataMap[relName] = {}
		dataMap[relName][value] = 1


def processRel(rel):
	pass



def analyze(root):
	for i in root:
		for j in i['data']:
			if("rels" in j.keys() and j['rels']):
				rel = j["rels"][0]
				print rel
				key = rel.keys()[0]
				if(rel[key]):
					setDm(key,rel[key])

	

		
f = open("alldata.json")
data = json.loads(f.read())

analyze(data["root"])



for i in dataMap:
	print "-"*30
	print
	print i
	print
	keys = dataMap[i].keys() 
	#print dataMap[i].keys()
	keys.sort(key=lambda x:dataMap[i][x] ,reverse=True)
	for j in keys[0:10]:
		print "\t",j,"\t:\t",dataMap[i][j]
		
