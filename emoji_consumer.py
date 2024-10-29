from kafka import KafkaConsumer
import requests
import json

consumer = KafkaConsumer(
    'emoji-aggregates',
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

for message in consumer:
    data = message.value
    response = requests.post("http://localhost:8081/update_feed", json=data)
    print("Sent data to client endpoint:", data)

