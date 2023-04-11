import tweepy

# Set up API credentials
consumer_key = "your_consumer_key"
consumer_secret = "your_consumer_secret"
access_token = "your_access_token"
access_token_secret = "your_access_token_secret"

# Authenticate with Twitter API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Create Tweepy API object
api = tweepy.API(auth, wait_on_rate_limit=True)

# Prompt the user to enter the keyword to search for
keyword = input("Enter keyword to search for: ")

# Retrieve all tweets from the user's timeline
tweets = api.user_timeline(count=1000)

# Loop through the tweets and delete the ones containing the specified keyword
for tweet in tweets:
    if keyword.lower() in tweet.text.lower():
        try:
            api.destroy_status(tweet.id)
            print("Deleted tweet: {}".format(tweet.text))
        except Exception as e:
            print("Failed to delete tweet {}: {}".format(tweet.id, e))
