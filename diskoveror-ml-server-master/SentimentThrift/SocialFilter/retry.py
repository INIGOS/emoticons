import pickle
import re, collections
import os, sys, inspect, traceback
cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)
from Twokenize import twokenize
from Twokenize import emoticons
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
stemmer=PorterStemmer()
path = cmd_folder+"/models/"

class Filter(object):

    def __init__(self):
        self.acronyms = self.load_obj("acronymsDict")
        self.emoticons = self.load_obj("SmileyDict")
        self.result = {}

    def load_obj(self,name ):
        with open( path + name + '.pkl', 'rb') as f:
            return pickle.load(f)

    def process(self,text,stopwordsF = 0, stemmerF = 0, encode = 1):
        list1=[]
        list2=[]
        line = re.sub(twokenize.Url_RE," ", text)
        temp = line.replace("#" , " ").lower().split()
        temp = " ".join(temp)

        for word in twokenize.tokenize(temp):
            if word != " ":

                word = word.strip()
                flagNonDict = 0

                try:

                    if self.wordDict[word] == 1:

                        word =	word
                except:
                    flagNonDict = 1
                    try:
                        score = self.emoticons[word]
                        emo = emoticons.analyze_tweetHeavy(word)

                        list1.append(emo)

                        self.result['EMOTICONS'] = list1
                    except:
                        try:
                            #Normalize Acronyms
                            word = self.acronyms[word]

                            list2.append(word)

                            self.result['ACRONYMS'] = list2

                        except:


                                if "@" in word:
                                 word = "@user"
        return self.result

fil=Filter()
ans=fil.process("lol :( hey this is INIGO SOLOMON from SERENDIO :) rofl :P :( =D lmbo , ok ciao")
print ans