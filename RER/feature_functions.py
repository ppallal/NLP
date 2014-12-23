'''
feature_functions.py
Implements the feature generation mechanism
Author: Anantharaman Narayana Iyer
Date: 21 Nov 2014

6th Dec: Org gazeteer added
7th Dec: 
'''
from nltk import sent_tokenize, word_tokenize
import nltk
import json
import numpy
import pickle
import datetime
import re
#from ner_client import *
from nltk.corpus import stopwords

supported_tags_list = ["Org",""]
phones = ["phone", "phones", "smartphone", "smartphones", "mobile", "tablet", "tablets", "phablet", "phablets"]
org_list = ['Samsung', 'Apple', 'Microsoft', 'Nokia', 'Sony', 'LG', 'HTC', 'Motorola', 'Huawei', 'Lenovo', 'Xiaomi', 'Acer', 'Asus', 'BlackBerry',
            'Alcatel', 'ZTE', 'Toshiba', 'Vodafone', 'T-Mobile', 'Gigabyte', 'Pantech', 'XOLO', 'Lava', 'Micromax', 'BLU', 'Spice', 'Prestigio',
            'verykool', 'Maxwest', 'Celkon', 'Gionee', 'vivo', 'NIU', 'Yezz', 'Parla', 'Plum']
org_list1 = [m.lower() for m in org_list]
os_list = ["iOS", "Android", "Windows", "Symbian", "Bada", "Unix", "Linux", "Ubuntu", "OS", "RIM", "Firefox"]
os_list1 = [m.lower() for m in os_list]
currency_symbols = ["rs", "inr", "$", "usd", "cents", "rupees","bucks","dollars"]
size_list = ["inch", "cm", "inches", "cms", r'"', "''", "pixel", "px", "mega", "gb", "mb", "kb", "kilo", "giga", "mega-pixel" ]
family_list = ["galaxy","lumia","canvas","iphone","nexus","moto"]


#ner = NerClient("1PI11CS116","G3")
#print ner.get_brand_product_bigrams_dict()
"""
brand_product_bigrams_dict = [] # use the web service from Ner_client to get this: ner.get_brand_product_bigrams() # gazeteer based 7th Dec 2014
product_names = []
for v in json.loads(ner.get_brand_product_bigrams_dict()).values():
    for v1 in v:
        product_names.append(v1.lower())

product_name_tokens = [] # some time product names may be strings with many words, we will split these so that we can compare it with input word token
for p in product_names:
    product_name_tokens.extend(p.split())
"""
#query_list = ['price_query', 'feature_query', 'comparison', 'interest_intent', 'irrelevant', 'disagreement', 'greeting', 'agreement', 'acknowledgement']

class FeatureFunctions(object):
    def __init__(self, tag_list = None, query_list = ['price_query', 'feature_query', 'comparison', 'interest_intent', 'irrelevant']):
        self.wmap = {} #word map
        self.flist = {} #[self.f1, self.f2, self.f3, self.f4, self.f5, self.f6, self.f7, self.f8, self.f9, self.f10, self.f11, self.f12, self.f13] #list of functions
        self.fdict = {}
        self.tag_list = tag_list
        self.query_list = query_list
        for k, v in FeatureFunctions.__dict__.items():
            if hasattr(v, "__call__"):
		#print "tag : ",v                
		if k[0] == 'f':
                    self.flist[k] = v # .append(v)
                    tag = k[1:].split("__")[0]
                 #   print "tag : ",tag
                    val = self.fdict.get(tag, [])
                    val.append(v)
                    self.fdict[tag] = val

        self.supported_tags = self.fdict.keys()        
        return

    #utilities for making features

    def set_wmap(self, sents): # given a list of words sets wmap
        for i in range(len(sents)):
            self.wmap[i] = {'words': sents[i], 'pos_tags': nltk.pos_tag(sents[i])}
        return

    def check_list(self, clist, w):
        #return 0
        w1 = w.lower()
        for cl in clist:
            if w1 in cl:
                return 1
        return 0

    
    #evaluates all the feature functions

    def evaluate(self, xi, tag):
        feats = []
	#print self.fdict.items()
        for t, f in self.fdict.items():
            if t == tag:
                for f1 in f:
                    feats.append(int(f1(self, xi, tag)))
            else:
                for f1 in f:
                    feats.append(0)
        return feats
    #------------------------------- Phone tag ---------------------------------------------------------
  

	
	#------------------------------- Functions for Price Query ---------------------------------------------------

    def fprice_query__1(self, data,relations_tags): #sentence -> Array, tags -> Array, relation -> String, relations_tags ->Array
		sentence = data[0].split(" ")
		tags = data[2]
		relation = data[1]

		#print "feature Price 1 callled"
		if(relations_tags != "price_query"):
			return 0
		if("Price" in tags):
			return 1
		else:
			return 0
	
    def fprice_query__2(self, data,relations_tags):
		sentence = data[0].split(" ")
		tags = data[2]
		relation = data[1]
				
		if(relations_tags != "price_query"):
			return 0
		for i in ['how','much','affordable','less','than','discount']:
			if(i in [k.lower() for k in sentence]):
				return 1
		else:
			return 0

	

    def fprice_query__3(self,data,relations_tags):
		# data = [sentence,relation,[tags]]
		
		if(relations_tags != "price_query"):
			return 0
		tags = data[2]
		#print tags
		if(sorted(tags) == sorted(["Phone","Price"])):
			#print "1 returned"
			return 1
		else:
			return 0

    def fprice_query__4(self,data,relations_tags):     # data = [sentence,relation,[tags]]
		if(relations_tags != "price_query"):
			return 0
		tags = data[2]
		if(sorted(tags) == sorted(["Org","Price"])):
			return 1
		else:
			return 0
	
    def fprice_query__5(self,data,relations_tags):     # data = [sentence,relation,[tags]]
		if(relations_tags != "price_query"):
			return 0
		tags = data[2]
		if(sorted(tags) == sorted(["Price"])):
			return 1
		else:
			return 0
    def fprice_query__6(self,data,relations_tags):     # data = [sentence,relation,[tags]]
		if(relations_tags != "price_query"):
			return 0
		tags = data[2]
		if(sorted(tags) == sorted(["Family","Price"])):
			return 1
		else:
			return 0
    def fprice_query__7(self,data,relations_tags):     # data = [sentence,relation,[tags]]
			
		if(relations_tags != "price_query"):
			return 0		
		p = re.compile('\d+[kK]')
	 	if (p.search(data[0])):
		#	print "retu"	 		
			return 1
	 	return 0	
	
	def fprice_query__8(self,data,relations_tags):     # data = [sentence,relation,[tags]]
		if(relations_tags != "price_query"):
			return 0
		tags = data[2]
		if(sorted(tags) == sorted(["Org","Price","Phone"])):
			return 1
		else:
			return 0
	

	#------------------------------- Functions for Feature Query -------------------------------------------------
	#------------------------------- Functions for Comparison ----------------------------------------------------
	#------------------------------- Functions for Interest Intent -----------------------------------------------
	'''Phone 	:	9
	Family-Version-Org 	:	6
	Org-Phone 	:	6
	Family-Org 	:	6
	Family-Version-Other 	:	5
	Version-Org 	:	5
	'''
	def finterest_intent__1(self,data,relations_tags):     # data = [sentence,relation,[tags]]
		if(relations_tags != "interest_intent"):
			return 0
		tags = data[2]
		if(sorted(tags) == sorted(["Phone"])):
			return 1
		else:
			return 0
	
	
	def finterest_intent__2(self,data,relations_tags):     # data = [sentence,relation,[tags]]
		if(relations_tags != "interest_intent"):
			return 0
		tags = data[2]
		if(sorted(tags) == sorted(["Family","Version","Org"])):
			return 1
		else:
			return 0
			
	def finterest_intent__3(self,data,relations_tags):     # data = [sentence,relation,[tags]]
		if(relations_tags != "interest_intent"):
			return 0
		tags = data[2]
		if(sorted(tags) == sorted(["Org","Phone"])):
			return 1
		else:
			return 0
			
	def finterest_intent__4(self,data,relations_tags):     # data = [sentence,relation,[tags]]
		if(relations_tags != "interest_intent"):
			return 0
		tags = data[2]
		if(sorted(tags) == sorted(["Family","Version"])):
			return 1
		else:
			return 0
			
	def finterest_intent__5(self,data,relations_tags):     # data = [sentence,relation,[tags]]
		if(relations_tags != "interest_intent"):
			return 0
		tags = data[2]
		if(sorted(tags) == sorted(["Family","Org"])):
			return 1
		else:
			return 0
			
	def finterest_intent__6(self,data,relations_tags):     # data = [sentence,relation,[tags]]
		if(relations_tags != "interest_intent"):
			return 0
		tags = data[2]
		if(sorted(tags) == sorted(["Version","Org"])):
			return 1
		else:
			return 0
			
	def fprice_query__7(self, data,relations_tags):
		sentence = data[0].split(" ")
		tags = data[2]
		relation = data[1]
				
		if(relations_tags != "price_query"):
			return 0
		for i in ['looking','looking','need','Show','like','would','interested','when','want']:
			if(i in [k.lower() for k in sentence]):
				return 1
		else:
			return 0

	
	
	
	#------------------------------- Functions for Irrelevant ----------------------------------------------------
	
	def firrelevant__8(self,data,relations_tags):     # data = [sentence,relation,[tags]]
		if(relations_tags != "irrelevant"):
			return 0
		tags = data[2]
		if(sorted(tags) == sorted(["Phone"]) or sorted(tags) == sorted(["OS","Version"]) or sorted(tags) == sorted(["Family","Version","Org"]) or sorted(tags) == sorted(["Family","Org"]) or sorted(tags) == sorted(["Phone","Org"]) or sorted(tags) == sorted(["OS"])):
			return 1
		else:
			return 0
	
	
	
if __name__ == "__main__":
    pass
