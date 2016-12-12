from telegram.ext import Updater
import logging
from telegram.ext import CommandHandler

competitors = {}

# Telegram bot token: 301838740:AAEBm36YW8ebArED6GScm4Hj1SRwtqwzDDM

updater = Updater(token='301838740:AAEBm36YW8ebArED6GScm4Hj1SRwtqwzDDM')
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

updater.start_polling()
