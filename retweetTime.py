import tweepy

consumer_key = "your_consumer_key"
consumer_secret = "your_consumer_secret"
access_token = "your_access_token"
access_token_secret = "your_access_token_secret"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

def get_retweet_timestamps(tweet_id):
    retweets = api.retweets(tweet_id, tweet_mode='extended')
    
    for retweet in retweets:
        retweeted_status = retweet.retweeted_status
        if retweeted_status:
            retweet_time = retweet.created_at
            retweet_user = retweet.user.screen_name
            print(f"{retweet_user} retweeted at: {retweet_time}")


tweet_id = "your_tweet_id"
get_retweet_timestamps(tweet_id)
