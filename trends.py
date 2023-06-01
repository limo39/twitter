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

trends = api.get_place_trends(id=woeid, exclude="hashtags")
 
trends_list = [trend['name'] for value in trends for trend in value['trends']]

# Print the top trends in a single line
trends_str = " ".join(trends_list)
print("The top trends for the location are:", trends_str)
