# coding=utf-8

import base64
import json

from flask import Flask
import requests

from config import API_URL, APP_ID, APP_TOKEN


app = Flask(__name__)


def get_auth_token():
    data = "%s:%s" % (APP_ID, APP_TOKEN)
    encoded = base64.b64encode(data)
    return "Basic " + encoded.decode("ascii")


def shop_api(command, data):
    payload = json.dumps([{command: data}])
    headers = {'Authorization': get_auth_token()}
    return requests.get(API_URL, data=payload, headers=headers)


@app.route("/<int:product_id>")
def index(product_id):
    r = shop_api("products", {"ids": [product_id], "fields": []})
    return r.content


if __name__ == "__main__":
    app.run(debug=True)
