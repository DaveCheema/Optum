import sys
import logging
import datetime
import time
import os

from azure.eventhub import EventHubClient, Sender, EventData

class SendtoEventHub():

    # Address can be in either of these formats:
    # "amqps://<URL-encoded-SAS-policy>:<URL-encoded-SAS-key>@<namespace>.servicebus.windows.net/eventhub"
    # "amqps://<namespace>.servicebus.windows.net/<eventhub>"
    # SAS policy and key are not required if they are encoded in the URL
    ADDRESS = "amqps://dc1-event-hubs.servicebus.windows.net/dc1-event-hub"
    USER = "policy1"
    KEY = "6eW5ravrVORk1DOU5sg3SuApCNMat1A65boJy7zCp4k="

    logger = logging.getLogger("azure")

    def __init__(self, client):
        self.client = client
        # Create Event Hubs client
        self.sender = client.add_sender(partition="0")
        client.run()

    def sendMessage(self, EventData):
        try:
            sender.send(EventData(message))
        except:
            raise
        finally:
            logger.info("Runtime: {} seconds".format(run_time))