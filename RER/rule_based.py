#from nltk.stem.porter import *

def max_in_dict(dic):
    maxx = max(dic.values())
    keys = [x for x,y in dic.items() if y ==maxx] 
    return keys[0] if len(keys)==1 else keys

def RuleBased(sentence): #sentence -> String

	sentence = str(sentence.lower())
	#stemmer
	#stemmer = PorterStemmer()

	#variables
	posibilities = {'disagreement': 0, 'greeting': 0, 'agreement': 0, 'acknowledgement':0} #'price_query': 0, 'feature_query': 0, 'comparison': 0, 'interest_intent': 0, 'irrelevant': 0, 
	relation_list = ['price_query', 'feature_query', 'comparison', 'interest_intent', 'irrelevant', 'disagreement', 'greeting', 'agreement', 'acknowledgement']
	sentenceString = " ".join(sentence)

	#rules

	#check if price

	#check if "how much" is there
	# for (i in [stemmer.stem(j) for j in ['how','much','affordable','less','than','discount','money']])
	# 		if(i in [stemmer.stem(k.lower()) for k in sentence]):
	# 			posibilities['price_query'] == 0.8
	# 			break

	#check if feature

	# for (i in [stemmer.stem(j) for j in ['how','much','affordable','less','than','discount','money']])
	# 		if(i in [stemmer.stem(k.lower()) for k in sentence]):
	# 			posibilities['price_query'] == 0.8
	# 			break

	#check if comparison
	#check if interest
	#check if irrelevant
	#check if disagreement
	temp = ['not','dont','problem','inconvenient','wrong']
	for i in temp:
		if(i in sentence):
			posibilities['disagreement'] = 0.9
			break

	#check if greeting

	temp = ['hi','hey','how are you','great day','weather','holiday','thank you']
	for i in temp:
		print i
		if i in sentence:
			posibilities['greeting'] = 0.8
			break

	#check if agreement

	temp = ['good','i like','correct']
	for i in temp:
		if i in sentence:
			posibilities['agreement'] = 0.8
			break

	if(posibilities['agreement']==0):
		if 'is' in sentence:
			posibilities['agreement'] = 0.2

	#check if acknowledgement

	temp = ['has','is']
	for i in temp:
		if(i in sentence):
			posibilities['acknowledgement'] = 0.4
			break

	#print posibilities
	return max_in_dict(posibilities)