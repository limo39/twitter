import tweepy
import requests
from PIL import Image
from io import BytesIO
import os

consumer_key =""
consumer_secret = ""

key = ""
secret = ""

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(key, secret)

api = tweepy.API(auth)

# prompt user for tweet link
tweet_url = input("Enter the link to the tweet containing a video: ")

# extract tweet ID from link
tweet_id = tweet_url.split("/")[-1]

# get tweet object
tweet = api.get_status(tweet_id, tweet_mode='extended')

# extract video URL from tweet
media = tweet.entities.get('media', [])
if len(media) > 0 and media[0]['type'] == 'video':
    variants = media[0]['video_info']['variants']
    video_url = max(variants, key=lambda v: v.get('bitrate', 0))['url']

    # download video
    response = requests.get(video_url)
    video = BytesIO(response.content)

    # save video to file
    desktop_dir = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    video_path = os.path.join(desktop_dir, f"{tweet_id}.mp4")
    with open(video_path, "wb") as f:
        f.write(video.getbuffer())
    print(f"Video saved to {video_path}")
else:
    print("The tweet does not contain a video.")
