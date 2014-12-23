#from nltk.stem.porter import *
import create_tuples
datast = create_tuples.getData()
def max_in_dict(dic):
    maxx = max(dic.values())
    #keys = [x for x,y in dic.items() if y ==maxx] 
    #return keys[0] if len(keys)==1 else keys
    for i in dic:
	if maxx == dic[i] : return i

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
	res = max_in_dict(posibilities)
	if res == posibilities:
		res = 0
	return res
	
	

posibilities2 = {'disagreement': 0, 'greeting': 0, 'agreement': 0, 'acknowledgement':0}
posibilities3 = {'disagreement': 0, 'greeting': 0, 'agreement': 0, 'acknowledgement':0}


for i in range(0,len(datast)):
	if(str(datast[i][1]) in posibilities2):
		#print datast[i][0]
		#print RuleBased(datast[i][0])
		#print RuleBased(str(datast[i][0])),"---",datast[i][1]
		if(RuleBased(str(datast[i][0])) == str(datast[i][1])):
						
			posibilities2[str(datast[i][1])]+=1
			#print posibilities2
		posibilities3[str(datast[i][1])]+=1
		#print "Pos ",posibilities3
		
sum = 0
sum2 = 0
for i in posibilities2:
	sum += posibilities2[i]
	sum2 += posibilities3[i]
	if(posibilities3[i] == 0):
		posibilities2[i] = 0
	else:
		posibilities2[i] /= float(posibilities3[i])

#print 2,posibilities2
#print 3,posibilities3
sum /= float(sum2)
		
f1 = {}
for i in posibilities2:
	if((sum+posibilities2[i]) == 0):
		f1[i] = 0
	else:
		f1[i] = (2*sum*posibilities2[i])/(sum+posibilities2[i])

#print posibilities2
	
print "precision : ",sum
#print "\t",sum
for i in posibilities2:
	print i,":\n"
	print "\trecall:\t",posibilities2[i]
	print "\tf1 score:\t",f1[i]
