import pickle , re, collections ,os , sys , inspect , traceback
cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)
from Twokenize import twokenize
from Twokenize import emoticons
path = cmd_folder+"/models/"

class Extraction(object):
    def __init__(self):
        self.acronyms=self.load_obj("acronymsDict")
        self.emoticons=self.load_obj("SmileyDict")
        self.answer={}
    def load_obj(self,name):
        with open( path + name + '.pkl' , 'rb') as f:
            return pickle.load(f)
    def Smileyoperation(self,text):
        emo_list=[]

        for word in twokenize.tokenize(text):
            if word !=" ":
                word=word.strip()

                try:
                    score=self.emoticons[word]
                    emo=emoticons.analyze_tweetHeavy(word)
                    emo_list.append(emo)
                    self.answer['SMILEYS']=emo_list
                except:

                    if "@" in word:
                        word="@user"
        return self.answer
    def AcronymsOperation(self,text):
        acr_list=[]

        for word in twokenize.tokenize(text):
            if word !=" ":
                word=word.strip()

                try:
                    word=self.acronyms[word]
                    acr_list.append(word)
                    self.answer['EXPANDED ACRONYMS']=acr_list
                except:
                    if "@" in word:
                        word="@user"

        return self.answer
extract=Extraction()
output=extract.Smileyoperation("hey hello :p , today is monday :) rofl and the weather is too hot @ chennai :( :p lol , ok ciao ")
#replace SmileyOperation by AcronymsOperation to get all the acronmys present in the given text
print output
