import functools
import requests
import os
import json
import telegram_send
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flaskr.db import get_db

bp = Blueprint('coinmarketcapAPI_test', __name__, url_prefix='/coinmarketcapAPI')

@bp.route('/fetch', methods=('GET', 'POST'))
def fetch_coinmarketcapAPI_data():
    
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
        'start':'1',
        'limit':'100'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': '0545f2e1-51b9-45c0-8fc2-0140cdf559f7',
    }

    if request.method == 'POST':
        print('ping')
        
        response = requests.get(
            url,
            headers=headers,
            params=parameters
        )

        response_body = response.json()
        response_logs = []
        response_logs.append(response_body["data"])


        with open(os.path.join(os.environ["HOMEPATH"], "Desktop/myCryptoBot/API/logs.json"),
                "w",
                encoding='utf-8') as f:
            json.dump(response_logs, f, sort_keys=True, indent=4)

        


    return render_template('test_api.html')

@bp.route('/write', methods=(['POST']))
def write_data_to_db():

    with open(os.path.join(os.environ["HOMEPATH"], "Desktop/myCryptoBot/API/logs.json")) as json_file:
        data = json.load(json_file)

        def function(coin):
                return coin['symbol'] == 'DOGE'

        doge = list(filter(function, data[0]))[0]

        db = get_db()
        db.execute(
            'INSERT INTO responces (percent_change_7d, percent_change_24h, price) VALUES (?, ?, ?)',
            (doge['quote']['USD']['percent_change_7d'], doge['quote']['USD']['percent_change_24h'], doge['quote']['USD']['price'])
        )
        db.commit()

    return render_template('test_api.html')

@bp.route('/send', methods=(['POST']))
def send_data_to_telegram():

    flash('Sending message')
    telegram_send.send(messages=["Hello! This is myCryptoBot"])

    return render_template('test_api.html')