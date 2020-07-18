# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 16:41:34 2020

@author: Bran
"""

import nltk
# run this to download necessary files
#nltk.download()
#nltk.download('punkt')

from nltk.tokenize import word_tokenize
#from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer


text = "If you set your goals ridiculously high and it's a failure, you will fail above everyone else's success."

# Tokenization
# this parses the string into units (usually words)
tokens = word_tokenize(text)
print(tokens)

# Lemmatization
# attempts to convert words into root word
# effectiveness can be reduced when using 
# lemmatization or stemming
# we're not going to download wordnet for this
#lemmatizer = WordNetLemmatizer()
#tokens=[lemmatizer.lemmatize(word) for word in tokens]

# Stemming
# attempts to convert words into root word

#tokens=word_tokenize(text.lower())
ps = PorterStemmer()
tokens=[ps.stem(word) for word in tokens]
print(tokens)

# Stop words
stopwords = nltk.corpus.stopwords.words('english')
print(stopwords)

tokens_new = [j for j in tokens if j not in stopwords]

# this is the result of only tokenizing and removing sopt words
#['If', 'set', 'goals', 'ridiculously', 'high', "'s", 'failure', ',', 'fail', 'everyone', 'else', "'s", 'success', '.']