from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from datetime import datetime
from functools import reduce
from storage import Storage
import logging, json, copy

# Handlers #

def unknown(bot, update):
    checkNewDay(update.message.date)

    global commands
    message = "Sorry, I didn't understand that command. Available commands are:\n"
    for command in commands:
        message += "/"+command+"\n"
    bot.sendMessage(chat_id=update.message.chat_id, text=message)

def repo(bot, update):
    checkNewDay(update.message.date)

    bot.sendMessage(chat_id=update.message.chat_id, text="My source code is located at https://github.com/SidneyBovet/WakeUpBot")

def test(bot, update):
    checkNewDay(update.message.date)

    chat_id = update.message.chat_id
    message_id = update.message.message_id
    from_user = update.message.from_user
    date = update.message.date
    bot.sendMessage(chat_id=chat_id, text="chat_id="+str(chat_id)+" message_id="+str(message_id)+" from_user="+str(from_user)+" date="+str(date))

def arrived(bot, update):
    checkNewDay(update.message.date)
    global storage
    user_id = update.message.from_user['id']
    date = update.message.date

    if not user_id in storage.competitors:
        registerNewUser(bot, update)

    if user_id in storage.arrivalsYesterday:
        if storage.arrivalsYesterday[user_id].time() > date.time():
            bot.sendMessage(chat_id=update.message.chat_id, text="You did better than yesterday, gg!")

    if not user_id in storage.arrivals:
        storage.lastDate = date
        storage.arrivals[user_id] = date
    else:
        bot.sendMessage(chat_id=update.message.chat_id, text="You already participated today.")

    storage.storeData()

def registerNewUser(bot, update):
    checkNewDay(update.message.date)

    user_id = update.message.from_user['id']
    if not user_id in storage.competitors:
        storage.competitors[user_id] = update.message.from_user['first_name']
        storage.scores[user_id] = 0
        bot.sendMessage(chat_id=update.message.chat_id, text="Welcome to the competition, " + str(update.message.from_user['first_name']))
    else:
        bot.sendMessage(chat_id=update.message.chat_id, text="You are already in, " + str(update.message.from_user['first_name']))

def bestPlayer(bot, update):
    checkNewDay(update.message.date)

    if storage.arrivals == None or not storage.arrivals: # if None or empty
        bot.sendMessage(chat_id=update.message.chat_id, text="No one yet arrived at work today.")
    else:
        bestKey = findBestPlayerID(storage.arrivals)
        bot.sendMessage(chat_id=update.message.chat_id, text="Today's best is " + str(storage.competitors[bestKey]))

def displayScores(bot, update):
    global storage
    message = "Scores: (last updated yesterday)\n"
    for playerID in storage.competitors:
        message += "- " + storage.competitors[playerID] + ": " + str(storage.scores[playerID])  + "\n"
    bot.sendMessage(chat_id=update.message.chat_id, text=message)

# Helpers #

def findBestPlayerID(arrivals):
    return reduce(lambda bestKey,key: key if arrivals[key] < arrivals[bestKey] else bestKey, arrivals)

def checkNewDay(date):
    global storage
    if date.date() > storage.lastDate.date():
        storage.arrivalsYesterday = copy.deepcopy(storage.arrivals)
        points = 4
        while storage.arrivals and points > 0:
            bestPlayerID = findBestPlayerID(storage.arrivals)
            storage.scores[bestPlayerID] += points
            del storage.arrivals[bestPlayerID]
            points -= 1
        storage.arrivals = {};

if __name__ == '__main__':
    storage = Storage()

    with open('settings.json') as settings_file:
        settings = json.load(settings_file)

    updater = Updater(token=settings['token'])
    dispatcher = updater.dispatcher

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    # Handlers creation

    commands = {'start':registerNewUser, 'test':test, 'git':repo, 'arrived':arrived, 'best':bestPlayer, 'scoreboard':displayScores}
    for command in commands:
        dispatcher.add_handler(CommandHandler(command, commands[command]))
    unknown_handler = MessageHandler(Filters.command, unknown)
    dispatcher.add_handler(unknown_handler)

    # Start the bot #

    updater.start_polling()
    updater.idle()
