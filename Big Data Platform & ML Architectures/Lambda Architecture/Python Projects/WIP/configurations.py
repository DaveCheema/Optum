TwitterSettings = {
    'consumer_key': '5j6NRxTCMeYeX699HqcaQmnW1',
    'consumer_secret': 'OJGV4ZZJZ92q5s0mTDeXKvJEqs1i4JXicXm9onwQUEfZuk1aXB',
    'access_token': '283119593-rBCTLgENNzPWjj9nB065jWgD9RZlqSSZzAUJ0CHz',
    'access_secret': '116ErxfGGImxpa1liSkPRDgYVfr1VPRDeHlJq1aIRSBz3',
    'filter_keywords': ['Trump', 'impeachment', 'Pelosi']
}

EventHubSettings = {
    'address': 'amqps://dc1-event-hubs.servicebus.windows.net/dc1-event-hub',
    'user': "policy1",
    'key': 'oiDHNS0xNxMGn2e22FMUprSxhfUBPxD4o3185li5N9E=',
    'partition_id': '0',
    'eventhub_name': 'dc1-event-hub',
    'consumer_group': '$Default',
    'wait_for': '2',
    'connection_string': 'Endpoint=sb://dc1-event-hubs.servicebus.windows.net/;SharedAccessKeyName=policy1;SharedAccessKey=oiDHNS0xNxMGn2e22FMUprSxhfUBPxD4o3185li5N9E='
}

DbSettings = {
    'host': 'https://dc1-cosmos-db.documents.azure.com:443/',
    'master_key': 'jgqEmCx2sq3fEt2L3DrCjUDabEFY5i22Um6O2a977fJKQxOAaGpiSejA9rbkRF3b8K4juLQBMY4VGycLBDlqTg==',
    'database_id': 'dc1-tweet-store',
    'collection_id': 'dc1-tweets',
    'preferred_locations' : 'West US'
}
