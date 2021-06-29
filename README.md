# myCryptoBot
Bot to track DOGECOIN grows. Much WOW!

Intended to be used on a rasberry pi with NOOBS (https://github.com/raspberrypi/noobs) installed and internet connection 

Get coinmarketcap API credentials here https://pro.coinmarketcap.com/account

Use this tutorial to configure telegram bot: https://medium.com/@robertbracco1/how-to-write-a-telegram-bot-to-send-messages-with-python-bcdf45d0a580

set up these cronjobs after done with the config:
  - $ flask coinmarketcap_api fetch
  - $ flask telegram_notifier check

Use this command to turn sleepmode on and off:
flask telegram_notifier sleepmode
Arguments: 'on' and 'off'

Use this command to configure the notification threshold:
flask telegram_notifier threshold