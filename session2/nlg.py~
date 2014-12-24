#nlg.py
import senddat



def generate(relation,sentace,tags,chukkaret):
	if(relation == "comparison"):


		org = []
		version = []

		#comparing phones with generic features
		#comparing phones a specific feature
		for i in range(0,len(tags)):
			tag = tags[i][0]
			word = tags[i][1]
			mylen = 0
			#print tag, " tw ", word
			if tag == 'Org':
				org.append(word)
				mylen = len(version)
				for j in range(i+1,len(tags)):

					if tags[j][0] == 'Family' or tags[j][0] == 'Version':
						try:
							version[mylen]+= " " +tags[j][1]
						except Exception:
							#print tags[j][1]
							version.append(tags[j][1])
					else:
						mylen = len(version)
						#print mylen
						#version.append('')
						break




		tagkeys = map(lambda x:x[0],tags)
		if("Feature" in tagkeys):
			answer = [False,False]
			fi = tagkeys.index("Feature")
			feature = tags[fi][1]
			for i in chukkaret[0]:		
				if(feature in i):
					answer[0] = True 
			for i in chukkaret[1]:			
				if(feature in i):
					answer[1] = True 
			
			if(answer[0] and answer[1]):
				ans =" Both " + org[0] + " " + version [0] +" and "  + org[1] + " " + version [1] + " has " + feature 		
			elif(answer[0]):
				ans = org[0] + " " + version [0] +" has " + feature + " where as "  + org[1] + " " + version [1] + " does not " 
			elif(answer[1]):
				ans = org[1] + " " + version [1] +" has " + feature + " where as "  + org[0] + " " + version [0] + " does not " 
			else:
				ans =" Both " + org[0] + " " + version [0] +" and "  + org[1] + " " + version [1] + " does not have " + feature  
			#print feature		
			#for i in chukkaret:
			#	if()
			print ans
			return ans
		elif("Price" in tagkeys):
			pass
		else:
			answer = 


ret = senddat.send("compare Nokia Lumia 520 and Samsung P300 with respect to GPS")
#print ret
generate(ret["relation"],ret["sentance"],ret["tags"],ret["chukka"])
