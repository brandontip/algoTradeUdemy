# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 18:57:45 2020

@author: Bran
"""

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob

# would not use either for finance because of words like bear, bull, red, etc.


###################################Vader#######################################

#general guideline: < -.05 = bad , > .05 good, else neutral

analyser = SentimentIntensityAnalyzer()
analyser.polarity_scores("This is not good")
# result:
# {'neg': 0.445, 'neu': 0.555, 'pos': 0.0, 'compound': -0.3412}
# notice it handles negation o.k.
# we want compound score


# can judge intensity from adjectives, punctuation, and capitalization
analyser.polarity_scores("This is good")
analyser.polarity_scores("This is awesome") 
analyser.polarity_scores("This is awesome!") 
analyser.polarity_scores("This is AWESOME!")
#Results:
#{'neg': 0.0, 'neu': 0.408, 'pos': 0.592, 'compound': 0.4404}
#{'neg': 0.0, 'neu': 0.328, 'pos': 0.672, 'compound': 0.6249}
#{'neg': 0.0, 'neu': 0.313, 'pos': 0.687, 'compound': 0.6588}
#{'neg': 0.0, 'neu': 0.281, 'pos': 0.719, 'compound': 0.729}

# works with some slang emojis and abbreviations 
analyser.polarity_scores("It works :D") 
analyser.polarity_scores("ROFL")
analyser.polarity_scores("This SUX") 


###################################Textblob####################################

TextBlob("I").sentiment
#result: Sentiment(polarity=0.0, subjectivity=0.0)
TextBlob("am").sentiment
#Sentiment(polarity=0.0, subjectivity=0.0)
TextBlob("clearly").sentiment
#Sentiment(polarity=0.10000000000000002, subjectivity=0.3833333333333333)
TextBlob("the").sentiment
#Sentiment(polarity=0.0, subjectivity=0.0)
TextBlob("best").sentiment
#entiment(polarity=1.0, subjectivity=0.3)
TextBlob("student").sentiment
#Sentiment(polarity=0.0, subjectivity=0.0)

# result is average of non-zero sentiments
TextBlob("I am clearly the best student").sentiment
#Sentiment(polarity=0.55, subjectivity=0.3416666666666667)



TextBlob("not").sentiment
#Sentiment(polarity=0.0, subjectivity=0.0)
TextBlob("good").sentiment
#Sentiment(polarity=0.7, subjectivity=0.6000000000000001)

TextBlob("I am not good").sentiment
#does o.k. with negations it seems
#Sentiment(polarity=-0.35, subjectivity=0.6000000000000001)
