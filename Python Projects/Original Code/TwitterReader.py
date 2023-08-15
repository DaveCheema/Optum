from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

import json

ckey='5j6NRxTCMeYeX699HqcaQmnW1'
csecret = 'OJGV4ZZJZ92q5s0mTDeXKvJEqs1i4JXicXm9onwQUEfZuk1aXB'

atoken = '283119593-rBCTLgENNzPWjj9nB065jWgD9RZlqSSZzAUJ0CHz'
asecret = '116ErxfGGImxpa1liSkPRDgYVfr1VPRDeHlJq1aIRSBz3'

class listener(StreamListener):

	def on_data(self, data):
		print (data)
		return True

	def on_error(self, status):
		print (status)

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener())
twitterStream.filter(track=['Trump', 'impeachment', 'Pelosi'], is_async=True)