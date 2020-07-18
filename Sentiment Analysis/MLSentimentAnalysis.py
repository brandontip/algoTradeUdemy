# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 10:14:34 2020

@author: Bran
"""
import pandas as pd
#use multinomial naive Bayes if only two values for dep. variable
# else, use GaussianNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

#####################import data set#############################
with open('pros.txt') as file_object:
    pros = file_object.read()


preproslist = pros.split("<Pros>")
proslist = [pro.replace("</Pros>","") for pro in preproslist]
prosdf = pd.DataFrame(proslist)
prosdf.columns = ["text"]
prosdf['sentiment'] = 2
prosdf.drop([0], inplace=True)

with open('cons.txt') as file_object:
    cons = file_object.read()

preconslist = cons.split("<Cons>")
conslist = [con.replace("</Cons>","") for con in preconslist]
consdf = pd.DataFrame(conslist)
consdf.columns = ["text"]
consdf['sentiment'] = -2
consdf.drop([0], inplace=True)

################create training and testing dataframes############

trainingpros = prosdf.iloc[:11000]
trainingcons = consdf.iloc[:11000]
trainingdf = trainingpros.append(trainingcons)

testpros = prosdf.iloc[11000:]
testcons = consdf.iloc[11000:]
testdf = testpros.append(testcons)
# this shuffles the rows
testdf =  testdf.sample(frac=1)


###########################training###############################


# tokenize the text and convert to matrix
vectorizer = CountVectorizer(stop_words='english')
X_vec = vectorizer.fit_transform(trainingdf["text"])
X_vec = X_vec.todense() # turns list of entry values into matrix

# Transform data by applying TF-IDF 
tfidf = TfidfTransformer() #by default applies "l2" normalization
X_tfidf = tfidf.fit_transform(X_vec)
X_tfidf = X_tfidf.todense()


# Apply Naive Bayes algorithm to train data
X_train = X_tfidf
Y_train = trainingdf["sentiment"]

# Train the NB classifier
clf = MultinomialNB().fit(X_train, Y_train) 


##############Predict sentiment using the trained classifier###################


X_vec_test = vectorizer.transform(testdf["text"]) #don't use fit_transform here because the model is already fitted
# otherwise, it will crash due to presence of new words
X_vec_test = X_vec_test.todense() #convert sparse matrix to dense

# Transform data by applying term frequency inverse document frequency (TF-IDF) 
X_tfidf_test = tfidf.fit_transform(X_vec_test)
X_tfidf_test = X_tfidf_test.todense()


# Predict the sentiment values
y_pred = clf.predict(X_tfidf_test)

testdf["prediction"] = y_pred
matches = 0
for i in range(len(testdf)):
    if testdf.iloc[i,-2] == testdf.iloc[i,-1]:
        matches+=1
        
matches/len(testdf)
# result: 86.6% accuracy!
        
###################sentiment analysis using just VADER#########################

analyser = SentimentIntensityAnalyzer()
analyser.polarity_scores("quality")['compound']

testdf['VADERsent']=0

for i in range(len(testdf)):
    if analyser.polarity_scores(testdf.iloc[i,0])['compound'] > 0:
        testdf.iloc[i,-1]=2
    else:
        testdf.iloc[i,-1]=-2
  
vmatches = 0
for i in range(len(testdf)):
    if testdf.iloc[i,-2] == testdf.iloc[i,-1]:
        vmatches+=1
        
vmatches/len(testdf)  
# result: 67.3-76.1% accuracy (former is >=0, latter is >0) 
  



