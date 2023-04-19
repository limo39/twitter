import tweepy

# set up your authentication credentials
consumer_key = 'your_consumer_key'
consumer_secret = 'your_consumer_secret'

# initialize the authentication handler
auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret)

# get the authorization URL
redirect_url = auth.get_authorization_url()

# ask the user to authorize their account
print(f"Please authorize the app by visiting this URL: {redirect_url}")
verifier = input("Enter the verification code: ")

# retrieve the access token and secret
access_token, access_token_secret = auth.get_access_token(verifier)

# initialize the API client
api = tweepy.API(auth)

# ask the user to confirm their intent to delete all tweets
confirmation = input("Are you sure you want to delete all your tweets? (y/n): ")
if confirmation.lower() == 'y':
    # delete all tweets
    for status in tweepy.Cursor(api.user_timeline).items():
        try:
            api.destroy_status(status.id)
            print(f"Deleted tweet with ID {status.id}")
        except tweepy.TweepError as e:
            print(f"Error deleting tweet with ID {status.id}: {str(e)}")
else:
    print("Operation cancelled.")
