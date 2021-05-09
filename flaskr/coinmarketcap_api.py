import functools
import requests
import json
import os
from flaskr.db import get_db
from flask import Blueprint


bp = Blueprint('coinmarketcap_api', __name__)

@bp.cli.command('fetch')
def fetch_coinmarketcapAPI_data():
    
    print('fetching')
    key = os.environ['COINMARKETCAPKEY']

    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
        'start':'1',
        'limit':'100'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': key,
    }
        
    response = requests.get(
        url,
        headers=headers,
        params=parameters
    )
    response_body = response.json()

    def function(coin):
            return coin['symbol'] == 'DOGE'
    try:
        doge = list(filter(function, response_body["data"]))[0]
    except Exception as E:
        print(E)

    db = get_db()
    db.execute(
            'INSERT INTO responces (percent_change_7d, percent_change_24h, price) VALUES (?, ?, ?)',
            (doge['quote']['USD']['percent_change_7d'], doge['quote']['USD']['percent_change_24h'], doge['quote']['USD']['price'])
        )
    db.commit()

    print('done fetching')
