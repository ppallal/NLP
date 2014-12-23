import json

f = open("all_data.json","r")
data = json.loads(f.read())


for i in data["root"]:
	for j in i["data"]:
		for k in j["updates"]:
			if(k["tag"]=="Model"):
				k["tag"]="Version"
			elif(k["tag"]=="Model"):
				k["tag"]="Version"
				
			elif(k["tag"]=="Model"):
				k["tag"]="Version"

print json.dumps(data)
