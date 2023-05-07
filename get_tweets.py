#http://www.tweepy.org/
import tweepy
import sys
import csv

#Get your Twitter API credentials and enter them here
consumer_key = "IgM5R8xVMGNJBZuqQ42RbEHI5"
consumer_secret = "Myu6ernLGk2ODUrsBNWr6deZu01MzlnVMTkvz93JARFJVHuoqU"
access_key = "339802190-clJpgJofm8n6tXUPVwrmWDILUZFdEGvecKqynjbY"
access_secret = "qqOr9Fx5Sh3uIxS0nf8Y0ic1rnoK2HJhQg0uAIpEGL5fh"

#method to get a user's last tweets
class TweetName():
    def __init__(self,name):
        self.name = name

    def get_tweets(self):
        #http://tweepy.readthedocs.org/en/v3.1.0/getting_started.html#api
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_key, access_secret)
        api = tweepy.API(auth)

        #set count to however many tweets you want
        number_of_tweets = 100
        #get tweets
        tweets_for_csv = []
        for tweet in tweepy.Cursor(api.user_timeline, screen_name = self.name).items(number_of_tweets):
            #create array of tweet information: username, tweet id, date/time, text
            #tweets_for_csv.append([username, tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")])
            tweets_for_csv.append([tweet.text.encode("utf-8")])
        #write to a new csv file from the array of tweets
        outfile = self.name + ".txt"
        print("writing to " + outfile)
        with open(outfile, 'w+') as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerows(tweets_for_csv)
        print('get tweet called')
