import telegram_send
from flaskr.db import get_db
from flask import Blueprint
import click

bp = Blueprint('telegram_notifier', __name__)


def fetch_config_from_db():
    return get_db().execute('SELECT * FROM config ORDER BY id DESC LIMIT 1').fetchone()


def fetch_from_db():
    return get_db().execute('SELECT * FROM responces ORDER BY id DESC LIMIT 1').fetchone()



@bp.cli.command('check')
def send_data_to_telegram():
    config = fetch_config_from_db()
    config_low_24h = config[2]
    config_high_24h = config[3]
    config_low_7d = config[4]
    config_high_7d = config[5]
    if config[6] == 0:
        sleep_mode = False
    else:
        sleep_mode = True

    data = fetch_from_db()
    timestamp = data[1]
    percent_change_7d = data[2]
    percent_change_24h = data[3]
    price = data[4]
    message_24h = f'24h changes: {percent_change_24h}'
    message_7d = f'7d changes: {percent_change_7d}'
    message_price = f'new price: {price}'

    try:
        if percent_change_24h > config_high_24h or percent_change_7d > config_high_7d:
            telegram_send.send(messages=[
                            f'{timestamp}\nDOGE MUCH WOW\n\n{message_price}\n\n{message_24h}\n{message_7d}\n\nhttps://coinmarketcap.com/currencies/dogecoin/'])
        elif percent_change_24h < config_low_24h or percent_change_7d < config_low_7d:
            telegram_send.send(messages=[
                            f'{timestamp}\nDOGE NOT WOW\n\n{message_price}\n\n{message_24h}\n{message_7d}\n\nhttps://coinmarketcap.com/currencies/dogecoin/'])
        elif sleep_mode:
            telegram_send.send(messages=["zzZZzZZzZZzZzzz"])
    except Exception as e:
        print(e)

@bp.cli.command('sleepmode')
@click.argument('state')
def send_data_to_telegram(state):

    states = ['on', 'off']

    if state not in states:
        print('sleepmode argumets are "on" and "off". other inputs are restricted')
    else:
        if state == 'on':
            get_db().execute(
                f'UPDATE config SET sleep_mode = {1} WHERE id = 1')
            get_db().commit()
        else:
            get_db().execute(
                f'UPDATE config SET sleep_mode = {0} WHERE id = 1')
            get_db().commit()
        telegram_send.send(messages=[f'Sleepmode is {state}'])

@bp.cli.command('threshold')
#@click.argument('state')
def send_data_to_telegram():

    direction_values = ['low', 'high']
    interval_values = ['7d', '24h']

    direction = ''
    interval = 0
    new_value = ''

    while direction not in direction_values:
        direction = input('change values for increase or decrease? "low" or "high" ')
        print('wrong input. please select either "low" or "high"' )
    while interval not in interval_values:
        interval = input('change values for what interval? "7d" or "24h" ')
        print('wrong input. please select either "7d" or "24h"' )
    while type(new_value) != int:
        try:
            new_value = int(input('new value? 7/24 '))
        except:
            print('wrong input. please select select a number' )

    telegram_send.send(messages=[f'Setting new threshold for {interval} interval for {direction} direction: {str(new_value)}'])

    get_db().execute(
        f'UPDATE config SET {direction}_{interval} = {str(new_value)} WHERE id = 1')
    get_db().commit()