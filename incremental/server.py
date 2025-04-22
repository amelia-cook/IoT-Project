
from flask import Flask, request, jsonify
import json
from numstickies import print_display
from flask_cors import CORS, cross_origin

app = Flask(__name__)
num_stickies = 1

@app.route("/")
def home():
    return 'Hello from Raspberry Pi 5!'

@app.route('/calID', methods=['POST'])
def receive_calID():
    data = request.json

    cal_id = data['calID']
    print_display(num_stickies, "calID", cal_id)
    print(f"Received: {data}")
    return jsonify({"status": "success", "received": data}), 200

#@app.route('/createSticky', methods=['OPTIONS'])
#def createSticky_options():
#    response = jsonify(message="options allowed")
#    response.headers.add("Access-Control-Allow-Options", "*")
#    return response

@app.route('/createSticky', methods=['POST'])
@cross_origin()
def receive_createSticky():
    global num_stickies
    num_stickies += 1
    data = request.json
#    print(f"Received: {data}")

    name = data['name']
    contents = data['content']

#    print(f"about to print display")
    print_display(num_stickies, name, contents)
#    print(f"after print display")
    
    print(f"Received: {data}")
    return jsonify({"status": "success", "received": data}), 200

@app.route('/getSticky', methods=['GET'])
def send_sticky():
    name = request.args.get('name') 
    print(f"Received: {name}")
    return jsonify({"status": "success", "data": name}), 200

app.run(host="0.0.0.0", port=5000)
