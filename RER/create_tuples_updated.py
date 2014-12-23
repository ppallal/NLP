import json

fpAllData = open("all_data.json","r")

data_list = json.loads(fpAllData.read())['root']
final = []
sents = []
tags = []

tag = []
word = []
tag_final = []
word_final = []


for data in data_list: 
	data1 = data['data']
	for rec in data1:
		

		updates = rec['updates']
		for i in updates:		
			tag.append(i["tag"])
			word.append(i["word"])


		updates = rec['updates']
		sent = rec['sentence']
		if("rels" not in rec): continue		
		tags = rec['rels']
		if(tags):		
			sents.append(sent)
			sents.append(tags[0].keys()[0])		
			sents.append(tags[0].values()[0])
			sents.append(tag)
			sents.append(word)		
		#print sents
		if(not sents) : continue
		
		final.append(sents)
		sents = []
		tag = []
		word = []
	
for i in final:
	print i
	break
