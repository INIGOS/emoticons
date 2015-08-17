'''
Copyright 2015 Serendio Inc.
Author - Satish Palaniappan

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.
'''
__author__ = "Satish Palaniappan"


import pickle
import gensim
from scipy import spatial
import operator
import numpy as np

path = "./Model/Seeds22/"

def save_obj(obj, name ):
    with open( path + name + '.pkl', 'wb') as f:
        pickle.dump(obj, f,  protocol=2)

def load_obj(name ):
    with open( path + name + '.pkl', 'rb') as f:
        return pickle.load(f)

class Categorize(object):

	def __init__(self):

		## Load Pickle
		self.Cluster_lookUP = load_obj("Cluster_lookUP")
		self.Cosine_Similarity = load_obj("Cosine_Similarity")
		self.num2cat = load_obj("num2cat")
		self.Cluster_Model = load_obj("clusterSmall")
		self.catVec = load_obj("catVec")
		self.model = gensim.models.Word2Vec.load_word2vec_format(path + 'vectors.bin', binary=True)
		self.model.init_sims(replace=True)

	def CosSim (self,v1,v2):
		return (1 - spatial.distance.cosine(v1, v2))

	def combine(self,v1,v2):
		A = np.add(v1,v2)
		M = np.multiply(A,A)
		lent=0
		for i in M:
			lent+=i
		return np.divide(A,lent)

	def getCategory(self,text):
		# Min Score for Each Word
		wminScore = 0.30

		# sentScore =  []

		scores=dict()
		for i in range(0,22):
			scores[i] = 0.0

		for phrase in text:
			#phrase = phrase[0]
			if len(phrase.split()) == 1:
				try:
					skore = self.Cosine_Similarity[phrase]
					if skore > wminScore:
						scores[self.Cluster_lookUP[phrase]] += skore
						# comment later
						# sentScore.append((phrase,self.num2cat[self.Cluster_lookUP[phrase]],skore))
					#print(num2cat[Cluster_lookUP[phrase]])
				except:
					#print(phrase + " Skipped!")
					continue
			else:
				words = phrase.split()
				try:
					vec = np.array(model[words[0]])
					for word in words[1:]:
						try:
							vec = combine(vec,np.array(model[word]))
						except:
							#print(word + " Skipped!")
							continue
					tempCat = self.Cluster_Model.predict(vec)
					#print(num2cat[tempCat[0]])
					skore = CosSim(vec,self.catVec[tempCat[0]])
					if skore > wminScore:
						scores[tempCat[0]] += skore
						# sentScore.append((phrase,self.num2cat[tempCat[0]],skore))
				except:
					#print(words[0] + " Skipped!")
					continue

		thresholdP = 0.50  # This value is in percent
		# if u want a more finer prediction set threshold to 0.35 or 0.40 (caution: don't exceed 0.40)
		maxS = max(scores.items(), key = operator.itemgetter(1))[1]
		threshold = maxS * thresholdP

		#Min Score
		minScore = 0.40
		# if u want a more noise free prediction set threshold to 0.35 or 0.40 (caution: don't exceed 0.40)
		flag = 0
		if maxS < minScore:
			flag = 1
		# set max number of cats assignable to any text
		catLimit = 6  # change to 3 or less more aggresive model
		# more less the value more aggresive the model

		scoreSort  = sorted(scores.items(), key = operator.itemgetter(1), reverse=True)
		#print(scoreSort)
		cats = []
		f=0
		for s in scoreSort:
			if s[1] != 0.0 and s[1] > threshold:
				f=1
				cats.extend([self.num2cat[s[0]]])
			else:
				continue
		if f == 0 or flag == 1: #No Category assigned!
			return ("general")
		else:
			if len(cats) == 1:
				ret = str(cats[0])
			elif len(cats) <= catLimit:
				ret = "|".join(cats)
			else:
				# ret = "general" or return top most topic
				ret = cats[0] +"|"+"general"
			return [ret]
