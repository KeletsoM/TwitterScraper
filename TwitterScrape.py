from tweepy.streaming import StreamListener
from tweepy import API
from tweepy import Cursor
from tweepy import OAuthHandler
from tweepy import Stream
import numpy as np
import pandas as pd
import twitter_credentials
import matplotlib.pyplot as plt

#### Twitter Client ####
class TwitterClient():
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().auth_twitter_app()
        self.twitter_client = API(self.auth)

        self.twitter_user = twitter_user

    def get_twitter_client_api(self):
        return self.twitter_client

    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id= self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets

    def get_friend_list(self,num_friends):
        friend_list = []
        for friend in Cursor(self.twitter_client.friends, id= self.twitter_user).items(num_friends):
            friend_list.append(friend)
        return friend_list

    def get_home_timeline_tweets(self, num_tweets):
        home_timeline_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline, id= self.twitter_user).items(num_tweets):
            home_timeline_tweets.append(tweet)
        return home_timeline_tweets


#### Twitter Authenticator ####
class TwitterAuthenticator():
    def auth_twitter_app(self):
        auth = OAuthHandler(twitter_credentials.CONSUMER_KEY,twitter_credentials.CONSUMER_SERET)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN,twitter_credentials.ACCESS_TOKEN_SECRET)
        return auth

#### Twitter Streamer ####
class TwitterStreamer():
    
    def __init__(self):
        self.twitter_authenticator = TwitterAuthenticator()
    def stream_tweets(self, fetched_tweet_filename,hashtag_list):
    #This handles auth and the connection to twitter streaming API
        listener = TwitterListener(fetched_tweet_filename)
        auth = self.twitter_authenticator.auth_twitter_app()
        stream = Stream(auth,listener)

        #this line filters tweets
        stream.filter(track=hashtag_list)

#### TWITTER STREAM LISTENER ####
class TwitterListener(StreamListener):

    def __init__(self, fetched_tweet_filename):
        self.fetched_tweet_filename = fetched_tweet_filename

    def on_data(self,data):
        try:
            print(data)
            with open(self.fetched_tweet_filename, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("Error on data: %s" % str(e))
        return True


    def on_error(self, status):
        print(status)

class TweetAnalyzer():

    def tweets_to_dataframe(self, tweets):
        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])

        
        df['date'] = np.array([tweet.created_at for tweet in tweets])
        df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        df['source'] = np.array([tweet.source for tweet in tweets])
        return df


if __name__ == "__main__":

    twitter_client = TwitterClient()
    tweet_analyzer = TweetAnalyzer()
    api = twitter_client.get_twitter_client_api()

    tweets = api.user_timeline(screen_name="rihanna", count= 50)

    df = tweet_analyzer.tweets_to_dataframe(tweets)
    #asdf = df.sort_values(by=['likes'], ascending=False)
    
    print(df.head(10))
    df.plot(kind='line', x= 'date' ,y= 'likes' )
    plt.show()
   
    