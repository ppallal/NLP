import build_history
import json

fpAllData = open("all_data.json","r")

data = json.loads(fpAllData.read())['root']

#print data

(history_list,sents,expected,) = build_history.build_history(data,["Org","Family","OS","Version","Price","Phone","Feature","Other"])

#print history_list
i=0
while i<(len(history_list)):

	#print json.dumps(i[0]) ,"\t->\t ",i[1]
	print history_list[i][1]+"\t",
	i+=1
	while(history_list[i][0]["i"]!=0):
		print history_list[i][1]+"\t",
		i+=1
	print


#print i
#break

fpAllData.close()