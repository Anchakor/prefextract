import base64
import os
import shutil
import cPickle as pickle

from nltk.corpus import wordnet as wn

import topia.termextract.extract
keywordExtractor = topia.termextract.extract.TermExtractor()

import data
from config import config

def cutup(str, length=255):
	"""
	cutup a string in pieces at most length long
	:rtype list of strings
	"""
	return cutup2([str], length)

def cutup2(sl, length):
	last = sl.pop()
	if (len(last) >= length):
		sl.append(last[:length])
		sl.append(last[length:])
		return cutup2(sl, length)
	else:
		sl.append(last)
		return sl

def getUserPath(id):
	longFileName = base64.urlsafe_b64encode(id)
	path = os.path.normpath("/".join(cutup(longFileName)))
	path = os.path.join("users", path)
	return path

def deleteUser(id):
	path = getUserPath(id)
	if(os.path.isdir(path)):
		shutil.rmtree(path)

class User:
	"""
	:var keywordRatings: a keyword ratings dict
	"""
	def __init__(self, id):
		"""
		:type id: string
		"""
		path = getUserPath(id)
		if(not os.path.isdir(path)):
			os.makedirs(path, 0777)
		self.path = path
		self.keywordRatings = dict()
		self.loadData()

	def loadData(self):
		try:
			f = open(os.path.join(self.path, "keywordRatings.pickle"),'rb')
			self.keywordRatings = pickle.load(f)
			f.close()
		except IOError:
			pass

	def saveData(self):
		f = open(os.path.join(self.path, "keywordRatings.pickle"),'wb')
		pickle.dump(self.keywordRatings, f, -1)
		f.close()

	def getKeywordRating(self, keyword):
		"""
		get rating for a keyword
		:type keyword: string
		:rtype float
		"""
		if keyword not in self.keywordRatings:
			return 0.0
		else:
			return self.keywordRatings[keyword]

	def modifyKeywordRating(self, keyword, ratingMod):
		"""
		set rating for a keyword
		:type keyword: string
		:type ratingMod: float
		"""
		self.keywordRatings[keyword] = self.getKeywordRating(keyword) + ratingMod

	def setKeywordRating(self, keyword, rating):
		"""
		set rating for a keyword
		:type keyword: string
		:type rating: float
		"""
		self.keywordRatings[keyword] = rating

	def getRating(self, str):
		"""
		get rating for a string
		:rtype float
		"""
		hypernymDepth = config.conf['hypernymDepth']
		hypernymDepthPowerQ = config.conf['hypernymDepthPowerQ']
		useDepthWeightedRating = config.conf['useDepthWeightedRating']
		depthWeightingDepthPowerQ = config.conf['depthWeightingDepthPowerQ']
		averageFactorAddition = config.conf['averageFactorAddition']

		# keyword tagging

		keywords0 = sorted(keywordExtractor(str))
		# var keywords1: all keywords
		keywords1 = map(lambda x: x[0], keywords0)
		# var keywords2: keywords appearing at least 2x
		keywords2 = map(lambda x: x[0], [y for y in keywords0 if y[1] > 1])
		keywords = keywords2

		# get keyword rating as average of rated keywords

		removeUnratedKeywords = lambda l: [s for s in l if not s[1] == 0.0]
		getRatedKeywords = lambda l, depth: removeUnratedKeywords(map(lambda x: (x, self.getKeywordRating(x), depth), l))
		
		ratedKeywords = getRatedKeywords(keywords, 0)

		# get hypernym rating
		synsets = map(lambda k: wn.synsets(k.replace(' ','_')), keywords)
		synsets = [ss for ss in synsets if ss] # filter out the empty ones
		synsets = map(lambda ss: ss[0], synsets) # get first synset of each keyword
		for depth in range(1,hypernymDepth+1):
			newSynsets = []
			for ss in synsets:
				newSynsets.extend(ss.hypernyms())
			for ss in newSynsets:
				kwL = map(lambda x: x.replace('_',' '), ss.lemma_names)
				ratedKeywords.extend(getRatedKeywords(kwL, depth))
			synsets = newSynsets
		
		getDepthRating = lambda rating, depth, depthPowerQ: rating * pow(depth+1, -depthPowerQ)

		#ratedKeywords = [('x',1.0,0),('xx',1.0,2)]
		if(len(ratedKeywords) <= 0):
			rating = 0.0
		else:
			ratings = map(lambda x: getDepthRating(x[1],x[2],hypernymDepthPowerQ), ratedKeywords)
			if(useDepthWeightedRating):
				# weightedList makes sure additional hypernym ratings don't drive the rating down much:
				# if hypernymDepthPowerQ == depthWeightingDepthPowerQ rating([('x',1.0,0),('xx',1.0,2)]) == rating([('x',1.0,0)]) = weighted mean
				# which is also problematic because then rating rating([('x',1.0,0)]) == rating([('xx',1.0,2)])
				if(depthWeightingDepthPowerQ > hypernymDepthPowerQ):
					print "warning: depthWeightingDepthPowerQ > hypernymDepthPowerQ -> keyword hypernyms are more valuable then keywords"
				weightedList = map(lambda x: getDepthRating(1.0,x[2],depthWeightingDepthPowerQ), ratedKeywords)
				rating = sum(ratings) / (sum(weightedList) + averageFactorAddition)
			else:
				rating = sum(ratings) / len(ratings)
		return rating


u = "testUser"
t = User(u)
t.setKeywordRating('document',1.0) # 'document' is hypernym of 'patent'
for i in data.testdata:
	print t.getRating(i['brief']) # 'patent' is keyword of the first article
t.saveData()
deleteUser(u)

