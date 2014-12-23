import json

fpAllData = open("alldata.json","r")

data_list = json.loads(fpAllData.read())['root']
final = []
sents = []

tags = []
for data in data_list: 
	data1 = data['data']
	for rec in data1:
		
		updates = rec['updates']
		sent = rec['sentence']
		if("rels" not in rec): continue		
		tags = rec['rels']
		if(tags):		
			sents.append(sent)
			sents.append(tags[0].keys()[0])		
			sents.append(tags[0].values()[0])
		#print sents
		if(not sents) : continue
		
		final.append(sents)
		sents = []
	
count = 0

# print final[0]
# exit()
for i in final:
	if(str(i[1]) == "acknowledgement"):
		print i[0]
		count+=1

print count
	
