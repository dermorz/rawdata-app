# coding=utf-8

import base64
import json

from flask import Flask, render_template
import requests

from config import API_URL, APP_ID, APP_TOKEN


app = Flask(__name__)

FIELDS = ['id', 'name', 'active', 'brand_id', 'description_long',
          'description_short', 'variants', 'inactive_variants',
          'min_price', 'max_price', 'sale', 'default_image',
          'tags', 'merchant_id']


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
    r = shop_api("products", {"ids": [product_id], "fields": FIELDS})
    product = r.json()[0]["products"]["ids"].values()[0]
    return render_template("detail.html", product=product)


if __name__ == "__main__":
    app.run(debug=True)
