from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/update_feed', methods=['POST'])
def update_feed():
    data = request.json
    print("Received emoji update:", data)
    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    app.run(port=8081)

