import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import json

import azure.cosmos.documents as documents
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.errors as errors
import datetime

import os
import sys
import json
import logging
import time
from azure.eventhub import Offset
from azure.eventhub import EventHubClient, Receiver

from configurations import EventHubSettings, DbSettings

# Event Hubs settings.
ADDRESS = EventHubSettings['address']
USER = EventHubSettings['user']
KEY = EventHubSettings['key']

CONSUMER_GROUP = "$Default"
OFFSET = Offset("-1")
PARTITION = "0"

total = 0
last_sn = -1
last_offset = "-1"

#-----------------------------------------------------
# Cosmos DB Connection settings.
#-----------------------------------------------------
HOST = DbSettings['host']
MASTER_KEY = DbSettings['master_key']
DATABASE_ID = DbSettings['database_id']
COLLECTION_ID = DbSettings['collection_id']
preferredLocations = DbSettings['preferred_locations']

database_link = 'dbs/' + DATABASE_ID
collection_link = database_link + '/colls/' + COLLECTION_ID

#------------------------------------------------------------------
# Set position of Change Feed reading.
#------------------------------------------------------------------
options = {
    'startFromBeginning' : True
}

class IDisposable(cosmos_client.CosmosClient):
   
    def __init__(self, obj):
        self.obj = obj

    def __enter__(self):
        return self.obj  # bound to target

    def __exit__(self, exception_type, exception_val, trace):
        # extra cleanup in here
        self.obj = None

def create_db_and_collection(client):    
    try:
        # setup database for this sample
        try:
            client.CreateDatabase({"id": DATABASE_ID})

        except errors.HTTPFailure as e:
            if e.status_code == 409:
                pass            
            else:
                raise

        # setup collection for this sample
        try:
            client.CreateContainer(
                database_link, {"id": COLLECTION_ID, "partitionKey": {"paths": ["/id"]}})
        except errors.HTTPFailure as e:
            if e.status_code == 409:
               pass            
            else:
                raise

    except errors.HTTPFailure as e:
        print('\ncreate_db_and_collection has caught an error. {0}'.format(e))
    finally:
        print("\ncreate_db_and_collection created.")


class ChangeFeedManagement:

    @staticmethod
    def ProcessChangefeed(client):
        start_time = time.time
        print('\nReading Change Feed from the beginning\n')

        options = {}
        # For a particular Partition Key Range we can use options['partitionKeyRangeId']
        options["startFromBeginning"] = True
        # Start from beginning will read from the beginning of the history of the collection
        # If no startFromBeginning is specified, the read change feed loop will pickup the documents that happen while the loop / process is active
        response = client.QueryItemsChangeFeed(collection_link, options)
        for doc in response:
            print(doc)

        end_time = time.time
        run_time = end_time - start_time
        print("\nReceived {} Change feeds in {} seconds".format(total, run_time))        

if __name__ == '__main__':    
   
    try:
        client = cosmos_client.CosmosClient(HOST, {'masterKey': MASTER_KEY})

        #Process Change Feed
        ChangeFeedManagement.ProcessChangefeed(client)
        
        for eventData in response:
            processChangeFeed(eventData)

        if client is None:
            ClientCreateException: 'Cosmos DB client creation failed'
    except:
        raise

    create_db_and_collection(client)    
        
ehClient = EventHubClient(ADDRESS, debug=False, username=USER, password=KEY)

# try:
#     receiver = ehClient.add_receiver(
#         CONSUMER_GROUP, PARTITION, prefetch=5000, offset=OFFSET)
#     ehClient.run()

#     start_time = time.time()
   
    # batch = receiver.receive(timeout=1000)

    # while batch:

    #     for event_data in batch:

    #         try:
    #             dictData = json.loads(event_data.body_as_str(encoding='UTF-8'))
    #             dictData["id"] = str(dictData["id"])
    #             client.CreateItem(collection_link, dictData)

    #             total += 1

    #         except errors.HTTPFailure as e:
    #             if e.status_code == 409:
    #                 print('Item with id \'{0}\' was found'.format(
    #                     dictData["id"]))
    #                 pass
    #             else:
    #                 raise

    #     batch = receiver.receive(timeout=1000)

#     end_time = time.time()
#     ehClient.stop()
#     run_time = end_time - start_time
#     print("Received {} messages in {} seconds".format(total, run_time))

try:
    receiver = ehClient.add_receiver(
        CONSUMER_GROUP, PARTITION, prefetch=10000, offset=OFFSET)

    ehClient.run()

    start_time = time.time()

    for event_data in receiver.receive(timeout=10000):
        try:
            dictData = json.loads(event_data.body_as_str(encoding='UTF-8'))
            dictData["id"] = str(dictData["id"])
            client.CreateItem(collection_link, dictData)

            total += 1
        except errors.HTTPFailure as e:
            if e.status_code == 409:
                print('Item with id \'{0}\' was found'.format(dictData["id"]))
                pass
            else:
                raise

    end_time = time.time()        
    run_time = end_time - start_time
    print("Received {} messages in {} seconds".format(total, run_time))

except KeyboardInterrupt:
    pass
except Exception as e:    
    print("Error on_data: %s" % str(e))
finally:
    ehClient.stop()
