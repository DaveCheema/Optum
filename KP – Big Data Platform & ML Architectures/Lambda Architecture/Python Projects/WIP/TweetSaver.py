import datetime
import json
from azure.eventhub import EventHubConsumerClient

import azure.cosmos.documents as documents
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.errors as errors

from configurations import EventHubSettings, DbSettings

#-----------------------------------------------------
# EventHub Connection settings.
#-----------------------------------------------------
CONNECTION_STRING = EventHubSettings["connection_string"]
EVENTHUB_NAME = EventHubSettings['eventhub_name']
CONSUMER_GROUP = EventHubSettings['consumer_group']

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

def on_event(partition_context, event):
    try:
        # Format event data into JSON object
        dictData = json.loads(event.body_as_str(encoding='UTF-8'))
        # Set id for the document item
        dictData["id"] = str(dictData["id"])
        # Add item to the cosmos DB collection.
        dbClient.CreateItem(collection_link, dictData)       
    except errors.HTTPFailure as e:
        if e.status_code == 409:
            print('Item with id \'{0}\' was found'.format(
                dictData["id"]))
        elif e.status_code == 429:
            print("Too many requests. Please slow it down.")
            pass
        else:
            raise
    except KeyError as e:
        print("\nKeyError on event data: {}.".format(event.body_as_str(encoding='UTF-8')))
        pass
    except Exception as e:
        print("An exception occurred: %s" % str(e))
        raise
    
def on_error(partition_context, error):
    # Put your code here. partition_context can be None in the on_error callback.
    if partition_context:
        print("An exception: {} occurred during receiving from Partition: {}.".format(
            partition_context.partition_id,
            error
        ))
    else:
        print("An exception: {} occurred during the load balance process.".format(error))


def create_db_and_collection(client):
    try:
        # setup database for this sample
        try:
            client.CreateDatabase({"id": DATABASE_ID})

        # If already exists, bypass it.
        except errors.HTTPFailure as e:
            if e.status_code == 409:
                pass
            else:
                raise

        # setup collection for this sample
        try:
            client.CreateContainer(
                database_link, {"id": COLLECTION_ID, "partitionKey": {"paths": ["/id"]}})

        # If already exists, bypass it.
        except errors.HTTPFailure as e:
            if e.status_code == 409:
               pass
            else:
                raise

    except errors.HTTPFailure as e:
        print('\ncreate_db_and_collection has caught an error. {0}'.format(e))
        raise
    finally:
        pass


class ChangeFeedManagement:

    @staticmethod
    def ProcessChangefeed(client):
        started = datetime.datetime.now()
        changeFeedCount = 0
        changeFeedErrorCount = 0
        print('\nReading Change Feed from the beginning\n')

        options = {}
        # For a particular Partition Key Range we can use options['partitionKeyRangeId']
        options["startFromBeginning"] = True
        # Start from beginning will read from the beginning of the history of the collection
        # If no startFromBeginning is specified, the read change feed loop will pickup the documents that happen while the loop / process is active
        try:
            response = client.QueryItemsChangeFeed(collection_link, options)

            for doc in response:
                changeFeedCount += 1
                print(doc)

            ended = datetime.datetime.now()
            timeSpan = ended - started
            print("\nReceived {} Change feeds in {} seconds".format(
                changeFeedCount, timeSpan))

        except errors.HTTPFailure as e:
            if e.status_code == 404:
                print('Database id: \'{0}\' and/or collection id: \'{1}\' were no found. Please investigate.'.format(
                    DATABASE_ID, COLLECTION_ID))
                pass
            else:
                raise
        except KeyError as e:
            changeFeedErrorCount += 1
            print("\nKeyError count: \'{0}\' \nKeyError found in \'{1}\' change feed event_data.".format(changeFeedErrorCount,
                                                                                                         doc))
            pass
        except Exception as e:
            print("An exception occurred: %s" % str(e))
            raise
        finally:
            pass

if __name__ == '__main__':
    
    # Create Cosmos DB connection
    dbClient = cosmos_client.CosmosClient(HOST, {'masterKey': MASTER_KEY})
    if dbClient is None:
            ClientCreateException: 'Cosmos DB client creation failed' 

    # Create Database and Collection instances.
    create_db_and_collection(dbClient)

    # Process Change Feed events.
    ChangeFeedManagement.ProcessChangefeed(dbClient)   
    
    # Create EventHub Consumer client.
    consumer_client = EventHubConsumerClient.from_connection_string(
        conn_str=CONNECTION_STRING,
        consumer_group=CONSUMER_GROUP,
        eventhub_name=EVENTHUB_NAME,
    )

    # Kick off the event reading process.
    try:
        with consumer_client:
            consumer_client.receive(
                on_event=on_event,
                on_error=on_error,
                # "-1" is from the beginning of the partition.
                starting_position="-1",
            )
    except KeyboardInterrupt:
        print('Stopped receiving.')
    finally:
        print("Done!")
        pass
