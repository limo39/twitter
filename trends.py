#!/usr/bin/env python
import tweepy

consumer_key =" "
consumer_secret = " "

key = " "
secret = " "

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(key, secret)

api = tweepy.API(auth)
woeid = input("Enter woeid: ")
# WOEID of Nairobi  1528488, NY = 2459115, Doha =1940517, UK - 12903, LA = 2442047

# woeid = 12903
 
# fetching the trends
trends = api.get_place_trends(id = woeid, exclude = "hashtags")
 
# printing the information
print("The top trends for the location are :")
 
for value in trends:
    for trend in value['trends']:
        print(trend['name'])