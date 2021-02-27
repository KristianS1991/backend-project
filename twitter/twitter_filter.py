import tweepy
import time
import datetime
from textblob import TextBlob
from tweet_store import TweetStore
import json

file_path = 'twitter/api_config.json'

with open(file_path) as f:
    twitter_api = json.loads(f.read())

consumer_key = twitter_api['consumer_key']
consumer_secret = twitter_api['consumer_secret']
access_token = twitter_api['access_token']
access_token_secret = twitter_api['access_token_secret']

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
store = TweetStore()


class StreamListener(tweepy.StreamListener):
    def __init__(self, time_limit=10):
        self.start_time = time.time()
        self.limit = time_limit
        super(StreamListener, self).__init__()

    def on_status(self, status):
        if (time.time() - self.start_time) < self.limit:
            if ('RT @' not in status.text):
                blob = TextBlob(status.text)
                sent = blob.sentiment
                polarity = sent.polarity
                subjectivity = sent.subjectivity

                tweet_item = {
                    'id_str': status.id_str,
                    'text': status.text,
                    'polarity': polarity,
                    'subjectivity': subjectivity,
                    'username': status.user.screen_name,
                    'name': status.user.name,
                    'profile_image_url': status.user.profile_image_url,
                    'received_at': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }

                store.push(tweet_item)
                if (polarity > 0):
                    print("Pushed to redis:", tweet_item)
            return True
        else:
            return False


    def on_error(self, status_code):
        if status_code == 420:
            return False

# below is now being called on POST request from resources.twitter_stream
# stream_listener = StreamListener()
# stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
# stream.filter(track=["food"])
