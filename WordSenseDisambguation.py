from __future__ import division
import string
from Tkinter import *
from sets import Set
import networkx as nx
import pylab as plt
import math
import nltk
import operator
from networkx.drawing.nx_agraph import graphviz_layout
from nltk.corpus import wordnet as wn
from itertools import combinations


top = Tk()
str = StringVar()
inputValue=[]
def cop():
    global inputValue
    inputValue=input1.get("1.0","end-1c")
    print (inputValue)    
'''
label1 = Label(top, text="Enter the text string",bg="red",width="40")
label1.pack(side=LEFT)
input1 = Text(top,bd=5,height="1")
input1.pack()
button1 = Button(top,text="Run", highlightcolor="blue",width="40",command=lambda:cop())
button1.pack(side = BOTTOM)
# print (str)
top.mainloop()
'''





def isPunct(word):
  return len(word) == 1 and word in string.punctuation

def isNumeric(word):
  try:
    float(word) if '.' in word else int(word)
    return True
  except ValueError:
    return False

class RakeKeywordExtractor:

  def __init__(self):
    self.stopwords = set(nltk.corpus.stopwords.words())
    self.top_fraction = 1 # consider top third candidate keywords by score

  def _generate_candidate_keywords(self, sentences):
    phrase_list = []
    for sentence in sentences:
      words = map(lambda x: "|" if x in self.stopwords else x,
        nltk.word_tokenize(sentence.lower()))
      phrase = []
      for word in words:
        if word == "|" or isPunct(word):
          if len(phrase) > 0:
            phrase_list.append(phrase)
            phrase = []
        else:
          phrase.append(word)
    return phrase_list

  def _calculate_word_scores(self, phrase_list):
    word_freq = nltk.FreqDist()
    word_degree = nltk.FreqDist()
    for phrase in phrase_list:
      degree = len(filter(lambda x: not isNumeric(x), phrase)) - 1
      for word in phrase:
        word_freq[word]+=1
        word_degree[word]+=degree # other words
    for word in word_freq.keys():
      word_degree[word] = word_degree[word] + word_freq[word] # itself
    # word score = deg(w) / freq(w)
    word_scores = {}
    for word in word_freq.keys():
      word_scores[word] = word_degree[word] / word_freq[word]
    return word_scores

  def _calculate_phrase_scores(self, phrase_list, word_scores):
    phrase_scores = {}
    for phrase in phrase_list:
      phrase_score = 0
      for word in phrase:
        phrase_score += word_scores[word]
      phrase_scores[" ".join(phrase)] = phrase_score
    return phrase_scores
    
  def extract(self, text, incl_scores=False):
    sentences = nltk.sent_tokenize(text)
    phrase_list = self._generate_candidate_keywords(sentences)
    word_scores = self._calculate_word_scores(phrase_list)
    phrase_scores = self._calculate_phrase_scores(
      phrase_list, word_scores)
    sorted_phrase_scores = sorted(phrase_scores.iteritems(),
      key=operator.itemgetter(1), reverse=True)
    n_phrases = len(sorted_phrase_scores)
    if incl_scores:
      return sorted_phrase_scores[0:int(n_phrases/self.top_fraction)]
    else:
      return map(lambda x: x[0],
        sorted_phrase_scores[0:int(n_phrases/self.top_fraction)])



def pairwise(it):
    it = iter(it)
    while True:
        yield next(it), next(it)

def djikstra(graph,x,y):
	if nx.has_path(graph,x,y):
		return nx.shortest_path_length(graph,x,y,1)
	else:
		return graph.number_of_nodes()

senses=[]
graph = nx.DiGraph()

def myfunction(a,b):
	global senses
	global graph
	drink=wn.synsets(a)
	milk=wn.synsets(b)
	print "First Sysnet"
	print drink

	print "Second Synset"
	print milk

	hyp=lambda s:s.hypernyms()
	hypo=lambda s:s.hyponyms()
	graph = nx.DiGraph()


	drink=Set(drink)
	milk=Set(milk)
	drinknames=[]
	milknames=[]
	for x in drink:
		drinknames.append(x.name())

	for x in milk:
		milknames.append(x.name())

	drinkdict={}
	milkdict={}

	senses=milk

	log=drink

	for x in senses:
		log.add(x)

	seen=Set()


	for x in drink:   
		graph.add_node(x.name())

	for x in milk:
		graph.add_node(x.name())




	def func(abc,x):
		global senses
		global graph
		if(len(abc)>=4):
			return
		else:


			for i in x:
				tempelementsyet=Set(abc)
				tempelementsyet.add(i)
				if(i in abc):
					continue
				elif(i in senses):
					print "Found a path:"
					print abc ,i
					print "\n"
					abc.add(i)
					for m in abc:
						graph.add_node(m.name())
						#print m.lemma_names()
					for a in (abc):
						for b in (abc):
							graph.add_edge(a.name(),b.name())
					senses.update(abc)
					continue
				elif(i in seen):
					continue
				else:
					seen.add(i)
					hypo1=i.hyponyms()
					hype1=i.hypernyms()
					abc1=i.closure(hyp,depth=2)
					defg1=i.closure(hypo,depth=2)
					
					func(tempelementsyet,hypo1)
					func(tempelementsyet,hype1)
					#func(tempelementsyet,abc1)
					#func(elementsyet,defg1)
					

					







	for x in drink:
		hype=x.hypernyms()
		hypo=x.hyponyms()
		abc=x.closure(hyp,depth=2)
		defg=x.closure(hypo,depth=2)

		elementsyet=Set([x])
		seen.add(x)
		
		func(elementsyet,hypo)
		func(elementsyet,hype)
		#func(elementsyet,abc)
		#func(elementsyet,defg)
		
		

	nx.draw(graph, with_labels=True,pos=graphviz_layout(graph), node_size=800, cmap=plt.cm.Blues,
	        node_color=range(len(graph)),arrows=False,edge_color='black',style='dashed',
	        prog='dot',label='val')


	#TOCode:- Djikstra Algorithm  to find shortest length in pytho n 



	def calcdegree(hx):
		dict={}
		for x in hx:
			dict[x]=graph.degree(x)

		return dict

	def entropy(degree):
		sum=0.0
		for x in degree:
			degree[x]=float(float(degree[x])/float(graph.number_of_edges()))
			if degree[x]!=0.0:
				degree[x]=float(degree[x])*float(math.log(degree[x]))
			else:
				degree[x]=0
			sum=sum+degree[x]
			sum=sum*-1
			sum=sum/float(math.log(graph.number_of_nodes()))

		return sum


	dict=nx.degree_centrality(graph)
	print ("\nDegree Centrality\n")
	drinkval=0
	milkval=0
	drinkname="null"
	milkname="null"
	for i in dict:
	    print i, dict[i]
	    if i in drinknames:
	    	if dict[i]>=drinkval:
	    		drinkval=dict[i]
	    		drinkname=i
	    if i in milknames:
	    	if dict[i]>=milkval:
	    		milkval=dict[i]
	    		milkname=i


	if drinkname in drinkdict:
		drinkdict[drinkname]+=1
	else:
		drinkdict[drinkname]=1

	if milkname in milkdict:
		milkdict[milkname]+=1
	else:
		milkdict[milkname]=1

	drinkval=0
	milkval=0
	drinkname="null"
	milkname="null"

	print("\nBetweeeness\n")
	dict=nx.betweenness_centrality(graph,normalized=True)

	for i in dict:
	    print i, dict[i]
	    if i in drinknames:
	    	if dict[i]>=drinkval:
	    		drinkval=dict[i]
	    		drinkname=i
	    if i in milknames:
	    	if dict[i]>=milkval:
	    		milkval=dict[i]
	    		milkname=i


	if drinkname in drinkdict:
		drinkdict[drinkname]+=1
	else:
		drinkdict[drinkname]=1

	if milkname in milkdict:
		milkdict[milkname]+=1
	else:
		milkdict[milkname]=1

	drinkval=0
	milkval=0
	drinkname="null"
	milkname="null"


	print("\nHits\n")
	hx,a=nx.hits(graph)

	for i in hx:
	    print i, hx[i]
	    print i, hx[i]
	    if i in drinknames:
	    	if dict[i]>=drinkval:
	    		drinkval=dict[i]
	    		drinkname=i
	    if i in milknames:
	    	if dict[i]>=milkval:
	    		milkval=dict[i]
	    		milkname=i
	if drinkname in drinkdict:
		drinkdict[drinkname]+=1
	else:
		drinkdict[drinkname]=1

	if milkname in milkdict:
		milkdict[milkname]+=1
	else:
		milkdict[milkname]=1

	drinkval=0
	milkval=0
	drinkname="null"
	milkname="null"

	print("\nPagerank\n")
	dict=nx.pagerank(graph)
	for i in dict:
	    print i, dict[i]
	    if i in drinknames:
	    	if dict[i]>=drinkval:
	    		drinkval=dict[i]
	    		drinkname=i
	    if i in milknames:
	    	if dict[i]>=milkval:
	    		milkval=dict[i]
	    		milkname=i


	if drinkname in drinkdict:
		drinkdict[drinkname]+=1
	else:
		drinkdict[drinkname]=1

	if milkname in milkdict:
		milkdict[milkname]+=1
	else:
		milkdict[milkname]=1

	


	drinkval=0
	milkval=0
	drinkname="null"
	milkname="null"

	print("\nCloseness\n")

	hx=nx.closeness_centrality(graph)
	dict=hx
	for i in hx:
	    print i, hx[i]
	    if i in drinknames:
	    	if dict[i]>=drinkval:
	    		drinkval=dict[i]
	    		drinkname=i
	    if i in milknames:
	    	if dict[i]>=milkval:
	    		milkval=dict[i]
	    		milkname=i


	if drinkname in drinkdict:
		drinkdict[drinkname]+=1
	else:
		drinkdict[drinkname]=1

	if milkname in milkdict:
		milkdict[milkname]+=1
	else:
		milkdict[milkname]=1


	print "\n\nThe final meanings are:-"
	print milkdict , drinkdict

	print("\nGLOBAL MEASURES\n")

	degree=calcdegree(hx)
	print("\nEntropy")
	allentropy=entropy(degree)
	print allentropy


	edgedensity=nx.density(graph)
	print("\nEdge Density")
	print edgedensity


	totalsum=0
	for x in graph.nodes():
		for y in graph.nodes():
			val=djikstra(graph,x,y)
			totalsum=totalsum+val

	print("\nCompactness")
	max=graph.number_of_nodes()*graph.number_of_nodes()*(graph.number_of_nodes()-1)
	min=graph.number_of_nodes()*(graph.number_of_nodes()-1)
	compactness=float(max-totalsum)/float(max- min )
	print compactness

	plt.show()
	#print senses
	sorteddrink=sorted(drinkdict.items(),key=operator.itemgetter(1))
	sortedmilk=sorted(milkdict.items(),key=operator.itemgetter(1))
	return sorteddrink[0][0],sortedmilk[0][0]
	 

def test():
	'''
  rake = RakeKeywordExtractor()
  keywords = rake.extract(inputValue, incl_scores=True)
  print (keywords)
  allkeys=[]
  
  for x in keywords:
  	allkeys.append(x[0])

  
  x=list(combinations(allkeys, 2))
  for i in x:
  	print i[0],i[1]
	a,b=myfunction(i[0],i[1])
	print a ,b
  '''
if __name__ == "__main__":
  test()			