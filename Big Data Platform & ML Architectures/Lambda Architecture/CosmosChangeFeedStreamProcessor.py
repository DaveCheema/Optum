# Databricks notebook source
readConfig = {
    "Endpoint" : "https://dc2-cosmos-db.documents.azure.com:443/",
    "Masterkey" : "ediWik75DjUVg1Cynl9EOT2AiF3wfa0ytf1apvNlz4zAdZr0Uo4lkdXKJqSpo4fD9zrcoiFUfC3G8oI3eEc77w==",
    "Database" : "dc2-tweet-store",
    "Collection" : "dc2-tweets",
    "ReadChangeFeed" : "true",
    "ChangeFeedQueryName" : "dc2-change-feed-name",
    "RollingChangeFeed": "false",
    "ChangeFeedStartFromTheBeginning" : "true",
    "ConnectionMode" : "Gateway",
    "InferStreamSchema" : "true",
    "ChangeFeedCheckpointLocation" : "/temp"  
}

# COMMAND ----------

# Start reading change feed as a stream
streamData = spark.readStream.format("com.microsoft.azure.cosmosdb.spark.streaming.CosmosDBSourceProvider").options(**readConfig).load()

# COMMAND ----------

# Start projecting change results.
query = streamData.withColumn("count_column", streamData["id"].substr(0, 0)).groupBy("count_column").count().writeStream.outputMode("complete").format("console").start()
