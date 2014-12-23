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
from ner_client import *
from nltk.corpus import stopwords

supported_tags_list = ["Org",""]
phones = ["phone", "phones", "smartphone", "smartphones", "mobile", "tablet", "tablets", "phablet", "phablets"]
org_list = ['Samsung', 'Apple', 'Microsoft', 'Nokia', 'Sony', 'LG', 'HTC', 'Motorola', 'Huawei', 'Lenovo', 'Xiaomi', 'Acer', 'Asus', 'BlackBerry',
            'Alcatel', 'ZTE', 'Toshiba', 'Vodafone', 'T-Mobile', 'Gigabyte', 'Pantech', 'XOLO', 'Lava', 'Micromax', 'BLU', 'Spice', 'Prestigio',
            'verykool', 'Maxwest', 'Celkon', 'Gionee', 'vivo', 'NIU', 'Yezz', 'Parla', 'Plum']
org_list1 = [m.lower() for m in org_list]
os_list = ["iOS", "Android", "Windows", "Symbian", "Bada", "Unix", "Linux", "Ubuntu", "OS", "RIM", "Firefox"]
os_list1 = [m.lower() for m in os_list]
currency_symbols = ["rs", "inr", "$", "usd", "cents", "rupees"]
size_list = ["inch", "cm", "inches", "cms", r'"', "''", "pixel", "px", "mega", "gb", "mb", "kb", "kilo", "giga", "mega-pixel" ]
family_list = ["galaxy","lumia","canvas","iphone","nexus","moto"]


ner = NerClient("1PI11CS116","G3")
#print ner.get_brand_product_bigrams_dict()

brand_product_bigrams_dict = [] # use the web service from Ner_client to get this: ner.get_brand_product_bigrams() # gazeteer based 7th Dec 2014
product_names = []
for v in json.loads(ner.get_brand_product_bigrams_dict()).values():
    for v1 in v:
        product_names.append(v1.lower())

product_name_tokens = [] # some time product names may be strings with many words, we will split these so that we can compare it with input word token
for p in product_names:
    product_name_tokens.extend(p.split())


class FeatureFunctions(object):
    def __init__(self, tag_list = None):
        self.wmap = {}
        self.flist = {} #[self.f1, self.f2, self.f3, self.f4, self.f5, self.f6, self.f7, self.f8, self.f9, self.f10, self.f11, self.f12, self.f13]
        self.fdict = {}
        for k, v in FeatureFunctions.__dict__.items():
            if hasattr(v, "__call__"):
                if k[0] == 'f':
                    self.flist[k] = v # .append(v)
                    tag = k[1:].split("_")[0]
                    val = self.fdict.get(tag, [])
                    val.append(v)
                    self.fdict[tag] = val

        self.supported_tags = self.fdict.keys()        
        return

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

    def evaluate(self, xi, tag):
        feats = []
        for t, f in self.fdict.items():
            if t == tag:
                for f1 in f:
                    feats.append(int(f1(self, xi, tag)))
            else:
                for f1 in f:
                    feats.append(0)
        return feats
    #------------------------------- Phone tag ---------------------------------------------------------
    # The following is an example for you to code your own functions
    # returns True if wi is in phones tag = Phone
    # h is of the form {'ta':xx, 'tb':xx, 'wn':xx, 'i':xx}
    # self.wmap provides a list of sentences (tokens) where each element in the list is a dict {'words': word_token_list, 'pos_tags': pos_tags_list}
    # each pos_tag is a tuple returned by NLTK tagger: (word, tag)
    # h[3] refers to a sentence number
   
    def fPhone_1(self, h, tag):
        if tag != "Phone":
            return 0
	print h
	if(type(h[0])==type((1,2))):
		h = h[0]
	print h
        words = self.wmap[h[2]]['words']        
        if (words[h[3]].lower() in phones):
            return 1
        else:
            return 0

    #------------------------------- Functions for Org tag ---------------------------------------------------------
    
    
	def fOrg_1(self, h, tag):
		if tag != "Org":
            		return 0
		if(type(h[0])==type((2,3))):
			h = h[0]
       		words = self.wmap[h[3]]['words']        
		if (words[h[2]].lower() in org_list1):
		    return 1
		else:
		    return 0

	def fOrg_2(self, h, tag):
		if(type(h[0])==type((2,3))):
			h = h[0]

		if(h[1]=="Version" or h[1] == "OS" and tag == "Org"):
			return 0
		return 1;
	
	def fOrg_3(self, h, tag):
		if(type(h[0])==type((2,3))):
			h = h[0]

		if(h[1]=="feature" and tag == "Org"):
			return 0
		return 1;
	
	def fOrg_4(self, h, tag):
		if(type(h[0])==type((2,3))):
			h = h[0]

		p = re.compile('\d+(\.\d+)?')
		words = self.wmap[h[3]]['words']
		a = words[h[2]].lower()
		if (p.match(a) and tag == "Org"):
			return 0
		return 1
	
	
	
	#------------------------------- Functions for Family tag ---------------------------------------------------------  
	def fFamily_1(self, h, tag):
		if(type(h[0])==type((2,3))):
			h = h[0]

		if(h[1]=="Phone" and tag == "family"):
			return 1
		return 0
	
	def fFamily_2(self, h, tag):
		if(type(h[0])==type((2,3))):
			h = h[0]

		if(h[0] == "Org" and h[1]=="Other" and tag == "family"):
			return 1;
		return 0;
		
	def fFamily_3(self, h, tag):
		if(type(h[0])==type((2,3))):
			h = h[0]

		if tag != "Family":
			return 0
        	words = self.wmap[h[3]]['words']        
		if (words[h[2]].lower() in family_list):
		    return 1
		else:
		    return 0

	def fFamily_4(self, h, tag):
		if(type(h[0])==type((2,3))):
			h = h[0]

		p = re.compile('\d+(\.\d+)?')
		words = self.wmap[h[3]]['words']
		a = words[h[2]].lower()
		if (p.match(a) and tag == "family"):
			return 0;
		return 1;
	
	def fFamily_5(self, h, tag):
		if(type(h[0])==type((2,3))):
			h = h[0]

		if(h[1]=="Version" and tag == "family"):
			return 0;
		return 1;
	
	def fFamily_6(self, h, tag):
		if(type(h[0])==type((2,3))):
			h = h[0]

		if(h[1]=="feature" and tag == "family"):
			return 0;
		return 1;
	
	
	#------------------------------- Functions for OS tag ---------------------------------------------------------     

    def fOS_1(self, h, tag):
       if(type(h[0])==type((2,3))):
           h = h[0]
       if tag != "OS":
           return 0
       words = self.wmap[h[2]]['words']        
       if (words[h[3]].lower() in os_list):
           return 1
       else:
           return 0
      
    
    def fOS_2(self, h, tag):
       if(type(h[0])==type((2,3))):
           h = h[0]

       if tag != "OS":
           return 0
       #words = self.wmap[h[2]]['words']        
       if (h[0]=="Version"  and  h[1]=="Other"):
           return 1
       else:
           return 0

    def fOS_3(self, h, tag):
       if(type(h[0])==type((2,3))):
           h = h[0]

       if tag != "OS":
           return 0
       #words = self.wmap[h[2]]['words']        
       if (h[0]=="Phone"  and  h[1]=="Other"):
           return 1
       else:
           return 0

    def fOS_4(self, h, tag):
       if(type(h[0])==type((2,3))):
           h = h[0]

       if tag != "OS":
           return 0
       #words = self.wmap[h[2]]['words']        
       if (h[3]==0):
           return 1
       else:
           return 0

    def fOS_5(self, h, tag):
       if(type(h[0])==type((2,3))):
           h = h[0]

       if tag != "OS":
           return 0
       #words = self.wmap[h[2]]['words']        
       if (h[3]==1  and  h[1]=="Other"):
           return 1
       else:
           return 0

    def fOS_6(self, h, tag):
       if(type(h[0])==type((2,3))):
           h = h[0]

       if tag != "OS":
           return 0
       #words = self.wmap[h[2]]['words']        
       if (h[3]>8):
           return 0
       else:
           return 1


   
    #------------------------------- Functions for Version tag ---------------------------------------------------------
    def fVersion_1(self, h, tag):
		if(type(h[0])==type((2,3))):
			h = h[0]

		if(h[1]=="OS" and tag == "Version"):
			return 1
		return 0
		
    

    
    def fVersion_2(self, h, tag):
		if(type(h[0])==type((2,3))):
			h = h[0]

		if(h[1]=="Phone" and tag == "Version"):
			return 1
		return 0
		
 
       
   
    def fVersion_3(self, h, tag):
		if(type(h[0])==type((2,3))):
			h = h[0]

		if(h[0] == "Org" and h[1]=="Phone" and tag == "Version"):
			return 1
		return 0
		
       

    
    def fVersion_4(self, h, tag):
		if(type(h[0])==type((2,3))):
			h = h[0]

		if(h[1]=="Other" and tag == "Version"):
			return 0
		return 1
		
        
    def fVersion_7(self, h, tag):
		if(type(h[0])==type((2,3))):
			h = h[0]

		if(h[1]=="Family" and tag == "Version"):
			return 1
		return 0

  
    def fVersion_5(self, h, tag):
		if(type(h[0])==type((2,3))):
			h = h[0]

		if(h[0] == "Org" and h[1]=="family" and tag == "Version"):
			return 1
		return 0
		
    
    def fVersion_6(self, h, tag):
		if(type(h[0])==type((2,3))):
			h = h[0]

		p = re.compile('\d+(\.\d+)?')
		words = self.wmap[h[2]]['words']
		a = words[h[3]].lower()
		if (p.match(a) and tag == "Version"):
			return 0
		return 1
	
	
	#------------------------------- Functions for Other tag ---------------------------------------------------------
    def fOther_1(self, h, tag): #Feature Feature
	if(type(h[0])==type((2,3))):
			h = h[0]
	
    	if tag != "Other":
            return 0
	if(h[0]=="Version"):
		return 1
	else:
		return 0

    def fOther_2(self, h, tag): #Feature Feature
	if(type(h[0])==type((2,3))):
		h = h[0]

    	if tag != "Other":
            return 0
        stop = stopwords.words('english')
	words = self.wmap[h[2]]['words']
	if(words[h[3]].lower() in stop):
		return 1
	return 0

    def fOther_3(self, h, tag): # if the last 2 tags were features
		if(type(h[0])==type((2,3))):
			h = h[0]
	
		if tag != "Other":
			return 0
		if(h[0]=="Other" and h[1]=="Other"):
			return 1
		else:
			return 0



    #------------------------------- Functions for Price tag ---------------------------------------------------------  
    def fPrice_1(self, h, tag):
       if(type(h[0])==type((2,3))):
           h = h[0]

       if tag != "Price":
           return 0
       #words = self.wmap[h[2]]['words']        
       if (h[3]>=3):
           return 1
       else:
           return 0

    def fPrice_2(self, h, tag):
       if(type(h[0])==type((2,3))):
           h = h[0]

       if tag != "Price":
           return 0
       #words = self.wmap[h[2]]['words']        
       if (h[1]=="Price"):
           return 1
       else:
           return 0

    def fPrice_3(self, h, tag):
       if(type(h[0])==type((2,3))):
           h = h[0]

       if tag != "Price":
           return 0
       #words = self.wmap[h[2]]['words']        
       if (h[1]=="Price"):
           return 1
       else:
           return 0

    def fPrice_4(self, h, tag):
       if(type(h[0])==type((2,3))):
           h = h[0]

       if tag != "Price":
           return 0
       #words = self.wmap[h[2]]['words']        
       if (h[0]=="Phone" and h[1]=="Other"):
           return 1
       else:
           return 0

    def fPrice_5(self, h, tag):
       if(type(h[0])==type((2,3))):
           h = h[0]

       if tag != "Price":
           return 0
       words = self.wmap[h[2]]['words']        
       if (words[h[3]].isdigit()):
           return 1
       else:
           return 0


    def fPrice_6(self, h, tag):
       if(type(h[0])==type((2,3))):
           h = h[0]

       if tag != "Price":
           return 0
       #words = self.wmap[h[2]]['words']        
       if (h[0]=="Version" and h[1]=="Other"):
           return 1
       else:
           return 0

    def fPrice_7(self, h, tag): # checking for Other Price
	if(type(h[0])==type((2,3))):
           h = h[0]

	if tag != "Price":
		return 0
	if(h[0]=="Other"):
		return 1
	return 0

	def fPrice_8(self, h, tag): # checking for Price Price
		if(type(h[0])==type((2,3))):
	           h = h[0]
	
		if tag != "Price":
			return 0
		if(h[0]=="Price"  and  h[1]=="Price"):
			return 1
		return 0

	def fPrice_9(self, h, tag): # if its a number
       		if(type(h[0])==type((2,3))):
        	   h = h[0]

		if tag != "Price":
			return 0
		p = re.compile('\d+(\.\d+)?')
		words = self.wmap[h[2]]['words']
		a = words[h[3]].lower()
		if (p.match(a)):
			return 1
		return 0

	def fPrice_10(self, h, tag): # checking its a number and the previous one is Price
		if(type(h[0])==type((2,3))):
        	   h = h[0]
	
		if tag != "Price":
			return 0
		p = re.compile('\d+(\.\d+)?')
		words = self.wmap[h[2]]['words']
		a = words[h[3]].lower()
		if (p.match(a)  and  h[0] == "Price"):
			return 1
		return 0

	def fPrice_11(self, h, tag): # if its currency
		if(type(h[0])==type((2,3))):
	           h = h[0]
	
		if tag != "Price":
			return 0
		words = self.wmap[h[2]]['words']
		if(words[h[3]].lower() in currency_symbols):
			return 1
		return 0

	def fPrice_12(self, h, tag): # if current 
		if(type(h[0])==type((2,3))):
	           h = h[0]

		if tag != "Price":
			return 0
		words = self.wmap[h[2]]['words']
		if(h[3] < len(words)-1):
			if(any(char.isdigit() for char in words[h[3]].lower())  and  (words[h[3]+1].lower() in currency_symbols)):
				return 1
		return 0


    #------------------------------- Functions for Size tag ---------------------------------------------------------  


    #------------------------------- Functions for Feature tag ---------------------------------------------------------  

    def fFeature_1(self, h, tag): #Feature Feature
	if(type(h[0])==type((2,3))):
           h = h[0]

    	if tag != "Feature":
            return 0
	if(h[0]=="Feature"):
		return 1
	else:
		return 0

	def fFeature_2(self, h, tag): # if the last 2 tags were features
		if(type(h[0])==type((2,3))):
	           h = h[0]

		if tag != "Feature":
			return 0
		if(h[0]=="Feature"  and  h[1]=="Feature"):
			return 1
		else:
			return 0

	def fFeature_3(self, h, tag): # if next word is inch, cms, etc.
		if(type(h[0])==type((2,3))):
	           h = h[0]

		if tag != "Feature":
			return 0
		words = self.wmap[h[2]]['words']
		if(h[3] < len(words)-1):
			if(words[h[3]].lower() in size_list):
				return 1
		return 0

	def fFeature_4(self, h ,tag): # if it's a number
		if(type(h[0])==type((2,3))):
	           h = h[0]

		if tag != "Feature":
			return 0
		words = self.wmap[h[2]]['words']
		if(any(char.isdigit() for char in words[h[3]].lower())):
			return 1
		return 0





if __name__ == "__main__":
    pass
