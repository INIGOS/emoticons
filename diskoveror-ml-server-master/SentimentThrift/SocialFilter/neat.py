import pickle
import re, collections
import os, sys, inspect, traceback
cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)
from Twokenize import twokenize
from Twokenize import emoticons
path = cmd_folder+"/models/"

class Filter(object):

    def __init__(self):
        self.acronyms = self.load_obj("acronymsDict")
        self.emoticons = self.load_obj("SmileyDict")
        self.result = {}

    def load_obj(self,name ):
        with open( path + name + '.pkl', 'rb') as f:
            return pickle.load(f)

    def process(self,text):
        list1=[]
        list2=[]


        for word in twokenize.tokenize(text):
            if word != " ":

                word = word.strip()


                try:

                    if self.wordDict[word] == 1:

                        word =	word
                except:

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