from ner_client import *
import senddat

sentence = "Uh Samsung Galaxy Note T879 or Nokia Lumia 930 ?"

prafret = senddat.send(sentence)
print prafret
ner = NerClient("1PI11CS122", "G03")
#varaible
#indexChat = integer
#relation = string
#tags = [('tag1':'word1', 'tag2':'word2', 'tag3':'word3')]
#sentence = string.lower()

indexChat = 0
relation = str(prafret['relation'])
tags = prafret['tags']#[{'tag':'Other', 'word':'Uh'},{'tag':'Org', 'word':'Samsung'},{'tag':'Family', 'word':'Galaxy'},{'tag':'Version', 'word':'S3'},{'tag':'Other', 'word':'or'},{'tag':'Org', 'word':'Windows'},{'tag':'Family', 'word':'Lumia'},{'tag':'Version', 'word':'920'},{'tag':'Other', 'word':'?'}]


#greeting relation
if relation == "greeting":
	if indexChat == 0:
		print "Welcome to ShopLy. How may I assist you?"
	elif 'thank you' in sentence:
		print "Your welcome. Is there anything else I can help you with?"
	else:
		print "Is there anything else I can help you with?"

#comparison

if relation == "comparison":

	#comparing phones

	org = []
	version = []

	#comparing phones with generic features
	#comparing phones a specific feature
	for i in range(0,len(tags)):
		tag = tags[i][0]
		word = tags[i][1]
		mylen = 0
		print tag, " tw ", word
		if tag == 'Org':
			org.append(word)
			mylen = len(version)
			for j in range(i+1,len(tags)):

				if tags[j][0] == 'Family' or tags[j][0] == 'Version':
					try:
						version[mylen]+= " " +tags[j][1]
					except Exception:
						print tags[j][1]
						version.append(tags[j][1])
				else:
					mylen = len(version)
					print mylen
					#version.append('')
					break

				


		# elif tag == 'Family':
		# 	family.append(word)

		# elif tag == "Version":
		# 	version.append(word)

	# if (family[0] != ""):
	# 	version[0] = family[0]+" "+version[0]
	# elif (family[1] != ""):
	# 	version[1] = family[1]+" "+version[1]
	
	print org
	print version
	firstPhone = ner.get_spec(brand=org[0],product=version[0])

	secondPhone = ner.get_spec(brand=org[1],product=version[1])

	print firstPhone
	print secondPhone

	#comparing os

	# NOTE : Data insufficient

if relation == "feature_tag"

