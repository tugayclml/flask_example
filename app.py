from flask import Flask, render_template, jsonify
from flask_cors import CORS
import requests
import xml.etree.ElementTree as ET

app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={
    r"/*": {
        "origins": "localhost"
    }
})


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_currency')
def get_currency():
    data = {"data": []}
    req = requests.get("https://www.tcmb.gov.tr/kurlar/today.xml")

    tree = ET.fromstring(req.content)
    for i in tree.getiterator('Currency'):
        if i.get('CurrencyCode') == "XDR":
            continue
        currency = {}
        currency['id'] = 'currency-' + i.get('CrossOrder')
        currency['CurrencyCode'] = i.get('CurrencyCode') + "/TRY"

        for child in i:
            currency[child.tag] = child.text
        data["data"].append(currency)
    return jsonify(data)


@app.route("/get_currency_codes")
def get_currency_codes():
    currency_codes = {}
    req = requests.get("https://www.tcmb.gov.tr/kurlar/today.xml")
    tree = ET.fromstring(req.content)
    for i in tree.getiterator('Currency'):
        if i.get('CurrencyCode') == "XDR":
            continue
        currency_codes['currency-'+i.get('CrossOrder')] = i.get('CurrencyCode') + "/TRY"
    return currency_codes


if __name__ == '__main__':
    app.run()