from rermymaxent import *
from rules import *

def getFull(sentance,tags):
	m = getRelation(sentance,tags)
	r = RuleBased(sentance)

	if m==r[0]:
		return m
	elif (m=="feature_query" or m=="comparison" or m=="price_query"):
		return m
	elif (r[1]>=0.8):
		return r[0]
	elif (m == "irrelevant" and r[1]>=0.3):
		return r[0]
	else:
		return m
		
