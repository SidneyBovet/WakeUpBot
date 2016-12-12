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

def repo(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="My source code is located at https://github.com/SidneyBovet/WakeUpBot")

def register(bot, update):
    chat_id = update.message.chat_id
    message_id = update.message.message_id
    from_user = update.message.from_user
    bot.sendMessage(chat_id=chat_id, text="chat_id="+chat_id+" message_id="+message_id+" from_user="+from_user)


start_handler = CommandHandler('start', start)
start_handler = CommandHandler('register', register)
start_handler = CommandHandler('git', repo)
dispatcher.add_handler(start_handler)

updater.start_polling()
