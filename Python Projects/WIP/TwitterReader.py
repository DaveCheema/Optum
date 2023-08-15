import datetime
import time
import json

import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

from azure.eventhub import EventHubProducerClient, EventData

from configurations import EventHubSettings, TwitterSettings

# Twitter settings
CONSUMER_KEY = TwitterSettings['consumer_key']
CONSUMER_SECRET = TwitterSettings['consumer_secret']
ACCESS_TOKEN = TwitterSettings['access_token']
ACCESS_SECRET = TwitterSettings['access_secret']
FILTER_KEYWORDS = TwitterSettings['filter_keywords']

# Eventhub settings
CONNECTION_STRING = EventHubSettings['connection_string']
EVENT_HUB_NAME = EventHubSettings['eventhub_name']
PARTITION_ID = EventHubSettings['partition_id']

class listener(StreamListener):

	def on_data(self, data):
		
		self.postMessageToEventHub(data)		
		return True

	def on_error(self, status):
		print(status)

	def postMessageToEventHub(self, data):
		try:
			event_data_batch = client.create_batch()
			event_data_batch.add(EventData(data))
			client.send_batch(event_data_batch)
			print(data)
		except Exception as e:
			print(e.args)
			pass

if __name__ == '__main__':
	try:
		client = EventHubProducerClient.from_connection_string(
				CONNECTION_STRING, eventhub_name=EVENT_HUB_NAME)

		auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
		auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
		twitterStream = Stream(auth, listener())
		twitterStream.filter(track=FILTER_KEYWORDS, is_async=True)
	except Exception as e:
		print("Top level Error: args:{0}, message:N/A".format(e.args))
	finally:
		pass
