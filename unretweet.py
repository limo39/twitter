import tweepy

# Your Twitter API credentials
consumer_key = "YOUR_CONSUMER_KEY"
consumer_secret = "YOUR_CONSUMER_SECRET"
access_token = "YOUR_ACCESS_TOKEN"
access_token_secret = "YOUR_ACCESS_TOKEN_SECRET"

# Authenticate to Twitter
auth = tweepy.OAuth1UserHandler(
    consumer_key, consumer_secret,
    access_token, access_token_secret
)

# Create an API object
api = tweepy.API(auth)

# Get all the retweets from your account
retweets = api.retweets_of_me()

# Unretweet all the retweets
for retweet in retweets:
    api.unretweet(retweet.id)
