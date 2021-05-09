import telegram_send
from flaskr.db import get_db
from flask import Blueprint

bp = Blueprint('telegram_notifier', __name__)


def fetch_from_db():
    return get_db().execute('SELECT * FROM responces ORDER BY id DESC LIMIT 1')


@bp.cli.command('check')
def send_data_to_telegram():
    data = fetch_from_db().fetchone()
    timestamp = data[1]
    percent_change_7d = data[2]
    percent_change_24h = data[3]
    price = data[4]
    message_24h = f'24h changes: {percent_change_24h}'
    message_7d = f'7d changes: {percent_change_7d}'
    message_price = f'new price: {price}'

    if percent_change_24h > 100 or percent_change_7d > 200:
        telegram_send.send(messages=[
                           f'{timestamp}\nDOGE MUCH WOW\n\n{message_price}\n\n{message_24h}\n{message_7d}\n\nhttps://coinmarketcap.com/currencies/dogecoin/'])
    elif percent_change_24h < -100 or percent_change_7d < -200:
        telegram_send.send(messages=[
                           f'{timestamp}\nDOGE NOT WOW\n\n{message_price}\n\n{message_24h}\n{message_7d}\n\nhttps://coinmarketcap.com/currencies/dogecoin/'])
    else:
        telegram_send.send(messages=["zzZZzZZzZZzZzzz"])