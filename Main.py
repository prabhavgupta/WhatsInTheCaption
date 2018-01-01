import WordSenseDisambguation
import pytumblr
import httplib, urllib, base64, urllib2, json
import requests
import json

def img_tag_category_call(link):
	print "\nFEATURES - TAGS AND CATEGORIES \n"
	headers = {
	'Content-Type': 'application/json',
	'Ocp-Apim-Subscription-Key': '3a39b0a8a4a14ce2b82f7688965a7a97',
	}


	try:
		url = '{ "url" : "' + link + '"}'
		conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
		conn.request("POST", "/vision/v1.0/describe?maxCandidates=1", url, headers)
		response = conn.getresponse()
		data = response.read()
		conn.close()
		return data
	except Exception as e:
		print("[Errno {0}] {1}".format(e.errno, e.strerror))
        
def search_ocr_call(query):
	print "\nQUERY SEARCH AND OCR API \n"
	headers = {
		'Content-Type': 'application/json',
		'Ocp-Apim-Subscription-Key': '6c41696fc79a4712a0a532cedf81d2be',
	}
	payload = {'q': query}
	r = requests.get('https://api.cognitive.microsoft.com/bing/v5.0/search', params=payload,headers=headers)
	print r.url
	return r.json()

client = pytumblr.TumblrRestClient('DaowyhPPqOeHzUX6Z8b1EFRD4bedEiuiNIXgEMq8q3tAWwA021')
link="http://ste.india.com/sites/default/files/2016/11/10/545426-travel-ts.jpg"
dict= img_tag_category_call(link)
data = json.loads(dict)
tags= data['description']['tags']
tags=tags[:5]
print tags
final_quotes=[]
for tag in tags:
    quote_data = client.tagged(tag+' quote', filter='text',limit=50)
    for x in quote_data:
        if (str(x['type']))=='quote':
            if( len(x['text']) <250):
            	final_quotes.append(x['text'])
            	print x['text']
            	print "------------------------------"
if len(final_quotes)>12:
	final_quotes=final_quotes[:11]
print json.dumps(final_quotes)