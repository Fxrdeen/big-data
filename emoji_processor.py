from pyspark.sql import SparkSession
from pyspark.sql.functions import col, window

spark = SparkSession.builder.appName("EmojiProcessor").getOrCreate()
emoji_stream = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "emoji-stream") \
    .load()

aggregates = emoji_stream \
    .selectExpr("CAST(value AS STRING) as emoji") \
    .groupBy("emoji", window("timestamp", "2 seconds")) \
    .count()

query = aggregates \
    .selectExpr("to_json(struct(*)) AS value") \
    .writeStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("topic", "emoji-aggregates") \
    .outputMode("update") \
    .start()

query.awaitTermination()

