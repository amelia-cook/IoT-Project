from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return 'Hello from Raspberry Pi 5!'

@app.route('/calID', methods=['POST'])
def receive_calID():
    data = request.json
    print(f"Received: {data}")
    return jsonify({"status": "success", "received": data}), 200

@app.route('/getSticky', methods=['GET'])
def send_sticky():
    # data = request.json
    # print(f"Received: {data}")
    return jsonify({"status": "success", "received": "data"}), 200

app.run(host="0.0.0.0", port=5000)

