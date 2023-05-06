import tweepy
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# Define the Twitter API keys and access tokens
consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""

# Define the hashtag and/or username to monitor
hashtag = "#hashtag"
username = "@handle"

# Define the font and text color to use for the name and handle overlays
name_font = ImageFont.truetype("arial.ttf", 20)
handle_font = ImageFont.truetype("arial.ttf", 16)
text_color = (255, 255, 255)

# Define the video output file path and properties
output_file = "output.mp4"
fps = 30.0

# Initialize the Tweepy API client with the Twitter API keys and access tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Define a function to extract the video URL from a tweet
def extract_video_url(tweet):
    media = tweet.entities.get("media", [])
    for item in media:
        if item.get("type") == "video":
            variants = item.get("video_info", {}).get("variants", [])
            for variant in variants:
                if variant.get("content_type") == "video/mp4":
                    return variant.get("url")
    return None

# Define a function to add the user's avatar, name, and handle to a video frame
def add_overlays(frame, user):
    # Get the user's avatar, name, and handle
    avatar_url = user.profile_image_url_https.replace("_normal", "")
    avatar_img = Image.open(requests.get(avatar_url, stream=True).raw).convert("RGBA")
    name_text = user.name
    handle_text = user.screen_name

    # Define the size and position of the avatar image and text overlays
    avatar_width = 64
    avatar_height = 64
    avatar_x = 10
    avatar_y = 10
    text_x = avatar_x + avatar_width + 10
    text_y = avatar_y

    # Create the name and handle text overlays as PIL Image objects
    name_overlay = Image.new("RGBA", (200, 40), (0, 0, 0, 128))
    handle_overlay = Image.new("RGBA", (200, 40), (0, 0, 0, 128))
    draw_name = ImageDraw.Draw(name_overlay)
    draw_handle = ImageDraw.Draw(handle_overlay)
    draw_name.text((0, 0), name_text, font=name_font, fill=text_color)
    draw_handle.text((0, 0), handle_text, font=handle_font, fill=text_color)

    # Convert the PIL Image objects to OpenCV format
    avatar_img = cv2.cvtColor(np.array(avatar_img), cv2.COLOR_RGBA2BGRA)
    name_overlay = cv2.cvtColor(np.array(name_overlay), cv2.COLOR_RGBA2BGRA)
    handle_overlay = cv2.cvtColor(np.array(handle_overlay), cv2.COLOR_RGBA2BGRA)

    # Resize the overlays to match the size of the avatar image
    name_overlay = cv2

def make_video(screen_name, tweet_id):
    # Get tweet object
    tweet = api.get_status(tweet_id, tweet_mode='extended')
    
    # Get video URL
    for media in tweet.entities.get("media",[{}]):
        if media.get("type",None) == "video":
            variants = media["video_info"]["variants"]
            video_url = max(variants, key=lambda v: v.get('bitrate', 0))['url']
            break

    # Download video
    video_path = f"{screen_name}_{tweet_id}.mp4"
    urllib.request.urlretrieve(video_url, video_path)
    
    # Get user information
    user = tweet.user
    user_name = user.name
    user_handle = user.screen_name
    avatar_url = user.profile_image_url_https.replace("_normal", "")
    avatar_path = f"{screen_name}_avatar.jpg"
    
    # Download user avatar
    urllib.request.urlretrieve(avatar_url, avatar_path)
    
    # OpenCV setup
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    frame_size = (640, 640)
    video = cv2.VideoWriter(f"{screen_name}_{tweet_id}_out.mp4", fourcc, 30.0, frame_size)
    
    # Add frames to video
    for i in range(30):
        img = cv2.imread(avatar_path)
        img = cv2.resize(img, frame_size)
        video.write(img)
    
    video_capture = cv2.VideoCapture(video_path)
    while True:
        ret, frame = video_capture.read()
        if not ret:
            break
        frame = cv2.resize(frame, frame_size)
        font = cv2.FONT_HERSHEY_SIMPLEX
        bottomLeftCornerOfText = (10, 620)
        fontScale = 0.5
        fontColor = (255, 255, 255)
        lineType = 2
        cv2.putText(frame,user_name + f" (@{user_handle})", 
                    bottomLeftCornerOfText, 
                    font, 
                    fontScale,
                    fontColor,
                    lineType)
        video.write(frame)
        
    # Release resources
    video_capture.release()
    video.release()
    cv2.destroyAllWindows()
    
    # Tweet the video
    video_tweet = api.update_with_media(f"{screen_name}_{tweet_id}_out.mp4", status=f"@{user_handle} Here is your video!")
    print(f"Tweeted video: {video_tweet.id}")
