from flask import Flask, request
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return "Emoji Sender is running!"

@app.route('/send_emoji', methods=['GET'])
def send_emoji():
    emoji = request.args.get('emoji')
    if emoji:
        response = requests.get(f"http://localhost:8081/send_emoji?emoji={emoji}")
        return response.text, response.status_code
    else:
        return "Emoji not specified", 400

if __name__ == '__main__':
    app.run(port=8082)
