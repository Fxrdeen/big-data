1. Zookeeper and Kafka Setup:Before running the application, ensure Zookeeper and Kafka are running. This setup only needs to be done once:
  Start Zookeeper:
        zookeeper-server-start.sh /path/to/kafka/config/zookeeper.properties
  Start Kafka Broker:
        kafka-server-start.sh /path/to/kafka/config/server.properties
  Create Kafka Topics:
        kafka-topics.sh --create --topic emoji-stream --bootstrap-server localhost:9092 --partitions 3 --replication-factor 1
        kafka-topics.sh --create --topic emoji-aggregates --bootstrap-server localhost:9092 --partitions 3 --replication-factor 1


2.Go API for Emoji Submission(File Name: emoji_api.go)
  i]Initialize Go module:  go mod init emoji_api
  ii]Install dependencies: go get github.com/Shopify/sarama
  iii]Run the Go server:   go run emoji_api.go
Your Go server will now be listening at http://localhost:8080/send_emoji.

3. Spark Job for Aggregating Emojis(File Name: emoji_processor.py)
   i]Run the Spark job:    spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12
This job will aggregate emojis every 2 seconds and send results to the emoji-aggregates topic.

4. Kafka Consumer in Python(File Name: emoji_consumer.py)
   Install necessary packages:  pip install kafka-python requests
   Run the consumer:            python3 emoji_consumer.py
This consumer will forward aggregated emoji data to the client endpoint.

5. Flask Client Endpoint(File Name: emoji_client.py)
   Install Flask:               pip install flask
   Run the Flask server:        python3 emoji_client.py
The Flask server will now listen on http://localhost:8081/update_feed and print received emoji updates.

6. Testing the Setup
    i] Submit Emojis: Open a terminal and test emoji submissions using curl:
          curl "http://localhost:8080/send_emoji?emoji=👍"
          curl "http://localhost:8080/send_emoji?emoji=🎉"
View Aggregated Results: After several submissions, check the Flask server logs to see aggregated updates appearing.

# Summary of Commands

Here's a summary of commands to run in separate terminals:
Zookeeper:       zookeeper-server-start.sh /path/to/kafka/config/zookeeper.properties
Kafka Broker:    kafka-server-start.sh /path/to/kafka/config/server.properties
Go API:          go run emoji_api.go
Spark Job:       spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.1 emoji_processor.py
Python Consumer: python emoji_consumer.py
Flask Client:    python emoji_client.py

This should fully set up and execute the distributed emoji system for real-time aggregation and display. Let me know if you have questions!
