import tweepy

# Enter your API credentials here
consumer_key = ''
consumer_secret = ''

access_token = ''
access_token_secret = ''

# Set up the Tweepy API object
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Define a function to handle incoming tweets
class TweetCounter(tweepy.Stream):
    def __init__(self, keyword):
        self.count = 0
        super().__init__(consumer_key, consumer_secret, access_token, access_token_secret)

        self.keyword = keyword

    def on_status(self, status):
        if self.keyword.lower() in status.text.lower():
            self.count += 1
            print("Number of tweets with {}: {}".format(self.keyword, self.count))


# Start the stream
keyword = input("Enter a keyword or hashtag to track: ")
tweet_counter = TweetCounter(keyword)
tweet_counter.filter(track=[keyword])
