import nltk
import string

from nltk.corpus import stopwords
from nltk.corpus import wordnet

from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.stem import WordNetLemmatizer

from googletrans import Translator

from sklearn.feature_extraction.text import TfidfVectorizer

class KeywordExtractor:
    def __init__(self,text_):
        self.text = text_.lower()
        self.translator = Translator()
        self.stop_words = set(stopwords.words('english'))
        self.punctuations = string.punctuation
        self.word_tokens = word_tokenize(self.text)

        self.filtered_sentence = []
        for w in self.word_tokens:
            if w not in self.stop_words and w not in self.punctuations:
                self.filtered_sentence.append(w)
        self.filtered_sentence = " ".join(self.filtered_sentence)
        self.translated_text = self.translator.translate(self.filtered_sentence, dest='en').text
        self.word_tokens = word_tokenize(self.translated_text)
        
    def extractKeywordList(self):
        stopwords = nltk.corpus.stopwords.words('english')
        tagList = []
        
        for i in self.word_tokens:
            wordList = nltk.word_tokenize(i)
            wordList[0] = wordList[0].lower()
            wordList = [w for w in wordList if not w in stopwords]
            tagged = nltk.pos_tag(wordList)
            tagList.append(tagged)
            
        punctuation = ['.', ',', ':', ';', '?', '(', ')', '[', ']', '&', '!', '*', '@', '#', '$', '%', '``', "''"]
    
        tagList[:] = [x for x in tagList if len(x)!=0]
        keyword_list_withTags = [word for word in tagList if word[0][0] not in stopwords and word[0][0] not in punctuation]

        wnl = WordNetLemmatizer()
        keyword_list = []
        for key in keyword_list_withTags:
            keytmp=""
            if key[0][1].startswith('J'):
                keytmp = wordnet.ADJ
            elif key[0][1].startswith('V'):
                keytmp = wordnet.VERB
            elif key[0][1].startswith('N'):
                keytmp = wordnet.NOUN
            elif key[0][1].startswith('R'):
                keytmp = wordnet.ADV
            else:
                keytmp = wordnet.NOUN
            keyword_list.append(wnl.lemmatize(key[0][0].lower(),pos=keytmp))    
            
        return keyword_list          
                    