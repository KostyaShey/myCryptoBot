# myCryptoBot
bot to track DOGECOIN grows. Much WOW!

Intended to be used on a rasberry pi with linux installed and internet connection 

Add .env file to root it should include following props and values:
COINMARKETCAPKEY=
SECRET_KEY=
FLASK_APP=flaskr

get api credentials here https://pro.coinmarketcap.com/account

use this tutorial to configure telegram bot: https://medium.com/@robertbracco1/how-to-write-a-telegram-bot-to-send-messages-with-python-bcdf45d0a580

set up these cronjobs after done with the config:
  - $ flask coinmarketcap_api fetch
  - $ flask telegram_notifier check