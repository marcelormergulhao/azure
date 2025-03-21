from flask import Flask, request, jsonify
from http import HTTPStatus
from datetime import datetime

import json

from azure_wrapper import azure_wrapper

app = Flask(__name__)


@app.route("/device/<id>/publish", methods=["POST"])
def publish(id):
    payload = request.json
    print(
        f"Payload received: {payload}, sending as a measurement for device id {id} to event grid")
    # Send the payload to
    return ("", HTTPStatus.NO_CONTENT)


@app.route("/device/<id>", methods=["PUT"])
def upsert_device(id):
    payload = request.json
    print(f"Upserting device {id} with {payload}")
    payload["id"] = id
    saved_item = azure_wrapper.upsert_new_device(payload)
    return jsonify(saved_item)


@app.route("/device/<id>", methods=["GET"])
def retrieve_device(id):
    print(f"Retrive data for device {id}")
    device = azure_wrapper.get_device_profile(id)
    return jsonify(device)


@app.route("/device_map", methods=["POST"])
def post_device_map():
    payload = request.json
    filename = "map_{}".format(datetime.now().isoformat())
    print(f"Store device map in {filename}")
    azure_wrapper.upload_blob(filename=filename, data=json.dumps(payload))
    return ("", HTTPStatus.NO_CONTENT)


@app.route("/device_map", methods=["GET"])
def get_device_maps():
    print(f"Retrieve device maps")
    device_maps = azure_wrapper.list_blobs()
    return jsonify(device_maps)


@app.route("/device_map/<name>", methods=["GET"])
def get_device_map(name):
    print(f"Retrieve device map {name}")
    device_map = json.loads(azure_wrapper.get_blob(name))
    return jsonify(device_map)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
