# Import the Twython class
from numpy import positive
from twython import Twython
import json
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import tweepy
from googletrans import Translator

# function to print sentiments
# of the sentence.
def sentiment_scores(sentence):
  
    # Create a SentimentIntensityAnalyzer object.
    sid_obj = SentimentIntensityAnalyzer()
  
    # polarity_scores method of SentimentIntensityAnalyzer
    # oject gives a sentiment dictionary.
    # which contains pos, neg, neu, and compound scores.
    sentiment_dict = sid_obj.polarity_scores(sentence)
      
    '''print("Overall sentiment dictionary is : ", sentiment_dict)
    print("sentence was rated as ", sentiment_dict['neg']*100, "% Negative")
    print("sentence was rated as ", sentiment_dict['neu']*100, "% Neutral")
    print("sentence was rated as ", sentiment_dict['pos']*100, "% Positive")
  
    print("Sentence Overall Rated As", end = " ")
  '''
    # decide sentiment as positive, negative and neutral
    if sentiment_dict['compound'] >= 0.05 :
        return "Positive"
  
    elif sentiment_dict['compound'] <= - 0.05 :
        return "Negative"
  
    else :
        return "Neutral"

def twitter_credentials():
    # Enter your keys/secrets as strings in the following fields
    credentials = {}
    credentials['CONSUMER_KEY'] = 'zgU92rH9lXYJeDK6otwie8Wpr'
    credentials['CONSUMER_SECRET'] = 'x13U1nq7z11sXOSoB2CDeADiKfBAyN2N8G8Dki4hc6D0J6Cb9I'
    credentials['ACCESS_TOKEN'] = '1390534356796514304-a9OrHPnkGQQTTwRZVUK5UuOf01l1ss'
    credentials['ACCESS_SECRET'] = 'QkexVBujL2fZiu3FVipn9Zmf0aaZ0PQfBkJZ4PlahFK8K'

    # Save the credentials object to file
    with open("twitter_credentials.json", "w") as file:
        json.dump(credentials, file)
    
def twitter_query(query):
    # Load credentials from json file
    with open("twitter_credentials.json", "r") as file:
        creds = json.load(file)

    # Instantiate an object
    python_tweets = Twython(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'])

    # Create our query
    query = {'q': query,
            'result_type': 'mixed',
            'count': 100,
            'lang': 'en',
            'geocode':'' 
            }

    # Search tweets
    dict_ = {'user': [], 'date': [], 'text': [], 'favorite_count': [], 'hashtags':[], 'location':[], 'language':[]}
    for status in python_tweets.search(**query)['statuses']:
        dict_['user'].append(status['user']['screen_name'])
        dict_['date'].append(status['created_at'])
        dict_['text'].append(status['text'])
        dict_['favorite_count'].append(status['favorite_count'])
        dict_['hashtags'].append([hashtag['text'] for hashtag in status['entities']['hashtags']])
        dict_['location'].append(status['user']['location'])
        dict_['language'].append('en')

    # Structure data in a pandas DataFrame for easier manipulation
    df = pd.DataFrame(dict_)
    df.sort_values(by='favorite_count', inplace=True, ascending=False)
    sentiment=[]
    for i in df['text']:
        sentiment+=[sentiment_scores(i)]
    df['sentiment']=sentiment
    try:
        pos=df['sentiment'].value_counts()['Positive']
    except:
        pos=0
    try:
        neg=df['sentiment'].value_counts()['Negative']
    except:
        neg=0
    try:
        neu=df['sentiment'].value_counts()['Neutral']
    except:
        neu=0
    #print(df.shape)
    return df,pos,neg,neu


def getinfo(name):
    

    # assign the values accordingly

    consumer_key = 'zgU92rH9lXYJeDK6otwie8Wpr'
    consumer_secret = 'x13U1nq7z11sXOSoB2CDeADiKfBAyN2N8G8Dki4hc6D0J6Cb9I'
    access_token =  '1390534356796514304-a9OrHPnkGQQTTwRZVUK5UuOf01l1ss'
    access_token_secret = 'QkexVBujL2fZiu3FVipn9Zmf0aaZ0PQfBkJZ4PlahFK8K'
    
    # authorization of consumer key and consumer secret
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    
    # set access to user's access key and access secret 
    auth.set_access_token(access_token, access_token_secret)
    
    # calling the api 
    api = tweepy.API(auth)

    # the screen name of the user
    screen_name = name
    
    # fetching the user
    user = api.get_user(screen_name)
    return user._json
    
def langdetect(text_content):
    
    translator = Translator()
    text_content= text_content.split()
    ans=''
    for i in text_content:
        if translator.detect(i).lang != 'en':
            ans= translator.detect(i).lang
        else:
            #print('en')
             
            return ans
    
    
def translate(tweet):
    
    translator = Translator()
    text_content= tweet.split()
    ans=''
    '''for i in text_content:
        translation = translator.translate(i, dest='en')
        ans+=' '+translation.text'''
    #print("Translation by Google Translate:",translator.translate(tweet, dest='en').text)
    #print("Translation by Proposed Method:", ans)
    return ans
    
    
'''def sentplot(df):
    fig, ax = plt.subplots()
    fig=df['sentiment'].value_counts().plot(ax=ax, kind='barh')
    return fig'''
#twitter_credentials()
#twitter_query('Rajya Lok Sabha Public Budget Demands February', 'mixed')

#print(langdetect("chalo chalte hai"))