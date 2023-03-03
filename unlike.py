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

# Get all the liked tweets from your account
liked_tweets = api.favorites()

# Unlike all the liked tweets
for tweet in liked_tweets:
    api.destroy_favorite(tweet.id)
