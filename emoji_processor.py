from flask import Flask, request
from kafka import KafkaProducer
import json

app = Flask(__name__)

# Initialize Kafka Producer
producer = KafkaProducer(bootstrap_servers='localhost:9092',
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

@app.route('/send_emoji', methods=['GET'])
def send_emoji():
    emoji = request.args.get('emoji')
    print(f"Sending emoji: {emoji}")  # Log the emoji being sent
    if emoji:  # Check if emoji is not None
        producer.send('emoji-stream', value=emoji)
        producer.flush()  # Ensure all messages are sent before returning
        print(f"Emoji {emoji} sent to Kafka successfully")  # Log successful send
        return "Emoji received", 200
    else:
        print("No emoji provided")  # Log if no emoji is provided
        return "Emoji not specified", 400

if __name__ == '__main__':
    app.run(port=8081)
