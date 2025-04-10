import flask import Flask

app = Flask(__name__)

@app.route("/")
def home()
  return 'Hello from Raspberry Pi 5!'

@app.route('/data', methods=['POST'])
def receive_data(): #fix this 
    data = request.json
    print(f"Received: {data}")
    return jsonify({"status": "success", "received": data}), 200

app.run(host="0.0.0.0", port=5000)

#get raspberry pi ip address (in termianl) --> hostname -I 