from kafka import KafkaConsumer
import requests
import json

consumer = KafkaConsumer(
    'emoji-stream',  # Adjusted to match the topic from the producer
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda x: x.decode('utf-8')  # No need for JSON decoding if we're sending strings
)

for message in consumer:
    emoji = message.value
    data = {'emoji': emoji}  # Wrap the emoji in a dictionary for the POST request
    response = requests.post("http://localhost:8081/update_feed", json=data)  # Ensure this endpoint is defined in your Flask app
    print("Sent data to client endpoint:", data)
