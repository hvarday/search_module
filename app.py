#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
	req = request.get_json(silent=True, force=True)

	print("Request:")
	print(json.dumps(req, indent=4))

	res = makeWebhookResult(req)

	res = json.dumps(res, indent=4)
	print(res)
	r = make_response(res)
	r.headers['Content-Type'] = 'application/json'
	return r

def makeWebhookResult(req):
		
	import re
	url_dict=defaultdict(list)

	PFT='http://www.anirbansaha.com/parsi-fire-temple-kolkata-india/'
	query_list1=['Calcutta Walks','Iftekhar Ahsan','Parsi community in Kolkata','Parsi Fire Temple']

	for i in query_list1:
		i=i.lower()
		url_dict[i].append(PFT)

	Saga_dawa='http://www.anirbansaha.com/saga-dawa-gangtok-sikkim/'
	query_list2=['Buddhist festivals in Sikkim','Saga Dawa','Saga Dawa Gangtok','Saga Dawa Sikkim','Sikkim','Gangtok']

	for i in query_list2:
		i=i.lower()
		url_dict[i].append(Saga_dawa)

	Ravangla='http://www.anirbansaha.com/ravangla-geyzing-monastery-chham-photographs/'
	query_list3=['Geyzing','Hills','north east india','Pelling','Pemayangtse monastery','Rabdantse','Ralang monastery','Ravangla', 'Sikkim', 'Sikkim tourism', 'Simptham', 'Travel destinations','Travel to Sikkim from Kolkata']

	for i in query_list3:
		i=i.lower()
		url_dict[i].append(Ravangla)

	Cham='http://www.anirbansaha.com/kayged-festival-ralang-monastery-cham-dance-in-ralang-monastery-sikkim/'
	query_list4=[ 'Black hat dance', 'Buddhist custom', 'Cham', 'Cham dance costumes', 'Cham dance mask', 'Cham dance photographs', 'cham mask', 'chham dance', 'chham dance sikkim', 'chham festival', 'chham festival sikkim', 'Folk culture', 'Folk dance', 'Kaged festival', 'Kagyat festival', 'Karma Lama', 'Karmapa Mahakala Dance', 'Mahakala Dance', 'Masked Dances', 'Tibetan dance','Sikkim','Chaam','Chaam Dance']	

	for i in query_list4:
		i=i.lower()
		url_dict[i].append(Cham)

	paragliding='http://www.anirbansaha.com/paragliding-gangtok-sikkim/'
	query_list5=['Sikkim','Winter','Travel',"Gangtok",'Paragliding']

	for i in query_list5:
		i=i.lower()
		url_dict[i].append(paragliding)

	print(url_dict['sikkim'])

	model=defaultdict(lambda:1)

	def train(features):
		for f in features:
			model[f]+=1
		return model	

	all_words_list=[]

	for i in query_list1:
		i=i.lower()
		all_words_list.append(i)
	for i in query_list2:
		i=i.lower()
		all_words_list.append(i)
	for i in query_list3:
		i=i.lower()
		all_words_list.append(i)				
	for i in query_list4:
		i=i.lower()
		all_words_list.append(i)
	for i in query_list5:
		i=i.lower()
		all_words_list.append(i)

	NWORDS=train(all_words_list)						
	alphabet = 'abcdefghijklmnopqrstuvwxyz'

	def edits1(word):
		s = [(word[:i], word[i:]) for i in range(len(word) + 1)]
		deletes= [a + b[1:] for a, b in s if b]
		transposes = [a + b[1] + b[0] + b[2:] for a, b in s if len(b)>1]
		replaces= [a + c + b[1:] for a, b in s for c in alphabet if b]
		inserts   = [a + c + b     for a, b in s for c in alphabet]
		return set(deletes + transposes + replaces + inserts)


	def known_edits2(word):
		return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)

	def known_edits1(word):
		return set(e1 for e1 in edits1(word) if e1 in NWORDS)	

	def valid(item):
	dummy_set=set()
	if item in NWORDS:
		dummy_set.add(item)
		return dummy_set
	elif len(known_edits1(item))>0:
		return known_edits1(item) 	
	else:
		return known_edits2(item)	

	try:
		if req.get("result").get("action") == 'search_blog':
			result=req.get("result")
			parameters=result.get("parameters")
			if len(parameters.get("search_blog"))>0:
				any_list=parameters.get('any')

				init_set=set()
				temp_set=set()
				count=0
				for item in any_list:
					item=item.lower()
					items=valid(item)
					for item in items:
						for j in url_dict[item]:
							temp_set.add(j)
						if count==0:
							init_set=temp_set
						else:
							init_set=init_set&temp_set
					#print(init_set)
					count+=1	
					temp_set=set()	

				speech=""
				for i in init_set:
					speech=speech+i+"\n"	
						
				return {
					"speech": speech,
					"displayText": speech,
					"data": {},
					"contextOut": [],
					"source": "apiai-onlinestore-shipping"
				}
		else:
			return{}
			
				
	except Exception as error:
		#speech=str(error)
		speech="I am inside error module \n"
		print("Speech:"+'\t'+speech+'\t'+"flag:"+'\t'+str(flag))
		return {
			"speech": speech,
			"displayText": speech,
			#"data": {},
			# "contextOut": [],
			"source": "apiai-onlinestore-shipping"
		}

if __name__ == '__main__':
	port = int(os.getenv('PORT', 5000))

	print("Starting app on port %d" % port)

	app.run(debug=True, port=port, host='0.0.0.0')

