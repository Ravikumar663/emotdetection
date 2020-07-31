import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize,sent_tokenize
from autocorrect import Speller
import spacy

#CONTRACTION_MAP from wikipedia
CONTRACTION_MAP = {
"ain't": "is not",
"aren't": "are not",
"can't": "cannot",
"can't've": "cannot have",
"'cause": "because",
"could've": "could have",
"couldn't": "could not",
"couldn't've": "could not have",
"didn't": "did not",
"doesn't": "does not",
"don't": "do not",
"hadn't": "had not",
"hadn't've": "had not have",
"hasn't": "has not",
"haven't": "have not",
"he'd": "he would",
"he'd've": "he would have",
"he'll": "he will",
"he'll've": "he will have",
"he's": "he is",
"how'd": "how did",
"how'd'y": "how do you",
"how'll": "how will",
"how's": "how is",
"I'd": "I would",
"I'd've": "I would have",
"I'll": "I will",
"I'll've": "I will have",
"I'm": "I am",
"I've": "I have",
"i'd": "i would",
"i'd've": "i would have",
"i'll": "i will",
"i'll've": "i will have",
"i'm": "i am",
"i've": "i have",
"isn't": "is not",
"it'd": "it would",
"it'd've": "it would have",
"it'll": "it will",
"it'll've": "it will have",
"it's": "it is",
"let's": "let us",
"ma'am": "madam",
"mayn't": "may not",
"might've": "might have",
"mightn't": "might not",
"mightn't've": "might not have",
"must've": "must have",
"mustn't": "must not",
"mustn't've": "must not have",
"needn't": "need not",
"needn't've": "need not have",
"o'clock": "of the clock",
"oughtn't": "ought not",
"oughtn't've": "ought not have",
"shan't": "shall not",
"sha'n't": "shall not",
"shan't've": "shall not have",
"she'd": "she would",
"she'd've": "she would have",
"she'll": "she will",
"she'll've": "she will have",
"she's": "she is",
"should've": "should have",
"shouldn't": "should not",
"shouldn't've": "should not have",
"so've": "so have",
"so's": "so as",
"that'd": "that would",
"that'd've": "that would have",
"that's": "that is",
"there'd": "there would",
"there'd've": "there would have",
"there's": "there is",
"they'd": "they would",
"they'd've": "they would have",
"they'll": "they will",
"they'll've": "they will have",
"they're": "they are",
"they've": "they have",
"to've": "to have",
"wasn't": "was not",
"we'd": "we would",
"we'd've": "we would have",
"we'll": "we will",
"we'll've": "we will have",
"we're": "we are",
"we've": "we have",
"weren't": "were not",
"what'll": "what will",
"what'll've": "what will have",
"what're": "what are",
"what's": "what is",
"what've": "what have",
"when's": "when is",
"when've": "when have",
"where'd": "where did",
"where's": "where is",
"where've": "where have",
"who'll": "who will",
"who'll've": "who will have",
"who's": "who is",
"who've": "who have",
"why's": "why is",
"why've": "why have",
"will've": "will have",
"won't": "will not",
"won't've": "will not have",
"would've": "would have",
"wouldn't": "would not",
"wouldn't've": "would not have",
"y'all": "you all",
"y'all'd": "you all would",
"y'all'd've": "you all would have",
"y'all're": "you all are",
"y'all've": "you all have",
"you'd": "you would",
"you'd've": "you would have",
"you'll": "you will",
"you'll've": "you will have",
"you're": "you are",
"you've": "you have"
}

data = pd.read_csv('train.csv')
content = data['Content']
labels = data['Sentiment']
nlp = spacy.load('en_core_web_sm', parse = False, tag=False, entity=False)

#make all lowercase
def lowkey(text):
	text = text.lower()
	return text


#To remove all http links from text 
def rem_links(text):
	text = re.sub(r'http\S+ ', '',text)
	return text

#remove all 1 letter
def rem_ler(text):
	tokens = word_tokenize(text)
	tokens = [word for word in tokens if len(word) > 1]
	filtered = ' '.join(tokens)
	return filtered 


#Reemoves all the char others than alpha num
def rem_oan(text):
	text = re.sub('[^a-zA-Z0-9\s]', '', text)
	text = re.sub(' +', ' ', text)
	return text


#Remove all the stop words from the sentence
def rem_stopwords(text):
	tokens = word_tokenize(text)
	stop_words = set(stopwords.words('english'))
	filtered_text = [w for w in tokens if not w in stop_words]
	filtered = ' '.join(filtered_text)
	return filtered


#remove all the Contractions
def expand_contractions(text, contraction_mapping=CONTRACTION_MAP):
    
    contractions_pattern = re.compile('({})'.format('|'.join(contraction_mapping.keys())), 
                                      flags=re.IGNORECASE|re.DOTALL)
    def expand_match(contraction):
        match = contraction.group(0)
        first_char = match[0]
        expanded_contraction = contraction_mapping.get(match) \
                                   if contraction_mapping.get(match) \
                                    else contraction_mapping.get(match.lower())                       
        expanded_contraction = first_char+expanded_contraction[1:]
        return expanded_contraction
        
    expanded_text = contractions_pattern.sub(expand_match, text)
    expanded_text = re.sub("'", "", expanded_text)
    return expanded_text
#Auto correct spelling mistakes
def auto_correct(text):
	spell= Speller(lang='en')
	tokens = word_tokenize(text)
	filtered_text =[]
	for i in tokens:
		filtered_text.append(spell(i))
	filtered = ' '.join(filtered_text)
	return filtered


#lemmatization
def lemmatize_text(text):
    text = nlp(text)
    text = ' '.join([word.lemma_ if word.lemma_ != '-PRON-' else word.text for word in text])
    return text


def pre_process(text):
	text = lowkey(text)
	text = rem_links(text)
	text = rem_oan(text)
	text = rem_stopwords(text)
	text = expand_contractions(text)
	text = auto_correct(text)
	text = lemmatize_text(text)
	return text


def main():
	new_content = []
	for i in content:
		i = pre_process(str(i))
		new_content.append(i)
	new_dict = list(zip(new_content,labels))
	df = pd.DataFrame(new_dict,columns = ['content','sentiment'])
	df.to_csv('processed_train.csv', index = False)
	
	


if __name__ == "__main__":
	main()