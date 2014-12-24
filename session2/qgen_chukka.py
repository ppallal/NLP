from ner_client import *
#import senddat

dat = {'less' : ["less","under","within"] , 'more' : ["greater","above","more"] , 'between':["range","between"]}
dat1 = {'yes' : ["has","show","have"] , 'more' : ["greater","above","more"] , 'between':["range","between"]}
condition = ""
number = 0
feature_list = []




def filter_fun(datast):
	global condition
	global number
	global feature_list
	brands = []
	tags = datast['tags']
	i=0

	temp=[]
	version = ""

	for i in range(0,len(tags)):
		tag = tags[i][0]
		word = tags[i][1]
		mylen = 0
		if tag == 'Org':
			temp.append(word)
			for j in range(i+1,len(tags)):
				if tags[j][0] == 'Family' or tags[j][0] == 'Version':
						version+= " " +tags[j][1]
				else:
					break
	if version[0] == " ":
		version = version[1:]
	temp.append(version)
	print "temp ", temp
	i=0
	while (i < len(tags)):
		if(tags[i][0] == "Family" or tags[i][0] == "Version" or tags[i][0] == "Org"):
			i+=1
			continue
		if(tags[i][1] in dat['less']):
			condition = "less"
		if(tags[i][1] in dat['more']):
			condition = "more"
		if(tags[i][0] == "Price" ):
			number = tags[i][1]
		if(tags[i][0] == "Feature" ):
			feature_list.append(tags[i][1])
		i=i+1
	if(len(temp)>0):		
		brands.append(temp)
	if(len(brands) > 0):	
		print "brands" ,brands
		return brands


def priceQuery(datast):	
	list = filter_fun()
	global condition
	global number
	tags = datast['tags']
	p_price =0
	i = 0
	less = []
	more = []		
	final = []
	final1= [] 
	if(list):
		print("inside if")
		for i in list:
			if(len(i) > 1):
				final = ner1.get_products(i[0],i[1])
				p_price = final[0]['dummy_price']
			else:
				final = ner1.get_products(i[0])
		final1 = final
	else:
		print("inside else")
		temp = json.loads(ner1.get_brand_product_bigrams_dict())
		print temp
		count = 0
		for i in temp:
			print "i :",i
			for j in temp[i]:
				print "j :" ,j
				if(count<5):
					final.append(ner1.get_products(i,j))
				count+=1
		final1 = []
		for i in final:
			final1.append(i[0])
	for i in final1:
		if(i['dummy_price']<int(number)):
			less.append(i['brand']+" "+i['product']+"   "+str(i['dummy_price']))
		else:
			more.append(i['brand']+" "+i['product']+"   "+str(i['dummy_price']))
	
	if(condition == "less"):
		return less 
	elif(condition == "more"):
		return more
	else:
		return p_price



def featureQuery(datast):
	list = filter_fun()
	global feature_list
	final = []
	#final1= [] 
	print list,feature_list
	if(list):
		#print("inside if")
		for i in list:
			if(len(i) > 1):
				final = ner1.get_spec(i[0],i[1])
				specific = 1
				#p_price = final[0]['dummy_price']
			else:
				final = ner1.get_spec(i[0])
				specific = 0
		
	#print final # list of dictionary
	final1 = {}
	for i in feature_list:
		final2 = []
		for j in final:
			if(i.lower() == j['category'].lower()):
				final2.append((j['value'],j['product']))
				if(specific):
					break
		final1[i] = final2
	return final1



def get_features(ret):
	#ret = ner.get_spec(brand = "Samsung", product = "P300")    
	l = []
    	for i in ret:
    		for j in range(len(i)):
			l1 = []
			l2 = []
			l1.append(i['value'])
			l2.append(i['field'])
			l.append(l1)
			l.append(l2)
		
    	#l = set(l)	
    	x = []
   	for p in l:
		if p in x: continue	
		x.append(p)	
   	#for i in x:	
   	 #	print i	
   	#print ret[:5], len(ret)
	return x
   
    
def get_prices():
	ret = ner.get_products("Samsung")	
	l = []
	for i in ret:
	    	for j in range(len(i)):
			l1 = []
			l1.append(i['product'])
			l1.append(i['dummy_price'])
			l.append(l1)
		
		
	for p in ret:
		print p
		




def getChukkaResult(prafret,sentence):
	#sentence = "Uh Samsung Galaxy Note T879 or Nokia Lumia 930 ?"

	#prafret = senddat.send(sentence)
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
			return "Welcome to ShopLy. How may I assist you?"
		elif 'thank you' in sentence:
			return "Your welcome. Is there anything else I can help you with?"
		else:
			return "Is there anything else I can help you with?"

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

				


			# elif tag == 'Family':
			# 	family.append(word)

			# elif tag == "Version":
			# 	version.append(word)

		# if (family[0] != ""):
		# 	version[0] = family[0]+" "+version[0]
		# elif (family[1] != ""):
		# 	version[1] = family[1]+" "+version[1]
	
		#print org
		#print version
		firstPhone = ner.get_spec(brand=org[0],product=version[0])

		secondPhone = ner.get_spec(brand=org[1],product=version[1])

		return [get_features(firstPhone),get_features(secondPhone)]

		#comparing os

		# NOTE : Data insufficient

	elif relation == "feature_tag":
		return featureQuery(prafret)


	elif relation == "price_query":
		return priceQuery(prafret)


