# Imports
import sys
import logging
import datetime
import time
import os
import json

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

from azure.eventhub import EventHubClient, Sender, EventData

from configurations import TwitterSettings, EventHubSettings

# Get Twitter account credentials
consumer_key = TwitterSettings['consumer_key']
consumer_secret = TwitterSettings['consumer_secret']
access_token = TwitterSettings['access_token']
access_secret = TwitterSettings['access_secret']

filter_keywords = TwitterSettings['filter_keywords']

# Event Hubs settings.
ADDRESS = EventHubSettings['address']
USER = EventHubSettings['user']
KEY = EventHubSettings['key']

class listener(StreamListener):

	def on_data(self, data):
		self.postMessageToEventHub(data)
		print (data)
		return True

	def on_error(self, status):
		print (status)

	def postMessageToEventHub(self, data):		
		try:
			sender.send(EventData(data))
			return True		
		except KeyboardInterrupt:
			pass
		except Exception as e:
			print("Error on_data: %s" % str(e))
		finally:
			return True

if __name__ == '__main__':
	try:
		client = EventHubClient(ADDRESS, debug=False, username=USER, password=KEY)
		sender = client.add_sender(partition="0")
		client.run()
		
		auth = OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(access_token, access_secret)
		twitterStream = Stream(auth, listener())
		twitterStream.filter(track=filter_keywords, is_async=True)
	except Exception as e:
		print("Top level Error: args:{0}, message:N/A".format(e.args))
